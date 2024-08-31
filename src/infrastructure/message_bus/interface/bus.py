from abc import ABC
from abc import abstractmethod
from typing import Any

from infrastructure.message_bus.interface.handler import IMessageHandler
from infrastructure.message_bus.interface.message import IMessage


class IMessageBus[T: IMessage, U: IMessageHandler](ABC):

    @abstractmethod
    def register(
        self,
        message: type[T],
        handler: U,
    ) -> None:
        ...

    @abstractmethod
    async def handle(
        self,
        message: T,
    ) -> Any:
        ...
