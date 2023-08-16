from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import uuid4

import psutil

from src.instance.status import Status
from src.services.base import BaseServiceWithState

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, List, Tuple

    from src.instance.state import State


@dataclass
class InstanceStatus:
    status: Status
    num_agents: int
    broken_agents: List[str]


class InstanceService(BaseServiceWithState):
    @property
    def state(self) -> State:
        return self._state

    async def get_instance_information(self) -> Dict[str, Any]:
        api_memory_usage = psutil.Process().memory_info().rss / 1024**2
        simulation_memory_usage = await self.state.get_simulation_memory_usage()
        status, simulation_id, num_agents, broken_agents = await self.state.get_state()
        return {
            "status": status.name,
            "simulation_id": simulation_id,
            "num_agents": num_agents,
            "broken_agents": broken_agents,
            "api_memory_usage_MiB": api_memory_usage,
            "simulation_memory_usage_MiB": simulation_memory_usage,
        }

    async def update_active_status(self, status: InstanceStatus) -> None:
        await self.state.update_active_state(
            status.status, status.num_agents, status.broken_agents
        )

    async def start_simulation(
        self, agent_code_lines: List[str], module_code_lines: List[str], agent_data: List[Dict[str, Any]]
    ) -> str:
        simulation_id = uuid4().hex[:8]
        await self.state.start_simulation_process(
            simulation_id, agent_code_lines, module_code_lines, agent_data
        )
        return simulation_id

    async def kill_simulation(self) -> None:
        await self.state.kill_simulation_process()

    async def get_state(self) -> Tuple[Status, str, int, List[str]]:
        state = await self.state.get_state()
        # ugly conversion but state[1] can be None
        if state[1] is None:
            return (state[0], "", state[2], state[3])
        else:
            return (state[0], state[1], state[2], state[3])

    async def get_simulation_id(self) -> str | None:
        _, simulation_id, _, _ = await self.state.get_state()
        return simulation_id

    async def is_simulation_running(self) -> bool:
        status, _, _, _ = await self.state.get_state()
        return status in (Status.RUNNING, Status.STARTING)
