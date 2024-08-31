from abc import ABC
from abc import abstractmethod

from infrastructure.message_bus.event_bus.event import IEvent
from infrastructure.message_bus.event_bus.handler.interface import IEventHandler


class IEventHandlerProvider(ABC):

    @abstractmethod
    def __getitem__(
        self,
        event: type[IEvent],
    ) -> list[IEventHandler]:
        ...

    @abstractmethod
    def __setitem__(
        self,
        event: type[IEvent],
        handler: IEventHandler,
    ) -> None:
        ...
