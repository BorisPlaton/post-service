from datetime import date

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from domain.post.model import PostComment
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.service.comment.interface import IPostCommentService
from domain.post.service.post.interface import IPostService
from domain.post.dto.comment.statistics import CommentBlockStatistics


class PostCommentService(IPostCommentService):
    """
    The service layer of the post comment model.

    This class contains business-logic, that can't be placed anywhere else.
    """

    def __init__(
        self,
        post_service: IPostService,
        post_comment_repository: IPostCommentRepository,
    ):
        """
        @param post_service:
            The post service class.
        @param post_comment_repository:
            The repository of the post comment model.
        """
        self._post_service = post_service
        self._post_comment_repository = post_comment_repository

    async def get_comments(
        self,
        post_id: int,
    ) -> list[PostComment]:
        """
        Returns all not banned comments for a specific not banned post.

        @param post_id:
            The post's id whose comments need to be fetched.
        @return:
            The list of post comments.
        """
        await self._post_service.get_post(post_id=post_id)

        return await self._post_comment_repository.get_all_by_filter(
            filter_=(PostComment.post_id == post_id) & (PostComment.blocked == False),
        )

    async def get_statistics(
        self,
        from_: date | None,
        to: date | None,
    ) -> list[CommentBlockStatistics]:
        """
        Returns of statistics of post comments in the specific date range.

        This statistics contains following values:
        * How many comments were created in the specific day.
        * How many comments were banned in the specific day.

        @param from_:
            Date from which statistics should start.
        @param to:
            Date at which statistics should end.
        @return:
            The list with statistics for provided date range.
        """
        statement = select(
            func.date(PostComment.created_at.label('date')),
            count(PostComment.id).label('created'),
            count(PostComment.id).filter(PostComment.blocked == True).label('blocked'),
        ).group_by(
            func.date(PostComment.created_at),
        ).order_by(
            PostComment.created_at,
        )

        if from_:
            statement = statement.where(
                PostComment.created_at >= from_
            )
        if to:
            statement = statement.where(
                PostComment.created_at <= to
            )

        return [
            CommentBlockStatistics(
                date_=post.date,
                created=post.created,
                blocked=post.blocked,
            ) for post in await self._post_comment_repository.scalars(statement)
        ]
