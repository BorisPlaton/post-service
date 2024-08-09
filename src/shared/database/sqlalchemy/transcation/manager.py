from contextlib import asynccontextmanager

from shared.database.sqlalchemy.connection.async_connection import AsyncSQLAlchemyConnectionManager
from shared.database.sqlalchemy.transcation.interface import ITransactionManager


class TransactionManager(ITransactionManager):

    def __init__(
        self,
        connection_manager: AsyncSQLAlchemyConnectionManager,
    ):
        self._connection_manager = connection_manager

    @asynccontextmanager
    async def begin(self) -> None:
        explicit_transaction_key = 'explicit_transaction'

        async with self._connection_manager.connect() as connection:
            info: dict = connection.info
            explicit_transaction = info.get(explicit_transaction_key, False)
            info[explicit_transaction_key] = True

            try:
                if not (connection.in_transaction() or explicit_transaction):
                    await connection.begin()
                yield
            except Exception as e:
                await connection.rollback()
                raise e

            if connection.in_transaction() and not explicit_transaction:
                await connection.commit()
