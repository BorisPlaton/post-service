from abc import ABC
from abc import abstractmethod

from shared.message_bus.command_bus.command import ICommand
from shared.message_bus.command_bus.handler.interface import ICommandHandler


class ICommandHandlerProvider(ABC):

    @abstractmethod
    def __getitem__(
        self,
        command: type[ICommand],
    ) -> ICommandHandler:
        raise NotImplementedError()

    @abstractmethod
    def __setitem__(
        self,
        message: type[ICommand],
        handler: ICommandHandler,
    ) -> None:
        raise NotImplementedError()
