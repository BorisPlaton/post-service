from abc import ABC
from abc import abstractmethod
from typing import Any

from shared.message_bus.interface.handler.handler import IMessageHandler
from shared.message_bus.interface.message import IMessage


class IMessageBus[T: IMessage, U: IMessageHandler](ABC):

    @abstractmethod
    def register(
        self,
        message: type[T],
        handler: U,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def handle(
        self,
        message: T,
    ) -> Any:
        raise NotImplementedError()
