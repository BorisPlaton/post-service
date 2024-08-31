from datetime import timedelta
from typing import Any

from rq import Queue

from infrastructure.database.sqlalchemy.transcation.interface import ITransactionManager
from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.command_bus.config.mixin.interface import IConfigurableCommand
from infrastructure.message_bus.command_bus.config.options.background import BackgroundExecutionOption
from infrastructure.message_bus.command_bus.config.options.transactional import TransactionalOption
from infrastructure.message_bus.command_bus.handler.executor.interface import ICommandHandlerExecutor
from infrastructure.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from infrastructure.redis_.client.interface import IRedisClient


class CommandHandlerExecutor(ICommandHandlerExecutor):

    def __init__(
        self,
        handler_provider: ICommandHandlerProvider,
        transaction_manager: ITransactionManager,
        redis_client: IRedisClient,
    ):
        self._transaction_manager = transaction_manager
        self._handler_provider = handler_provider
        self._queue = Queue(connection=redis_client.client)

    async def __call__(
        self,
        command: ICommand,
    ) -> Any:
        handler = self._handler_provider[command.__class__]

        # TODO: Refactor it. Executor doesn't have to know about what
        #  options do.

        if isinstance(command, IConfigurableCommand):
            # ===== BackgroundOption
            if background_option := command.command_config.get(BackgroundExecutionOption):
                if background_option.is_background and command.context.get("background_execution") is not True:
                    command.context = {
                        "background_execution": True,
                    }
                    # TODO: Add check for enqueue_in option
                    # TODO: Add background execution with background worker and message broker
                    # self._queue.enqueue_in()
                    return

            # ===== TransactionalOption
            start_transaction = True
            if transaction_option := command.command_config.get(TransactionalOption):
                start_transaction = transaction_option.is_transactional
            if start_transaction:
                async with self._transaction_manager.begin():
                    return await handler(command)

        return await handler(command)
