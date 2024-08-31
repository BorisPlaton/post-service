from punq import Container

from infrastructure.settings.ai import AISettings
from infrastructure.settings.app import ApplicationSettings
from infrastructure.settings.database import DatabaseSettings
from infrastructure.settings.redis import RedisSettings
from infrastructure.database.sqlalchemy.transcation.interface import ITransactionManager
from infrastructure.database.sqlalchemy.transcation.manager import TransactionManager
from infrastructure.message_bus.command_bus.bus.bus import CommandBus
from infrastructure.message_bus.command_bus.handler.executor.executor import CommandHandlerExecutor
from infrastructure.message_bus.command_bus.handler.executor.interface import ICommandHandlerExecutor
from infrastructure.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from infrastructure.message_bus.command_bus.handler.provider.provider import CommandHandlerProvider
from infrastructure.message_bus.event_bus.bus.bus import EventBus
from infrastructure.message_bus.event_bus.bus.interface import IEventBus
from infrastructure.message_bus.event_bus.handler.provider.interface import IEventHandlerProvider
from infrastructure.message_bus.event_bus.handler.provider.provider import EventHandlerProvider
from infrastructure.module_setup.interface import IModule
from infrastructure.database.sqlalchemy.connection.async_connection import AsyncSQLAlchemyConnectionManager
from infrastructure.database.sqlalchemy.connection.interface import IAsyncSQLAlchemyConnectionManager
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus
from infrastructure.redis_.client.client import RedisClient
from infrastructure.redis_.client.interface import IRedisClient


class InfrastructureModule(IModule):

    def configure(
        self,
        container: Container,
    ) -> None:
        db_settings: DatabaseSettings = container.resolve(DatabaseSettings)

        container.register(
            service=DatabaseSettings,
            instance=DatabaseSettings(),
        )
        container.register(
            service=ApplicationSettings,
            instance=ApplicationSettings(),
        )
        container.register(
            service=AISettings,
            instance=AISettings(),
        )
        container.register(
            service=RedisSettings,
            instance=RedisSettings(),
        )

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

        container.register(
            service=ICommandHandlerProvider,
            instance=CommandHandlerProvider(),
        )
        container.register(
            service=ICommandHandlerExecutor,
            instance=CommandHandlerExecutor(
                handler_provider=container.resolve(ICommandHandlerProvider),
                transaction_manager=container.resolve(ITransactionManager),
                redis_client=container.resolve(IRedisClient),
            ),
        )
        container.register(
            service=ICommandBus,
            instance=CommandBus(
                handler_provider=container.resolve(ICommandHandlerProvider),
                handler_executor=container.resolve(ICommandHandlerExecutor),
                middlewares=[],
            )
        )

