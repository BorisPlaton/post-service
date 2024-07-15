from abc import ABC
from abc import abstractmethod
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession


class ITransactionManager(ABC):

    @abstractmethod
    @asynccontextmanager
    async def begin(
        self,
        session: AsyncSession,
    ) -> None:
        raise NotImplementedError()
