from datetime import timedelta

from rq import Queue

from domain.ai.component.client.interface import IAIClient
from domain.auto_reply.repository.configuration.interface import ICommentAutoResponseConfigurationRepository
from domain.auto_reply.task.auto_reply import AutoReplyTask
from domain.auto_reply.task.dto import NewCommentCreatedTaskDTO
from domain.post.event.new_comment_created import NewCommentCreatedEvent
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.repository.post.interface import IPostRepository
from domain.user.repository.user.interface import IUserRepository
from shared.message_bus.event_bus.handler.interface import IEventHandler
from shared.module_setup.config import ModulesConfig
from shared.redis_.client.interface import IRedisClient


class AutoResponseForNewComment(IEventHandler[NewCommentCreatedEvent]):

    def __init__(
        self,
        configuration_repository: ICommentAutoResponseConfigurationRepository,
        ai_client: IAIClient,
        post_comment_repository: IPostCommentRepository,
        post_repository: IPostRepository,
        user_repository: IUserRepository,
        redis_client: IRedisClient,
        modules_config: ModulesConfig,
    ):
        self._configuration_repository = configuration_repository
        self._queue = Queue(connection=redis_client.client)
        self._ai_client = ai_client
        self._post_comment_repository = post_comment_repository
        self._post_repository = post_repository
        self._user_repository = user_repository
        self._modules_config = modules_config

    async def __call__(
        self,
        message: NewCommentCreatedEvent,
    ) -> None:
        configuration = await self._configuration_repository.get_by_user_id(
            user_id=message.post_author_id,
        )

        if configuration.enabled and message.comment_author_id != message.post_author_id and not message.blocked:
            self._queue.enqueue_in(
                time_delta=timedelta(seconds=configuration.auto_reply_delay),
                func=AutoReplyTask.execute,
                dto=NewCommentCreatedTaskDTO(
                    post_id=message.post_id,
                    comment_id=message.comment_id,
                    comment_author_id=message.comment_author_id,
                    post_author_id=message.post_author_id,
                    modules=self._modules_config.modules,
                ),
            )
            self._queue.enqueue(
                AutoReplyTask.execute,
                dto=NewCommentCreatedTaskDTO(
                    post_id=message.post_id,
                    comment_id=message.comment_id,
                    comment_author_id=message.comment_author_id,
                    post_author_id=message.post_author_id,
                    modules=self._modules_config.modules,
                ),
            )

