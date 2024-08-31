from abc import ABC

from infrastructure.message_bus.event_bus.event import IEvent
from infrastructure.message_bus.event_bus.handler.interface import IEventHandler
from infrastructure.message_bus.interface.bus import IMessageBus


class IEventBus(IMessageBus[IEvent, IEventHandler], ABC):
    pass
