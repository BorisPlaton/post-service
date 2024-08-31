from abc import ABC, abstractmethod


class IConsumer(ABC):

    @abstractmethod
    async def consume(self): ...
