from abc import ABC
from abc import abstractmethod

from domain.auto_reply.model.configuration import CommentAutoReplyConfiguration
from shared.database.sqlalchemy.repository import AsyncSQLAlchemyRepository


class ICommentAutoResponseConfigurationRepository(
    AsyncSQLAlchemyRepository[int, CommentAutoReplyConfiguration],
    ABC,
):

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: int,
    ) -> CommentAutoReplyConfiguration:
        raise NotImplementedError()
