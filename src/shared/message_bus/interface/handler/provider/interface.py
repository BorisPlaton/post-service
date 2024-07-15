from abc import ABC
from abc import abstractmethod

from shared.message_bus.interface.handler.handler import IMessageHandler
from shared.message_bus.interface.message import IMessage


class IHandlerProvider[T: IMessage, U: IMessageHandler](ABC):

    @abstractmethod
    def __getitem__(
        self,
        message: type[T],
    ) -> U:
        raise NotImplementedError()

    @abstractmethod
    def __setitem__(
        self,
        message: type[T],
        handler: U,
    ) -> None:
        raise NotImplementedError()
