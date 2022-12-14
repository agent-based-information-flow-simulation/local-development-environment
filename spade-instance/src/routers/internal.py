from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from src.dependencies.state import state
from src.exceptions.simulation import SimulationException
from src.instance.state import State
from src.models.instance import InstanceStatus

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_ROUTER_INTERNAL", "INFO"))

router = APIRouter()


@router.post("/internal/instance/status", status_code=201)
async def update_active_instance_status(
    instance_status: InstanceStatus, state: State = Depends(state)
):
    logger.debug(f"Update active instance state: {instance_status}")
    try:
        await state.update_active_state(
            instance_status.status,
            instance_status.num_agents,
            instance_status.broken_agents,
        )
    except SimulationException as e:
        raise HTTPException(400, str(e))
