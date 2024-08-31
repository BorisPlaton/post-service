from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler
from infrastructure.message_bus.command_bus.handler.provider.exception.no_command_handler_found import \
    NoCommandHandlerFoundException
from infrastructure.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider


class CommandHandlerProvider(ICommandHandlerProvider):
    def __init__(self):
        self._message_handler_map: dict[type[ICommand], ICommandHandler] = {}

    def __getitem__(
        self,
        command: type[ICommand],
    ) -> ICommandHandler:
        if not (handler := self._message_handler_map.get(command)):
            raise NoCommandHandlerFoundException()

        return handler

    def __setitem__(
        self,
        message: type[ICommand],
        handler: ICommandHandler,
    ) -> None:
        self._message_handler_map[message] = handler

