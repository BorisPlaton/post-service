from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy import sql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database.sqlalchemy.base import Base
from infrastructure.database.sqlalchemy.mixins import IdMixin


class Post(IdMixin, Base):
    """
    Post model.
    """
    __tablename__ = 'post'

    title: Mapped[str] = mapped_column(
        String(
            length=256,
        ),
        name='title',
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        String(
            length=4096,
        ),
        name='content',
        nullable=False,
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="user.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        name='author_id',
        nullable=False,
    )
    blocked: Mapped[bool] = mapped_column(
        name='blocked',
        nullable=False,
        default=False,
        server_default=sql.false(),
    )
    created_at: Mapped[datetime] = mapped_column(
        name="created_at",
        default=datetime.now(),
        server_default=func.now(),
        nullable=True,
    )

    @classmethod
    def create(
        cls,
        title: str,
        content: str,
        author_id: int,
        blocked: bool,
    ) -> Post:
        """
        Creates a comment for the specific post.

        @param title:
            The post's title.
        @param content:
            The text of the comment.
        @param author_id:
            The user's id who wrote the comment.
        @param blocked:
            Whether the post is blocked.
        @return:
            The comment record.
        """
        return Post(
            title=title,
            content=content,
            author_id=author_id,
            blocked=blocked,
        )
