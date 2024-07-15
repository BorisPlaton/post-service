from abc import ABC
from abc import abstractmethod

from shared.message_bus.command_bus.interface.command import ICommand
from shared.message_bus.interface.handler.handler import IMessageHandler


class ICommandHandler[T, U: ICommand](IMessageHandler[U, T], ABC):

    @abstractmethod
    async def __call__(self, message: U) -> T:
        raise NotImplementedError()
