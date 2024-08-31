from abc import ABC
from abc import abstractmethod
from typing import Any

from infrastructure.message_bus.command_bus.command import ICommand


class ICommandHandlerExecutor(ABC):

    @abstractmethod
    async def __call__(
        self,
        command: ICommand,
    ) -> Any:
        ...
