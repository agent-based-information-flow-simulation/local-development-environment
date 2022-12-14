from __future__ import annotations

import os

from pydantic import BaseSettings


class SimulationSettings(BaseSettings):
    status_url: str = os.environ.get("ACTIVE_SIMULATION_STATUS_ANNOUCEMENT_URL", "")
    status_period: int = int(
        os.environ.get("ACTIVE_SIMULATION_STATUS_ANNOUCEMENT_PERIOD", 10)
    )
    registration_retry_after: int = int(
        os.environ.get("AGENT_REGISTRATION_RETRY_AFTER", 5)
    )
    registration_max_concurrency: int = int(
        os.environ.get("AGENT_REGISTRATION_MAX_CONCURRENCY", 5)
    )


simulation_settings = SimulationSettings()
