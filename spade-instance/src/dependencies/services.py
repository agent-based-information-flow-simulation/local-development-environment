from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection

from src.database.connection import (
    get_app_db,
    get_app_db_client,
    get_collection,
    get_session_from_db_pool,
)
from src.database.repositories.base import BaseRepository
from src.instance.state import State, get_app_simulation_state, get_simulation_state
from src.services.base import (
    BaseService,
    BaseServiceWithRepository,
    BaseServiceWithState,
)
from src.services.instance import InstanceService
from src.services.timeseries import TimeseriesService

if TYPE_CHECKING:  # pragma: no cover
    from typing import Callable, Type

    from fastapi import FastAPI


def get_repository(
    repository_type: Type[BaseRepository],
) -> Callable[[AsyncIOMotorClientSession], BaseRepository]:
    def _get_repository(
        session: AsyncIOMotorClientSession = Depends(get_session_from_db_pool),
        collection: AsyncIOMotorCollection = Depends(
            get_collection(repository_type.collection_name)
        ),
    ) -> BaseRepository:
        return repository_type(session, collection)

    return _get_repository


def get_service(
    service_type: Type[BaseService],
) -> Callable[[BaseRepository], BaseService]:
    if issubclass(service_type, BaseServiceWithRepository):

        def _get_service_with_repository(
            repository: BaseRepository = Depends(
                get_repository(service_type.repository_type)
            ),
        ) -> BaseService:
            return service_type(repository)

        return _get_service_with_repository

    elif issubclass(service_type, BaseServiceWithState):

        def _get_service_with_state(
            state: State = Depends(get_simulation_state()),
        ) -> BaseService:
            return service_type(state)

        return _get_service_with_state

    else:
        return service_type()


async def get_service_without_request(
    app: FastAPI, service_type: Type[BaseService]
) -> BaseService:
    if issubclass(service_type, BaseServiceWithRepository):
        db = get_app_db(app)
        collection = get_collection(service_type.repository_type.collection_name)(db)
        db_client = get_app_db_client(app)
        session = await get_session_from_db_pool(db_client)
        repository = get_repository(service_type.repository_type)(session, collection)
        return service_type(repository)

    elif issubclass(service_type, BaseServiceWithState):
        state = get_app_simulation_state(app)
        return service_type(state)

    else:
        return service_type()


timeseries_service: Callable[[], TimeseriesService] = get_service(TimeseriesService)
instance_service: Callable[[], InstanceService] = get_service(InstanceService)
