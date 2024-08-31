from datetime import timedelta

from rq import Queue

from domain.ai.component.client.interface import IAIClient
from domain.auto_reply.command.auto_reply.command import AutoReplyCommentCommand
from domain.auto_reply.repository.configuration.interface import ICommentAutoReplyConfigurationRepository
from domain.post.event.new_comment_created import NewCommentCreatedEvent
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.repository.post.interface import IPostRepository
from domain.user.repository.user.interface import IUserRepository
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus
from infrastructure.message_bus.command_bus.config.options.background import BackgroundExecutionOption
from infrastructure.message_bus.event_bus.handler.interface import IEventHandler
from infrastructure.redis_.client.interface import IRedisClient


class AutoReplyForNewComment(IEventHandler[NewCommentCreatedEvent]):

    def __init__(
        self,
        configuration_repository: ICommentAutoReplyConfigurationRepository,
        ai_client: IAIClient,
        post_comment_repository: IPostCommentRepository,
        post_repository: IPostRepository,
        user_repository: IUserRepository,
        redis_client: IRedisClient,
        command_bus: ICommandBus,
    ):
        self._configuration_repository = configuration_repository
        self._queue = Queue(connection=redis_client.client)
        self._ai_client = ai_client
        self._post_comment_repository = post_comment_repository
        self._post_repository = post_repository
        self._user_repository = user_repository
        self._command_bus = command_bus

    async def __call__(
        self,
        message: NewCommentCreatedEvent,
    ) -> None:
        configuration = await self._configuration_repository.get_by_user_id(
            user_id=message.post_author_id,
        )

        if configuration.enabled and not message.blocked:
            command = AutoReplyCommentCommand(
                post_id=message.post_id,
                comment_id=message.comment_id,
                comment_author_id=message.comment_author_id,
                post_author_id=message.post_author_id,
            )
            command.update_config(
                config=BackgroundExecutionOption,
                enqueue_in=10,
            )
            await self._command_bus.handle(
                message=command,
            )
