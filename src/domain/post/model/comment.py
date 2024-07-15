from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy import sql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from shared.database.sqlalchemy.base import Base
from shared.database.sqlalchemy.mixins import IdMixin


class PostComment(IdMixin, Base):
    """
    Post's comment model.
    """
    __tablename__ = 'post_comment'

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
    post_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="post.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        name='post_id',
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
        content: str,
        author_id: int,
        post_id: int,
        blocked: bool,
    ) -> PostComment:
        """
        Creates a comment for the specific post.

        @param content:
            The text of the comment.
        @param author_id:
            The user's id who wrote the comment.
        @param post_id:
            The post's id to which comment belongs.
        @param blocked:
            Whether the comment is blocked.
        @return:
            The comment record.
        """
        return PostComment(
            content=content,
            author_id=author_id,
            post_id=post_id,
            blocked=blocked,
        )
