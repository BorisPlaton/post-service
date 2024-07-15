from abc import ABC
from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession


class IAsyncSQLAlchemyConnection(ABC):

    @abstractmethod
    @asynccontextmanager
    async def connect(self) -> AsyncContextManager[AsyncSession]:
        raise NotImplementedError()
