from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from src.dependencies.services.requests import instance_service
from src.services.instance import InstanceService

router = APIRouter(default_response_class=ORJSONResponse)


@router.get("/health", status_code=200)
async def healthcheck(instance_service: InstanceService = Depends(instance_service)):
    instance_info = await instance_service.get_instance_information()
    return {"response": "success", "instance_info": instance_info}
