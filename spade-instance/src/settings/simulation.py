from __future__ import annotations

import os

from pydantic import BaseSettings


class SimulationSettings(BaseSettings):
    status_period: int = int(
        os.environ.get("ACTIVE_SIMULATION_STATUS_ANNOUCEMENT_PERIOD", 10)
    )


simulation_settings = SimulationSettings()
