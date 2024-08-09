from punq import Container

from settings.config.database import DatabaseSettings
from settings.config.redis import RedisSettings
from shared.database.sqlalchemy.transcation.interface import ITransactionManager
from shared.database.sqlalchemy.transcation.manager import TransactionManager
from shared.message_bus.command_bus.bus.bus import CommandBus
from shared.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from shared.message_bus.command_bus.handler.provider.provider import CommandHandlerProvider
from shared.message_bus.command_bus.middleware.transaction import TransactionMiddleware
from shared.message_bus.event_bus.bus.bus import EventBus
from shared.message_bus.event_bus.bus.interface import IEventBus
from shared.message_bus.event_bus.handler.provider.interface import IEventHandlerProvider
from shared.message_bus.event_bus.handler.provider.provider import EventHandlerProvider
from shared.module_setup.module import IModule
from shared.database.sqlalchemy.connection.async_connection import AsyncSQLAlchemyConnectionManager
from shared.database.sqlalchemy.connection.interface import IAsyncSQLAlchemyConnectionManager
from shared.message_bus.command_bus.bus.interface import ICommandBus
from shared.redis_.client.client import RedisClient
from shared.redis_.client.interface import IRedisClient


class SharedModule(IModule):

    def configure(
        self,
        container: Container,
    ) -> None:
        db_settings: DatabaseSettings = container.resolve(DatabaseSettings)

        container.register(
            service=IAsyncSQLAlchemyConnectionManager,
            instance=AsyncSQLAlchemyConnectionManager(
                host=db_settings.HOST,
                port=db_settings.PORT,
                database=db_settings.DATABASE,
                username=db_settings.USERNAME,
                password=db_settings.PASSWORD,
                driver=db_settings.driver,
            ),
        )
        container.register(
            service=ITransactionManager,
            instance=TransactionManager(
                connection_manager=container.resolve(IAsyncSQLAlchemyConnectionManager),
            )
        )

        container.register(
            service=ICommandHandlerProvider,
            instance=CommandHandlerProvider(),
        )
        container.register(
            service=ICommandBus,
            instance=CommandBus(
                handler_provider=container.resolve(ICommandHandlerProvider),
                middlewares=[
                    TransactionMiddleware(
                        transaction_manager=container.resolve(ITransactionManager),
                        handler_provider=container.resolve(ICommandHandlerProvider),
                    ),
                ],
            )
        )

        container.register(
            service=IEventHandlerProvider,
            instance=EventHandlerProvider(),
        )
        container.register(
            service=IEventBus,
            instance=EventBus(
                handler_provider=container.resolve(IEventHandlerProvider),
            ),
        )

        container.register(
            service=IRedisClient,
            instance=RedisClient(
                settings=container.resolve(RedisSettings),
            ),
        )
