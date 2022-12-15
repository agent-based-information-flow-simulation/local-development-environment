from __future__ import annotations


class GraphNotGeneratedException(Exception):
    def __init__(self):
        super().__init__("Could not generate graph")
