from collections import defaultdict

from infrastructure.message_bus.event_bus.event import IEvent
from infrastructure.message_bus.event_bus.handler.interface import IEventHandler
from infrastructure.message_bus.event_bus.handler.provider.interface import IEventHandlerProvider


class EventHandlerProvider(IEventHandlerProvider):

    def __init__(self):
        self._event_handler_map: dict[type[IEvent], list[IEventHandler]] = defaultdict(list)

    def __getitem__(
        self,
        event: type[IEvent],
    ) -> list[IEventHandler]:
        return self._event_handler_map[event]

    def __setitem__(
        self,
        event: type[IEvent],
        handler: IEventHandler,
    ) -> None:
        return self._event_handler_map[event].append(handler)
