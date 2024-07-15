from punq import Container

from settings.config.database import DatabaseSettings
from shared.message_bus.command_bus.handler.provider.interface import ICommandHandlerProvider
from shared.message_bus.command_bus.handler.provider.provider import CommandHandlerProvider
from shared.message_bus.command_bus.middleware.transaction import TransactionMiddleware
from shared.module_setup.module import IModule
from shared.database.sqlalchemy.connection.async_connection import AsyncSQLAlchemyConnection
from shared.database.sqlalchemy.connection.interface import IAsyncSQLAlchemyConnection
from shared.message_bus.command_bus.bus import CommandBus
from shared.message_bus.command_bus.interface.bus import ICommandBus


class SharedModule(IModule):

    def configure(
        self,
        container: Container,
    ) -> None:
        db_settings: DatabaseSettings = container.resolve(DatabaseSettings)

        container.register(
            service=IAsyncSQLAlchemyConnection,
            instance=AsyncSQLAlchemyConnection(
                host=db_settings.HOST,
                port=db_settings.PORT,
                database=db_settings.DATABASE,
                username=db_settings.USERNAME,
                password=db_settings.PASSWORD,
                driver=db_settings.driver,
            ),
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
                        connection=container.resolve(IAsyncSQLAlchemyConnection),
                        handler_provider=container.resolve(ICommandHandlerProvider),
                    ),
                ],
            )
        )
