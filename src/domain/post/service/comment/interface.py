from abc import ABC
from abc import abstractmethod
from datetime import date

from domain.post.model import PostComment
from domain.post.dto.comment.statistics import CommentBlockStatistics


class IPostCommentService(ABC):

    @abstractmethod
    async def get_comments(
        self,
        post_id: int,
    ) -> list[PostComment]:
        raise NotImplementedError()

    @abstractmethod
    async def get_statistics(
        self,
        from_: date,
        to: date,
    ) -> list[CommentBlockStatistics]:
        raise NotImplementedError()
