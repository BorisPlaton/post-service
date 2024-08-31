from abc import ABC
from abc import abstractmethod

from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler


class ICommandHandlerProvider(ABC):

    @abstractmethod
    def __getitem__(
        self,
        command: type[ICommand],
    ) -> ICommandHandler:
        ...

    @abstractmethod
    def __setitem__(
        self,
        message: type[ICommand],
        handler: ICommandHandler,
    ) -> None:
        ...
