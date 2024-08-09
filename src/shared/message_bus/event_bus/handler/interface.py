from abc import ABC
from abc import abstractmethod

from shared.message_bus.event_bus.event import IEvent
from shared.message_bus.interface.handler import IMessageHandler


class IEventHandler[U: IEvent](IMessageHandler[U, None], ABC):

    @abstractmethod
    async def __call__(self, message: U) -> None:
        raise NotImplementedError()
