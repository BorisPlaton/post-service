from shared.message_bus.interface.handler.exception.no_handler_found import NoMessageHandlersFound
from shared.message_bus.interface.handler.handler import IMessageHandler
from shared.message_bus.interface.handler.provider.interface import IHandlerProvider
from shared.message_bus.interface.message import IMessage


class BaseHandlerProvider[T: IMessage, U: IMessageHandler](IHandlerProvider):

    def __init__(self):
        self._message_handler_map: dict[type[T], U] = {}

    def __getitem__(
        self,
        message: type[T],
    ) -> U:
        if not (handler := self._message_handler_map.get(message)):
            raise NoMessageHandlersFound()

        return handler

    def __setitem__(
        self,
        message: type[T],
        handler: U,
    ) -> None:
        self._message_handler_map[message] = handler
