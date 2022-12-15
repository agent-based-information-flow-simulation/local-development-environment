from __future__ import annotations

from typing import TYPE_CHECKING

from src.database.repositories.agent_updates import AgentUpdatesRepository
from src.services.base import BaseServiceWithRepository


class AgentUpdatesService(BaseServiceWithRepository):
    repository_type = AgentUpdatesRepository

    @property
    def repository(self) -> repository_type:
        return self._repository
