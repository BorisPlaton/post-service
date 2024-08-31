from abc import ABC

from infrastructure.message_bus.interface.message import IMessage


class IEvent(IMessage, ABC):
    pass
