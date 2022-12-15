from __future__ import annotations

import random
import uuid
from typing import TYPE_CHECKING

import numpy

from src.exceptions.graph_creator import GraphNotGeneratedException
from src.services.base import BaseService
from src.settings.communication_server import communication_server_settings

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List


class GraphCreatorService(BaseService):
    def run_generated_algorithm(
        self, graph_code_lines: List[str]
    ) -> List[Dict[str, Any]]:
        code_without_imports = self._remove_imports(graph_code_lines)
        exec("\n".join(code_without_imports))
        try:
            algorithm: Callable[[str], List[Dict[str, Any]]] = locals()[
                "generate_graph_structure"
            ]
        except KeyError:
            raise GraphNotGeneratedException()
        return algorithm(communication_server_settings.domain)

    def _remove_imports(self, graph_code_lines: List[str]) -> List[str]:
        return list(
            filter(lambda line: not line.startswith("import"), graph_code_lines)
        )
