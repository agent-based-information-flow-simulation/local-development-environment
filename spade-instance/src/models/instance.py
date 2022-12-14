from __future__ import annotations

from typing import List

from pydantic import BaseModel

from src.instance.status import Status


class InstanceStatus(BaseModel):
    status: Status
    num_agents: int
    broken_agents: List[str]
