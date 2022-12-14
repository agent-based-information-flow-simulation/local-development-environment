from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse, StreamingResponse

from src.dependencies.services.requests import timeseries_service
from src.exceptions.timeseries import TimeseriesDoesNotExistException
from src.services.timeseries import TimeseriesService

router = APIRouter(prefix="/simulations", default_response_class=ORJSONResponse)


@router.get("/{simulation_id}/timeseries")
async def get_timeseries(
    simulation_id: str,
    timeseries_service: TimeseriesService = Depends(timeseries_service),
):
    try:
        db_cursor_wrapper = await timeseries_service.get_timeseries(simulation_id)
    except TimeseriesDoesNotExistException as e:
        raise HTTPException(400, str(e))

    return StreamingResponse(
        db_cursor_wrapper.stream(chunk_size_bytes=1024 * 512),
        media_type="application/json",
        headers={
            "Access-Control-Expose-Headers": "Content-Disposition",
            "Content-Disposition": f"attachment;filename=timeseries_{simulation_id}.json",
        },
    )


@router.delete("/{simulation_id}/timeseries")
async def delete_timeseries(
    simulation_id: str,
    timeseries_service: TimeseriesService = Depends(timeseries_service),
):
    try:
        num_deleted = await timeseries_service.delete_timeseries(simulation_id)
    except TimeseriesDoesNotExistException as e:
        raise HTTPException(400, str(e))

    return {"num_deleted": num_deleted}


@router.get("/timeseries/ids")
async def get_all_timeseries_ids(
    timeseries_service: TimeseriesService = Depends(timeseries_service),
):
    ids = await timeseries_service.get_all_timeseries_ids()
    return {"ids": ids}
