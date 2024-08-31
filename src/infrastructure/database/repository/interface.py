from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Iterable

from sqlalchemy import ScalarResult


class IAsyncCRUDRepository[T, U](ABC):

    @abstractmethod
    async def get(
        self,
        id_: T,
    ) -> U:
        ...

    @abstractmethod
    async def get_by_ids(
        self,
        ids: list[T],
        order_by: Iterable[Any] | None = None,
    ) -> U:
        ...

    @abstractmethod
    async def get_all(
        self,
        order_by: Iterable[Any] | None = None,
    ) -> list[U]:
        ...

    @abstractmethod
    async def get_all_by_filter(
        self,
        filter_: Any,
        order_by: Iterable[Any] | None = None,
    ) -> list[U]:
        ...

    @abstractmethod
    async def delete(
        self,
        entity: U,
    ) -> None:
        ...

    @abstractmethod
    async def update(
        self,
        entity: U,
    ) -> None:
        ...

    @abstractmethod
    async def update_many(
        self,
        entities: list[U],
    ) -> None:
        ...

    @abstractmethod
    async def create(
        self,
        entity: U,
    ) -> None:
        ...

    @abstractmethod
    async def scalars(
        self,
        *args,
        **kwargs,
    ) -> ScalarResult:
        ...

    @abstractmethod
    async def scalar(
        self,
        *args,
        **kwargs,
    ) -> ScalarResult:
        ...

    @abstractmethod
    async def execute(
        self,
        *args,
        **kwargs,
    ) -> Any:
        ...
