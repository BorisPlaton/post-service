from abc import ABC

from shared.message_bus.interface.message import IMessage


class IEvent(IMessage, ABC):
    pass
