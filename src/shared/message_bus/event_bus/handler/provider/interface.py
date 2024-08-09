from abc import ABC
from abc import abstractmethod

from shared.message_bus.event_bus.event import IEvent
from shared.message_bus.event_bus.handler.interface import IEventHandler


class IEventHandlerProvider(ABC):

    @abstractmethod
    def __getitem__(
        self,
        event: type[IEvent],
    ) -> list[IEventHandler]:
        raise NotImplementedError()

    @abstractmethod
    def __setitem__(
        self,
        event: type[IEvent],
        handler: IEventHandler,
    ) -> None:
        raise NotImplementedError()
