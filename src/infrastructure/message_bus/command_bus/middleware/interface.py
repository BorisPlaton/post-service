from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Awaitable
from typing import Callable

from infrastructure.message_bus.command_bus.command import ICommand


class ICommandBusMiddleware[T](ABC):

    @abstractmethod
    async def handle(
        self,
        message: ICommand,
        next_: Callable[[ICommand], Awaitable[Any]],
    ) -> T:
        ...
