from abc import ABC
from abc import abstractmethod
from functools import cached_property
from typing import Any

from sqlalchemy import ScalarResult
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.database.repository.interface import IAsyncCRUDRepository
from shared.database.sqlalchemy.connection.async_connection import AsyncSQLAlchemyConnection
from shared.database.sqlalchemy.mixins import IdMixin


class AsyncSQLAlchemyRepository[T, U: IdMixin](
    IAsyncCRUDRepository,
    ABC,
):

    def __init__(
        self,
        async_connection: AsyncSQLAlchemyConnection,
    ) -> None:
        self._conn_provider = async_connection

    async def get(self, id_: T) -> U:
        statement = select(
            self.entity_class
        ).where(
            self.entity_class.id == id_,
        ).execution_options(
            populate_existing=True,
        ).options(
            selectinload('*'),
        )
        return await self.scalar(statement)

    async def get_by_ids(self, ids: list[T]) -> U:
        statement = select(
            self.entity_class
        ).where(
            self.entity_class.id.in_(ids),
        ).execution_options(
            populate_existing=True,
        ).options(
            selectinload('*'),
        )
        return await self.scalars(statement)

    async def get_all(self) -> list[U]:
        statement = select(
            self.entity_class
        ).execution_options(
            populate_existing=True,
        ).options(
            selectinload('*'),
        )
        return await self.scalars(statement)

    async def get_all_by_filter(
        self,
        filter_,
    ) -> list[U]:
        statement = select(
            self.entity_class
        ).execution_options(
            populate_existing=True,
        ).where(
            filter_,
        ).options(
            selectinload('*'),
        )
        return await self.scalars(statement)

    async def delete(self, entity: U) -> None:
        async with self._conn_provider.connect() as session:
            await session.delete(entity)
            await session.flush()

    async def update(self, entity: U) -> None:
        async with self._conn_provider.connect() as session:
            session.add(entity)
            await session.flush()

    async def update_many(self, entities: list[U]) -> None:
        async with self._conn_provider.connect() as session:
            session.add_all(entities)
            await session.flush()

    async def create(self, entity: U) -> None:
        async with self._conn_provider.connect() as session:
            session.add(entity)
            await session.flush()

    async def scalars(self, *args, **kwargs) -> list[U]:
        async with self._conn_provider.connect() as session:
            session: AsyncSession
            return (await session.scalars(*args, **kwargs)).all()

    async def scalar(self, *args, **kwargs) -> U:
        async with self._conn_provider.connect() as session:
            session: AsyncSession
            return (await session.scalar(*args, **kwargs)).first()

    async def execute(self, *args, **kwargs) -> Any:
        async with self._conn_provider.connect() as session:
            session: AsyncSession
            return await session.execute(*args, **kwargs)

    @cached_property
    @abstractmethod
    def entity_class(self) -> type[U]:
        raise NotImplementedError()
