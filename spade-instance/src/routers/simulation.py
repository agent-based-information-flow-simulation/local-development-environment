from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from src.dependencies.services import instance_service
from src.exceptions.simulation import SimulationException
from src.models.simulation import CreateSimulation, DeletedSimulation
from src.services.instance import InstanceService

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_ROUTERS_SIMULATION", "INFO"))

router = APIRouter(default_response_class=ORJSONResponse)


@router.post("/simulation", status_code=201)
async def create_simulation(
    simulation_data: CreateSimulation,
    instance_service: InstanceService = Depends(instance_service),
):
    logger.debug(
        f"Creating simulation {simulation_data.simulation_id}, state: {await instance_service.get_state()}"
    )
    try:
        await instance_service.start_simulation(
            simulation_data.simulation_id,
            simulation_data.agent_code_lines,
            simulation_data.agent_data,
        )
    except SimulationException as e:
        raise HTTPException(400, str(e))


@router.delete("/simulation", response_model=DeletedSimulation, status_code=200)
async def delete_simulation(
    instance_service: InstanceService = Depends(instance_service),
):
    logger.debug(f"Deleting simulation, state: {await instance_service.get_state()}")
    _, simulation_id, _, _ = await instance_service.get_state()
    try:
        await instance_service.kill_simulation()
        return DeletedSimulation(simulation_id=simulation_id)
    except SimulationException as e:
        raise HTTPException(400, str(e))
