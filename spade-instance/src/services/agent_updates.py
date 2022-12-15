from __future__ import annotations

from typing import TYPE_CHECKING

from src.database.repositories.agent_updates import AgentUpdatesRepository
from src.services.base import BaseServiceWithRepository

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, List

    from src.database.repositories.agent_updates import SavedAgentUpdates


class AgentUpdatesService(BaseServiceWithRepository):
    repository_type = AgentUpdatesRepository

    @property
    def repository(self) -> repository_type:
        return self._repository

    async def save_agent_updates(
        self, batch: List[Dict[str, Any]]
    ) -> SavedAgentUpdates:
        return await self.repository.save_agent_updates(batch)
