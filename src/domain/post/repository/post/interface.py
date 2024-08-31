from abc import ABC

from domain.post.model import Post
from infrastructure.database.sqlalchemy.repository import AsyncSQLAlchemyRepository


class IPostRepository(AsyncSQLAlchemyRepository[int, Post], ABC):
    pass
