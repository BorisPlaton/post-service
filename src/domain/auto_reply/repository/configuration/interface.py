from abc import ABC
from abc import abstractmethod

from domain.auto_reply.model.configuration import CommentAutoReplyConfiguration
from infrastructure.database.sqlalchemy.repository import AsyncSQLAlchemyRepository


class ICommentAutoReplyConfigurationRepository(
    AsyncSQLAlchemyRepository[int, CommentAutoReplyConfiguration],
    ABC,
):

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: int,
    ) -> CommentAutoReplyConfiguration:
        ...
