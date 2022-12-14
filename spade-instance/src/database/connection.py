from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from fastapi import Depends
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from starlette.requests import Request

from src.exceptions.database import CollectionDoesNotExistException
from src.settings.database import database_settings

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, AsyncGenerator, Callable, Coroutine

    from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_DB", "INFO"))


def set_app_db_client(app: FastAPI, db_client: AsyncIOMotorClient) -> None:
    app.state.db_client = db_client


def get_app_db_client(app: FastAPI) -> AsyncIOMotorClient:
    return app.state.db_client


def get_db_client() -> Callable[[Request], AsyncIOMotorClient]:
    def _get_db_client(request: Request) -> AsyncIOMotorClient:
        return get_app_db_client(request.app)

    return _get_db_client


def set_app_db(app: FastAPI, db: AsyncIOMotorDatabase) -> None:
    app.state.db = db


def get_app_db(app: FastAPI) -> AsyncIOMotorDatabase:
    return app.state.db


def get_db() -> Callable[[Request], AsyncIOMotorDatabase]:
    def _get_db(request: Request) -> AsyncIOMotorDatabase:
        return get_app_db(request.app)

    return _get_db


async def get_session_from_db_pool(
    db_client: AsyncIOMotorClient = Depends(get_db),
) -> AsyncGenerator[AsyncIOMotorClientSession, None, None]:
    async with await db_client.start_session() as session:
        yield session


def get_collection(
    collection_name: str,
) -> Callable[[AsyncIOMotorDatabase], Coroutine[Any, Any, AsyncIOMotorCollection]]:
    async def _get_collection(
        db: AsyncIOMotorDatabase = Depends(get_db),
    ) -> AsyncIOMotorCollection:
        if collection_name not in await db.list_collection_names():
            raise CollectionDoesNotExistException(collection_name)
        return db[collection_name]

    return _get_collection


def create_startup_db_connection_handler(
    app: FastAPI,
) -> Callable[[], None]:
    def connect() -> None:
        logger.info("Connecting to the database")
        set_app_db_client(app, AsyncIOMotorClient(database_settings.url))
        logger.info("Connected to the database")

    return connect


def create_shutdown_db_connection_handler(
    app: FastAPI,
) -> Callable[[], None]:
    def disconnect() -> None:
        logger.info("Disconnecting from the database")
        get_app_db_client(app).close()
        logger.info("Disconnected from the database")

    return disconnect


def create_startup_db_access_handler(
    app: FastAPI,
) -> Callable[[], None]:
    def access_db() -> None:
        logger.info("Accessing the database")
        set_app_db(app, get_app_db_client(app).get_database("simulations"))
        logger.info("Accessed the database")

    return access_db
