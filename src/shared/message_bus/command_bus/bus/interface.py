from abc import ABC

from shared.message_bus.command_bus.handler.interface import ICommandHandler
from shared.message_bus.command_bus.command import ICommand
from shared.message_bus.interface.bus import IMessageBus


class ICommandBus(IMessageBus[ICommand, ICommandHandler], ABC):
    pass
