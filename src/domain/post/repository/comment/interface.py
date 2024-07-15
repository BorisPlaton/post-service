from abc import ABC

from domain.post.model import PostComment
from shared.database.sqlalchemy.repository import AsyncSQLAlchemyRepository


class IPostCommentRepository(AsyncSQLAlchemyRepository[int, PostComment], ABC):
    pass
