from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.sqlalchemy.transcation.interface import ITransactionManager


class TransactionManager(ITransactionManager):

    @asynccontextmanager
    async def begin(
        self,
        session: AsyncSession,
    ) -> None:
        explicit_transaction_key = 'explicit_transaction'

        info: dict = session.info
        explicit_transaction = info.get(explicit_transaction_key, False)
        info[explicit_transaction_key] = True

        if not (session.in_transaction() or explicit_transaction):
            await session.begin()

        try:
            yield
        except:
            await session.rollback()

        if session.in_transaction() and not explicit_transaction:
            await session.commit()
