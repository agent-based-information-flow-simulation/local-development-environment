from __future__ import annotations

import asyncio
import logging
import os
from multiprocessing import Process
from typing import TYPE_CHECKING

import psutil
from starlette.requests import Request

from src.exceptions.simulation import (
    SimulationException,
    SimulationIdNotSetException,
    SimulationStateNotSetException,
)
from src.instance.status import Status
from src.simulation.main import main
from aioprocessing import AioQueue
import asyncio

if TYPE_CHECKING:  # pragma: no cover
    from asyncio.locks import Lock
    from typing import Any, Callable, Coroutine, Dict, List, Tuple

    from fastapi import FastAPI
    from src.services.agent_updates import AgentUpdatesService

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_STATE", "INFO"))


class State:
    def __init__(self, app: FastAPI):
        self.app: FastAPI = app
        self.mutex: Lock = asyncio.Lock()
        self.status: Status = Status.IDLE
        self.simulation_process: Process | None = None
        self.simulation_id: str | None = None
        self.num_agents: int = 0
        self.broken_agents: List[str] = []
        self.agent_updates: AioQueue | None = None

    def _clean_state(self) -> None:
        self.simulation_process = None
        self.simulation_id = None
        self.num_agents = 0
        self.broken_agents = []
        self.agent_updates = None

    async def update_active_state(
        self, status: Status, num_agents: int, broken_agents: List[str]
    ) -> Coroutine[Any, Any, None]:
        logger.debug(f"Setting state: {status}, {num_agents}, {broken_agents}")
        async with self.mutex:
            if self.status == status.IDLE:
                raise SimulationException(self.status, "Simulation is not running.")

            self.status = status
            self.num_agents = num_agents
            self.broken_agents = broken_agents

    async def get_state(self) -> Tuple[Status, str | None, int, List[str]]:
        logger.debug("Getting state")
        async with self.mutex:
            return (
                self.status,
                self.simulation_id,
                self.num_agents,
                self.broken_agents,
            )

    async def get_simulation_id(self) -> Coroutine[Any, Any, str]:
        logger.debug("Getting simulation id")
        async with self.mutex:
            if self.simulation_id is None:
                raise SimulationIdNotSetException()

            return self.simulation_id

    async def start_simulation_process(
        self,
        simulation_id: str,
        agent_code_lines: List[str],
        agent_data: List[Dict[str, Any]],
    ) -> Coroutine[Any, Any, None]:
        logger.debug(
            f"Starting simulation {simulation_id}, state: {await self.get_state()}"
        )
        async with self.mutex:
            if self.status not in (Status.IDLE, Status.DEAD):
                raise SimulationException(self.status, "Simulation is already running.")

            self.status = Status.STARTING
            self.simulation_id = simulation_id
            self.agent_updates = AioQueue()
            self.simulation_process = Process(
                target=main, args=(agent_code_lines, agent_data, self.agent_updates)
            )
            self.simulation_process.start()
            asyncio.create_task(self.read_and_save_agent_updates(self.agent_updates, self.simulation_id))

    async def read_and_save_agent_updates(self, agent_updates: AioQueue, simulation_id: str) -> None:
        from src.dependencies.services.app import agent_updates as agent_updates_service
        logger.info(f"Started reading agent updates for simulation {simulation_id}")
        queue_size_task = asyncio.create_task(self.show_queue_size(agent_updates, every_seconds=30))
        agent_updates_service = await agent_updates_service(self.app)
        while True:
            update: Dict[str, Any] | None = await agent_updates.coro_get()
            if update is None:
                break
            update["simulation_id"] = simulation_id
            await agent_updates_service.save_agent_updates([update])
        queue_size_task.cancel()
        logger.info(f"Stopped reading agent updates for simulation {simulation_id}")
        logger.info(f"Unread items in agent updates queue after stopping: {agent_updates.qsize()}")

    async def show_queue_size(self, agent_updates: AioQueue, every_seconds: float) -> None:
        while True:
            logger.info(f"Unread items in agent updates queue: {agent_updates.qsize()}")
            await asyncio.sleep(every_seconds)

    async def kill_simulation_process(self) -> Coroutine[Any, Any, None]:
        logger.debug(f"Killing simulation, state: {await self.get_state()}")
        async with self.mutex:
            if self.simulation_process is None:
                raise SimulationException(self.status, "Simulation is not running.")

            self.status = Status.IDLE
            self.simulation_process.kill()
            await self.agent_updates.coro_put(None)
            self._clean_state()

    async def get_simulation_memory_usage(self) -> Coroutine[Any, Any, float]:
        logger.debug(
            f"Getting simulation memory usage, state: {await self.get_state()}"
        )
        async with self.mutex:
            if (
                self.simulation_process is not None
                and self.simulation_process.is_alive()
            ):
                return (
                    psutil.Process(self.simulation_process.pid).memory_info().rss
                    / 1024**2
                )

            return 0.0

    async def verify_simulation_process(self) -> Coroutine[Any, Any, None]:
        logger.debug(f"Verify simulation process, state: {await self.get_state()}")
        async with self.mutex:
            if (
                self.simulation_process is not None
                and not self.simulation_process.is_alive()
            ):
                logger.warning("Simulation process is dead")
                self.status = Status.DEAD
                self._clean_state()


def set_app_simulation_state(app: FastAPI, state: State) -> None:
    app.state.simulation_state = state


def get_app_simulation_state(app: FastAPI) -> State:
    try:
        return app.state.simulation_state
    except AttributeError:
        raise SimulationStateNotSetException()


def get_simulation_state() -> Callable[[Request], State]:
    def _get_simulation_state(request: Request) -> State:
        return get_app_simulation_state(request.app)

    return _get_simulation_state


def create_simulation_state_startup_handler(app: FastAPI) -> Callable[[], None]:
    def simulation_state_startup_handler() -> None:
        logger.info("Setting up simulation state")
        set_app_simulation_state(app, State(app))
        logger.info("Simulation state set up complete")

    return simulation_state_startup_handler


def create_simulation_state_shutdown_handler(
    app: FastAPI,
) -> Callable[[], Coroutine[Any, Any, None]]:
    async def simulation_state_shutdown_handler() -> Coroutine[Any, Any, None]:
        logger.info("Shutting down simulation")
        try:
            await get_app_simulation_state(app).kill_simulation_process()
        except SimulationException as e:
            logger.info(str(e))
        logger.info("Simulation shutdown complete")

    return simulation_state_shutdown_handler
