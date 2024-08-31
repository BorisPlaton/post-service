from abc import ABC
from abc import abstractmethod
from datetime import date

from domain.post.model import Post
from domain.post.dto.post.statistics import PostBlockStatistics


class IPostService(ABC):

    @abstractmethod
    async def get_post(
        self,
        post_id: int,
    ) -> Post:
        ...

    @abstractmethod
    async def get_statistics(
        self,
        from_: date,
        to: date,
    ) -> list[PostBlockStatistics]:
        ...
