from __future__ import annotations

from typing import TYPE_CHECKING

from src.services.agent_updates import AgentUpdatesService
from src.services.instance import InstanceService

from src.dependencies.injection import get_service_without_request

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable, Coroutine

    from fastapi import FastAPI

agent_updates_service: Callable[
    [FastAPI], Coroutine[Any, Any, AgentUpdatesService]
] = get_service_without_request(AgentUpdatesService)
instance_service: Callable[
    [FastAPI], Coroutine[Any, Any, InstanceService]
] = get_service_without_request(InstanceService)
