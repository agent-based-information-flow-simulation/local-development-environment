from __future__ import annotations

from typing import List

from pydantic import BaseModel


class CreateSimulation(BaseModel):
    code_lines: List[str]


class DeletedSimulation(BaseModel):
    simulation_id: str
