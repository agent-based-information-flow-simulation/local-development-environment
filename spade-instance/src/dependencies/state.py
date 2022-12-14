from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.requests import Request

from src.instance.state import State, get_app_simulation_state

if TYPE_CHECKING:  # pragma: no cover
    from typing import Callable


def get_simulation_state() -> Callable[[Request], State]:
    def _get_simulation_state(request: Request) -> State:
        return get_app_simulation_state(request.app)

    return _get_simulation_state


state: Callable[[Request], State] = get_simulation_state()
