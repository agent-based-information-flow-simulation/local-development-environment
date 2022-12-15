from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from src.dependencies.services import instance_service
from src.exceptions.simulation import SimulationException
from src.models.instance import InstanceStatus
from src.services.instance import InstanceService

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_ROUTER_INTERNAL", "INFO"))

router = APIRouter(default_response_class=ORJSONResponse)


@router.post("/internal/instance/status", status_code=201)
async def update_active_instance_status(
    instance_status: InstanceStatus,
    instance_service: InstanceService = Depends(instance_service),
):
    logger.debug(f"Update active instance state: {instance_status}")

    try:
        await instance_service.update_active_status(instance_status)
    except SimulationException as e:
        raise HTTPException(400, str(e))
