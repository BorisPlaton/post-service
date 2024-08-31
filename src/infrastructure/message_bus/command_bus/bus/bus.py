from typing import Any
from typing import Awaitable
from typing import Callable

from infrastructure.message_bus.command_bus.bus.interface import ICommandBus
from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.command_bus.handler.executor.interface import ICommandHandlerExecutor
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler
from infrastructure.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from infrastructure.message_bus.command_bus.middleware.interface import ICommandBusMiddleware


class CommandBus(ICommandBus):

    def __init__(
        self,
        middlewares: list[ICommandBusMiddleware],
        handler_provider: ICommandHandlerProvider,
        handler_executor: ICommandHandlerExecutor,
    ) -> None:
        self._handler_provider = handler_provider
        self._handler_executor = handler_executor
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
            return await self._handler_executor(
                command=message,
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
