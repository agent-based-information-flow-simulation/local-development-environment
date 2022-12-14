from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from fastapi_utils.tasks import repeat_every

from src.instance.state import get_app_simulation_state
from src.settings.instance import instance_settings

if TYPE_CHECKING:  # pragma: no cover
    from typing import Awaitable, Callable

    from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_REPEATED_TASKS_SIMULATION", "INFO"))


def create_simulation_process_health_check_handler(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:
    @repeat_every(
        seconds=instance_settings.process_health_check_period,
        raise_exceptions=False,
        logger=logger,
    )
    async def simulation_process_health_check_handler() -> Awaitable[None]:
        await get_app_simulation_state(app).verify_simulation_process()

    return simulation_process_health_check_handler
