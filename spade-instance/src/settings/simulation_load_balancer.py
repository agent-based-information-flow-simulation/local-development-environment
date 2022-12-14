from __future__ import annotations

import os

from pydantic import BaseSettings


class SimulationLoadBalancerSettings(BaseSettings):
    url: str = os.environ.get("SIMULATION_LOAD_BALANCER_URL", "")
    announcement_period: int = int(
        os.environ.get("SIMULATION_LOAD_BALANCER_ANNOUNCEMENT_PERIOD", 10)
    )


simulation_load_balancer_settings = SimulationLoadBalancerSettings()
