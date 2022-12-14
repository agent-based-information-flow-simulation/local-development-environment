from __future__ import annotations


class TimeseriesDoesNotExistException(Exception):
    def __init__(self, simulation_id: str):
        super().__init__(f"[simulation {simulation_id}] Timeseries does not exist")
