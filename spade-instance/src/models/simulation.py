from __future__ import annotations

from typing import List

import orjson
from pydantic import BaseModel


class CreateSimulation(BaseModel):
    code_lines: List[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class CreatedSimulation(BaseModel):
    simulation_id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class DeletedSimulation(BaseModel):
    simulation_id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
