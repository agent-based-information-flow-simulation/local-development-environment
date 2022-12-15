from __future__ import annotations

from typing import TYPE_CHECKING

from src.services.graph_creator import GraphCreatorService
from src.services.instance import InstanceService
from src.services.timeseries import TimeseriesService
from src.services.translator import TranslatorService

from src.dependencies.injection import get_service

if TYPE_CHECKING:  # pragma: no cover
    from typing import Callable




timeseries_service: Callable[[], TimeseriesService] = get_service(TimeseriesService)
instance_service: Callable[[], InstanceService] = get_service(InstanceService)
translator_service: Callable[[], TranslatorService] = get_service(TranslatorService)
graph_creator_service: Callable[[], GraphCreatorService] = get_service(
    GraphCreatorService
)
