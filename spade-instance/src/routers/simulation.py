from __future__ import annotations

import logging
import os

import orjson
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from src.dependencies.services.requests import (
    graph_creator_service,
    instance_service,
    translator_service,
)
from src.exceptions.graph_creator import GraphNotGeneratedException
from src.exceptions.simulation import SimulationException
from src.exceptions.translator import TranslationException, TranslatorException
from src.models.simulation import CreatedSimulation, CreateSimulation, DeletedSimulation
from src.services.graph_creator import GraphCreatorService
from src.services.instance import InstanceService
from src.services.translator import TranslatorService

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_ROUTERS_SIMULATION", "INFO"))

router = APIRouter(default_response_class=ORJSONResponse)


@router.get("/simulation", status_code=200)
async def get_simulation_state(
    instance_service: InstanceService = Depends(instance_service),
):
    instance_info = await instance_service.get_instance_information()
    return {
        "response": "success",
        "instance_info": instance_info,
        "environment": "local-development",
    }


@router.post("/simulation", response_model=CreatedSimulation, status_code=201)
async def create_simulation(
    simulation_data: CreateSimulation,
    instance_service: InstanceService = Depends(instance_service),
    translator_service: TranslatorService = Depends(translator_service),
    graph_creator_service: GraphCreatorService = Depends(graph_creator_service),
):
    logger.debug(f"Creating simulation, state: {await instance_service.get_state()}")

    if await instance_service.is_simulation_running():
        raise HTTPException(400, "Simulation is already running.")

    try:
        translated_code = await translator_service.translate(
            simulation_data.aasm_code_lines, simulation_data.module_code_lines
        )
    except TranslatorException as e:
        raise HTTPException(500, f"Translator service exception: {str(e)}")
    except TranslationException as e:
        return ORJSONResponse(status_code=400, content=orjson.loads(str(e)))

    try:
        agent_data = graph_creator_service.run_generated_algorithm(
            translated_code.graph_code_lines
        )
    except GraphNotGeneratedException as e:
        raise HTTPException(500, str(e))

    try:
        simulation_id = await instance_service.start_simulation(
            translated_code.agent_code_lines, agent_data
        )
    except SimulationException as e:
        raise HTTPException(400, str(e))

    return CreatedSimulation(simulation_id=simulation_id)


@router.delete("/simulation", response_model=DeletedSimulation, status_code=200)
async def delete_simulation(
    instance_service: InstanceService = Depends(instance_service),
):
    logger.debug(f"Deleting simulation, state: {await instance_service.get_state()}")

    simulation_id = await instance_service.get_simulation_id()
    try:
        await instance_service.kill_simulation()
        return DeletedSimulation(simulation_id=simulation_id)
    except SimulationException as e:
        raise HTTPException(400, str(e))
