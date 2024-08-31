from abc import ABC
from abc import abstractmethod

from infrastructure.message_bus.event_bus.event import IEvent
from infrastructure.message_bus.interface.handler import IMessageHandler


class IEventHandler[U: IEvent](IMessageHandler[U, None], ABC):

    @abstractmethod
    async def __call__(
        self,
        message: U,
    ) -> None:
        ...
