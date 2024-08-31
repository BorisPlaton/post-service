from domain.ai.component.client.interface import IAIClient
from domain.auto_reply.command.auto_reply.command import AutoReplyCommentCommand
from domain.auto_reply.excepiton.comment_autho_doesnt_exist import CommentAuthorDoesNotExist
from domain.auto_reply.excepiton.post_author_doesnt_exist import PostAuthorDoesNotExist
from domain.post.model import PostComment
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.repository.post.interface import IPostRepository
from domain.user.repository.user.interface import IUserRepository
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler


class AutoReplyCommentCommandHandler(ICommandHandler[AutoReplyCommentCommand, None]):

    def __init__(
        self,
        user_repository: IUserRepository,
        post_repository: IPostRepository,
        post_comment_repository: IPostCommentRepository,
        ai_client: IAIClient,
    ):
        self._user_repository = user_repository
        self._post_repository = post_repository
        self._post_comment_repository = post_comment_repository
        self._ai_client = ai_client

    async def __call__(
        self,
        command: AutoReplyCommentCommand,
    ) -> None:
        post_author = await self._user_repository.get(
            id_=command.post_author_id,
        )
        if not post_author:
            raise PostAuthorDoesNotExist()

        comment_author = await self._user_repository.get(
            id_=command.post_author_id,
        )
        if not comment_author:
            raise CommentAuthorDoesNotExist()

        comment = await self._post_comment_repository.get(
            id_=command.comment_id,
        )
        reply_text = self._ai_client.send(
            message=f'Reply on this post comment: {comment.content}.'
        ).strip('"')
        reply_comment = PostComment.create(
            author_id=command.post_author_id,
            post_id=command.post_id,
            blocked=False,
            content=f"@{comment_author.login}, {reply_text}",
        )

        await self._post_comment_repository.create(reply_comment)
