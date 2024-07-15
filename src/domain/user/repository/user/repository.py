from functools import cached_property

from sqlalchemy import select

from domain.user.model.user import User
from domain.user.repository.user.interface import IUserRepository


class UserRepository(IUserRepository):
    """
    The repository for interacting with user model.
    """

    async def get_by_login(self, login: str) -> User | None:
        """
        Returns a user by its login.

        @param login:
            The user's login.
        @return:
            The user if it's found, `None` otherwise.
        """
        statement = select(
            User,
        ).where(
            User.login == login,
        ).execution_options(
            populate_existing=True,
        )
        return await self.scalar(statement)

    @cached_property
    def entity_class(self) -> type[User]:
        return User
