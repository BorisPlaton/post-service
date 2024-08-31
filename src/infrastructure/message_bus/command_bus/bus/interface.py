from abc import ABC

from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler
from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.interface.bus import IMessageBus


class ICommandBus(IMessageBus[ICommand, ICommandHandler], ABC):
    pass
