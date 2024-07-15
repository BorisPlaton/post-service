from datetime import date

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from domain.post.exception.post_doesnt_exist import PostDoesNotExist
from domain.post.model import Post
from domain.post.repository.post.interface import IPostRepository
from domain.post.service.post.interface import IPostService
from domain.post.dto.post.statistics import PostBlockStatistics


class PostService(IPostService):
    """
    The service layer of the post model.

    This class contains business-logic, that can't be placed anywhere else.
    """

    def __init__(
        self,
        post_repository: IPostRepository,
    ):
        """
        @param post_repository:
            The repository of the post model.
        """
        self._post_repository = post_repository

    async def get_post(
        self,
        post_id: int,
    ) -> Post:
        """
        Returns a not banned post by its id.

        @param post_id:
            The post's id.
        @return:
            The list of posts.
        """
        post = await self._post_repository.get_all_by_filter(
            filter_=(Post.id == post_id) & (Post.blocked == False),
        )

        if not post:
            raise PostDoesNotExist()

        return post[0]

    async def get_statistics(
        self,
        from_: date | None,
        to: date | None,
    ) -> list[PostBlockStatistics]:
        """
        Returns of statistics of posts in the specific date range.

        This statistics contains following values:
        * How many posts were created in the specific day.
        * How many posts were banned in the specific day.

        @param from_:
            Date from which statistics should start.
        @param to:
            Date at which statistics should end.
        @return:
            The list with statistics for provided date range.
        """
        statement = select(
            func.date(Post.created_at).label('date'),
            count().label('created'),
            count().filter(Post.blocked == True).label('blocked'),
        ).group_by(
            func.date(Post.created_at),
        ).order_by(
            func.date(Post.created_at),
        )

        if from_:
            statement = statement.where(
                Post.created_at >= from_
            )
        if to:
            statement = statement.where(
                Post.created_at <= to
            )

        return [
            PostBlockStatistics(
                date=post.date,
                created=post.created,
                blocked=post.blocked,
            ) for post in await self._post_repository.execute(statement)
        ]
