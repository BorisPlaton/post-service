from infrastructure.message_bus.command_bus.exception import CommandBusException


class NoCommandHandlerFoundException(CommandBusException):

    def __init__(self):
        super().__init__("No command handler found for the command.")
