from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from pymongo import ASCENDING
from pymongo.errors import CollectionInvalid

from src.database.connection import get_app_db

if TYPE_CHECKING: # pragma: no cover
    from typing import Callable

    from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_DB", "INFO"))


def create_startup_db_collection_creator(
    app: FastAPI,
) -> Callable[[], None]:
    async def create_collection() -> None:
        collection_name = "agents"
        logger.info(f"Creating collection '{collection_name}'")
        db = get_app_db(app)
        try:
            collection = await db.create_collection(
                collection_name,
                timeseries={"timeField": "timestamp", "metaField": "metadata"},
            )
            logger.info(f"Collection '{collection_name}' created")
        except CollectionInvalid:
            logger.info(f"Collection '{collection_name}' already exists")
            return
        logger.info(f"Creating indexes for the collection '{collection_name}'")
        await collection.create_index(
            [
                ("timestamp", ASCENDING),
                ("metadata.jid", ASCENDING),
                ("metadata.simulation_id", ASCENDING),
            ]
        )
        logger.info(f"Created indexes for the collection '{collection_name}'")

    return create_collection
