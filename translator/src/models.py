from __future__ import annotations

from typing import List

import orjson
from pydantic import BaseModel


class AgentsAssemblyCode(BaseModel):
    code_lines: List[str]
    module_lines: List[List[str]]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class PythonSpadeCode(BaseModel):
    agent_code_lines: List[str]
    graph_code_lines: List[str]
    module_code_lines: List[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
