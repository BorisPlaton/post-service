from abc import ABC

from shared.message_bus.command_bus.handler.handler import ICommandHandler
from shared.message_bus.command_bus.interface.command import ICommand
from shared.message_bus.interface.handler.provider.interface import IHandlerProvider


class ICommandHandlerProvider(IHandlerProvider[ICommand, ICommandHandler], ABC):
    pass
