from abc import ABC
from abc import abstractmethod

from infrastructure.message_bus.interface.message import IMessage


class IMessageHandler[T: IMessage, U](ABC):

    @abstractmethod
    async def __call__(self, message: T) -> U:
        raise NotImplementedError()
