from __future__ import annotations

import os

from pydantic import BaseSettings


class InstanceSettings(BaseSettings):
    process_health_check_period: int = int(
        os.environ.get("SIMULATION_PROCESS_HEALTH_CHECK_PERIOD", 5)
    )


instance_settings = InstanceSettings()
