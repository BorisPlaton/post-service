from abc import ABC
from abc import abstractmethod
from contextlib import asynccontextmanager


class ITransactionManager(ABC):

    @abstractmethod
    @asynccontextmanager
    async def begin(self) -> None: ...
