from abc import ABC
from dataclasses import dataclass

from infrastructure.message_bus.interface.message import IMessage


@dataclass(slots=True, kw_only=True)
class ICommand[U: dict](IMessage, ABC):
    pass
