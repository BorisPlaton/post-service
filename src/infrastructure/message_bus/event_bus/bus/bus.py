from infrastructure.message_bus.event_bus.bus.interface import IEventBus
from infrastructure.message_bus.event_bus.event import IEvent
from infrastructure.message_bus.event_bus.handler.interface import IEventHandler
from infrastructure.message_bus.event_bus.handler.provider.interface import IEventHandlerProvider


class EventBus(IEventBus):

    def __init__(
        self,
        handler_provider: IEventHandlerProvider,
    ) -> None:
        self._handler_provider = handler_provider

    def register(
        self,
        message: type[IEvent],
        handler: IEventHandler,
    ) -> None:
        self._handler_provider[message] = handler

    async def handle(
        self,
        message: IEvent,
    ) -> None:
        for handler in self._handler_provider[message.__class__]:
            await handler(message=message)
