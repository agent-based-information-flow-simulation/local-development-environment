from __future__ import annotations

from typing import TYPE_CHECKING

from src.services.agent_updates import AgentUpdatesService

from src.services.graph_creator import GraphCreatorService
from src.services.instance import InstanceService
from src.services.timeseries import TimeseriesService
from src.services.translator import TranslatorService

from src.dependencies.injection import get_service, get_service_without_request

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable, Coroutine

    from fastapi import FastAPI


timeseries_service: Callable[[], TimeseriesService] = get_service(TimeseriesService)
instance_service: Callable[[], InstanceService] = get_service(InstanceService)
translator_service: Callable[[], TranslatorService] = get_service(TranslatorService)
graph_creator_service: Callable[[], GraphCreatorService] = get_service(
    GraphCreatorService
)
agent_updates: Callable[
    [FastAPI], Coroutine[Any, Any, AgentUpdatesService]
] = get_service_without_request(AgentUpdatesService)
