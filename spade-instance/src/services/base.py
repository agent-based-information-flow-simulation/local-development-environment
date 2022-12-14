from __future__ import annotations

from typing import TYPE_CHECKING

from src.database.repositories.base import BaseRepository

if TYPE_CHECKING:
    from typing import Type

    from src.instance.state import State


class BaseService:
    def __init__(self) -> None:
        ...


class BaseServiceWithRepository(BaseService):
    repository_type: Type[BaseRepository] = BaseRepository

    def __init__(self, repository: BaseRepository) -> None:
        super().__init__()
        self._repository = repository

    @property
    def repository(self) -> repository_type:
        ...


class BaseServiceWithState(BaseService):
    def __init__(self, state: State) -> None:
        super().__init__()
        self._state = state

    @property
    def state(self) -> State:
        ...
