from shared.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from shared.message_bus.interface.handler.provider.provider import BaseHandlerProvider


class CommandHandlerProvider(BaseHandlerProvider, ICommandHandlerProvider):
    pass
