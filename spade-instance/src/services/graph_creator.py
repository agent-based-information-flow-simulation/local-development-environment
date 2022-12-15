from __future__ import annotations

import random
import uuid
from typing import TYPE_CHECKING

import numpy

from src.exceptions.graph_creator import GraphNotGeneratedException
from src.services.base import BaseService

if TYPE_CHECKING: # pragma: no cover
    from typing import Any, Callable, Dict, List


class GraphCreatorService(BaseService):
    fake_domain: str = "x"
    
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
        return algorithm(self.fake_domain)

    def _remove_imports(self, graph_code_lines: List[str]) -> List[str]:
        return list(
            filter(lambda line: not line.startswith("import"), graph_code_lines)
        )
