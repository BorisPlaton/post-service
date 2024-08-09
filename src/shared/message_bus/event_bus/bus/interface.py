from abc import ABC

from shared.message_bus.event_bus.event import IEvent
from shared.message_bus.event_bus.handler.interface import IEventHandler
from shared.message_bus.interface.bus import IMessageBus


class IEventBus(IMessageBus[IEvent, IEventHandler], ABC):
    pass
