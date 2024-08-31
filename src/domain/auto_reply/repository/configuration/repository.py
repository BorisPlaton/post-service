from functools import cached_property

from sqlalchemy import select

from domain.auto_reply.excepiton.configuration_doesnt_exist import ConfigurationDoesNotExist
from domain.auto_reply.model.configuration import CommentAutoReplyConfiguration
from domain.auto_reply.repository.configuration.interface import ICommentAutoReplyConfigurationRepository


class DelayedCommentResponseConfigurationRepository(ICommentAutoReplyConfigurationRepository):

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> CommentAutoReplyConfiguration:
        configuration = await self.scalar(
            select(
                CommentAutoReplyConfiguration
            ).where(
                CommentAutoReplyConfiguration.user_id == user_id,
            )
        )

        if not configuration:
            raise ConfigurationDoesNotExist()

        return configuration

    @cached_property
    def entity_class(self) -> type[CommentAutoReplyConfiguration]:
        return CommentAutoReplyConfiguration
