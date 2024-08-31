from abc import ABC
from abc import abstractmethod

from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.interface.handler import IMessageHandler


class ICommandHandler[U: ICommand, T](IMessageHandler[U, T], ABC):

    @abstractmethod
    async def __call__(self, message: U) -> T:
        raise NotImplementedError()
