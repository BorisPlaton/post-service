from abc import ABC
from abc import abstractmethod

from domain.user.model.user import User
from shared.database.sqlalchemy.repository import AsyncSQLAlchemyRepository


class IUserRepository(AsyncSQLAlchemyRepository[int, User], ABC):

    @abstractmethod
    async def get_by_login(self, login: str) -> User | None:
        raise NotImplementedError()
