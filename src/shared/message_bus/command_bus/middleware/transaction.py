from typing import Any
from typing import Awaitable
from typing import Callable

from shared.database.sqlalchemy.connection.interface import IAsyncSQLAlchemyConnection
from shared.database.sqlalchemy.transcation.manager import TransactionManager
from shared.message_bus.command_bus.config.mixin import IConfigurableCommand
from shared.message_bus.command_bus.config.options.transactional import TransactionalOption
from shared.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from shared.message_bus.command_bus.interface.command import ICommand
from shared.message_bus.command_bus.interface.middleware import ICommandBusMiddleware


class TransactionMiddleware(ICommandBusMiddleware):

    def __init__(
        self,
        handler_provider: ICommandHandlerProvider,
        connection: IAsyncSQLAlchemyConnection,
    ):
        self._connection = connection
        self._handler_provider = handler_provider

    async def handle(
        self,
        message: ICommand,
        next_: Callable[[ICommand], Awaitable[Any]],
    ) -> Any:
        handler = self._handler_provider[message.__class__]
        start_transaction = True

        if isinstance(handler, IConfigurableCommand):
            if transaction_option := handler.config.get(TransactionalOption):
                start_transaction = transaction_option.is_transactional

        if start_transaction:
            async with self._connection.connect() as session:
                async with TransactionManager().begin(session):
                    return await next_(message)
        else:
            return await next_(message)

