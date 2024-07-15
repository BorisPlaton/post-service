from typing import Any
from typing import Awaitable
from typing import Callable

from shared.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from shared.message_bus.command_bus.interface.bus import ICommandBus
from shared.message_bus.command_bus.interface.command import ICommand
from shared.message_bus.command_bus.handler.handler import ICommandHandler
from shared.message_bus.command_bus.interface.middleware import ICommandBusMiddleware


class CommandBus(ICommandBus):

    def __init__(
        self,
        middlewares: list[ICommandBusMiddleware],
        handler_provider: ICommandHandlerProvider,
    ) -> None:
        self._handler_provider = handler_provider
        self._middlewares = middlewares
        self._middleware_chain = self._build_middlewares()

    def register(
        self,
        message: type[ICommand],
        handler: ICommandHandler,
    ) -> None:
        self._handler_provider[message] = handler

    async def handle(
        self,
        message: ICommand,
    ) -> Any:
        return await self._middleware_chain(message)

    def _build_middlewares(self) -> Callable[[ICommand], Awaitable[Any]]:
        async def command_executor(message: ICommand) -> None:
            return await self._handler_provider[message.__class__](
                message=message,
            )

        def wrapped_middleware(
            mdl: ICommandBusMiddleware,
            next_handler: Callable[[ICommand], Awaitable[Any]],
        ) -> Callable[[ICommand], Awaitable[Any]]:
            async def wrapped_handler(message: ICommand) -> Any:
                return await mdl.handle(
                    message=message,
                    next_=next_handler,
                )

            return wrapped_handler

        for middleware in self._middlewares[::-1]:
            command_executor = wrapped_middleware(
                mdl=middleware,
                next_handler=command_executor,
            )

        return command_executor
