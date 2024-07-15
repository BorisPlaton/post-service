from asyncio import current_task
from contextlib import asynccontextmanager
from functools import cached_property
from typing import AsyncContextManager

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from shared.database.sqlalchemy.connection.interface import IAsyncSQLAlchemyConnection


class AsyncSQLAlchemyConnection(IAsyncSQLAlchemyConnection):

    def __init__(
        self,
        username: str,
        password: str,
        database: str,
        host: str,
        port: int,
        driver: str,
    ) -> None:
        self._username = username
        self._password = password
        self._database = database
        self._host = host
        self._port = port
        self._driver = driver

    @asynccontextmanager
    async def connect(self) -> AsyncContextManager[AsyncSession]:
        yield self._session()

    @cached_property
    def _engine(self) -> AsyncEngine:
        return create_async_engine(
            URL.create(
                drivername=f"postgresql+{self._driver}",
                username=self._username,
                password=self._password,
                database=self._database,
                host=self._host,
                port=self._port,
            )
        )

    @cached_property
    def _session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self._engine,
            expire_on_commit=True,
        )

    @cached_property
    def _session(self) -> async_scoped_session[AsyncSession]:
        return async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=current_task,
        )
