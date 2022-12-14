from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
async def healthcheck():
    return {"response": "success"}
