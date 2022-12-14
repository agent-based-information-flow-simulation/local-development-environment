from __future__ import annotations

from typing import TYPE_CHECKING

import psutil

from src.models.instance import InstanceStatus
from src.services.base import BaseServiceWithState

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, List, Tuple

    from src.instance.state import State
    from src.instance.status import Status


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
        self,
        simulation_id: str,
        agent_code_lines: List[str],
        agent_data: List[Dict[str, Any]],
    ):
        self.state.start_simulation_process(simulation_id, agent_code_lines, agent_data)

    async def kill_simulation(self) -> None:
        await self.state.kill_simulation_process()

    async def get_state(self) -> Tuple[Status, str, int, List[str]]:
        return await self.state.get_state()
