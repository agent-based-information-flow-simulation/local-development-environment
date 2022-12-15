from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from src.database.repositories.base import BaseRepository

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, List


@dataclass
class SavedAgentUpdates:
    num_updates: int
    num_acknowledged: int


class AgentUpdatesRepository(BaseRepository):
    collection_name = "agents"

    async def save_agent_updates(
        self, batch: List[Dict[str, Any]]
    ) -> SavedAgentUpdates:
        data = [
            {
                "timestamp": datetime.fromtimestamp(agent["__timestamp__"]),
                "metadata": {
                    "jid": agent["jid"],
                    "simulation_id": agent["simulation_id"],
                },
                "agent": agent,
            }
            for agent in batch
        ]
        result = await self.collection.insert_many(data)
        return SavedAgentUpdates(len(result.inserted_ids), result.acknowledged)
