from domain.ai.component.client.interface import IAIClient
from domain.auto_reply.excepiton.comment_autho_doesnt_exist import CommentAuthorDoesNotExist
from domain.auto_reply.excepiton.post_author_doesnt_exist import PostAuthorDoesNotExist
from domain.auto_reply.task.dto import NewCommentCreatedTaskDTO
from domain.post.model import PostComment
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.repository.post.interface import IPostRepository
from domain.user.repository.user.interface import IUserRepository
from shared.database.sqlalchemy.transcation.interface import ITransactionManager
from shared.task.abstract import AbstractTask


class AutoReplyTask(AbstractTask[NewCommentCreatedTaskDTO]):

    def __init__(
        self,
        dto: NewCommentCreatedTaskDTO,
    ):
        super().__init__(dto=dto)
        self._user_repository: IUserRepository = self.container.resolve(IUserRepository)
        self._post_repository: IPostRepository = self.container.resolve(IPostRepository)
        self._post_comment_repository: IPostCommentRepository = self.container.resolve(IPostCommentRepository)
        self._ai_client: IAIClient = self.container.resolve(IAIClient)
        self._transaction_manager: ITransactionManager = self.container.resolve(ITransactionManager)

    async def __call__(self) -> None:
        post_author = await self._user_repository.get(
            id_=self.dto.post_author_id,
        )
        if not post_author:
            raise PostAuthorDoesNotExist()

        comment_author = await self._user_repository.get(
            id_=self.dto.post_author_id,
        )
        if not comment_author:
            raise CommentAuthorDoesNotExist()

        comment = await self._post_comment_repository.get(
            id_=self.dto.comment_id,
        )
        reply_text = self._ai_client.send(
            message=f'Reply on this post comment: {comment.content}.'
        ).strip('"')
        reply_comment = PostComment.create(
            author_id=self.dto.post_author_id,
            post_id=self.dto.post_id,
            blocked=False,
            content=f"@{comment_author.login}, {reply_text}",
        )

        async with self._transaction_manager.begin():
            await self._post_comment_repository.create(reply_comment)
