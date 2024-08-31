from __future__ import annotations

from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import sql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database.sqlalchemy.base import Base
from infrastructure.database.sqlalchemy.mixins import IdMixin


class CommentAutoReplyConfiguration(IdMixin, Base):
    """
    The settings for the auto reply on post comments.
    """
    __tablename__ = 'comment_auto_reply_configuration'
    __table_args__ = (
        CheckConstraint('auto_reply_delay > 0', name='auto_reply_delay_must_be_positive'),
    )

    enabled: Mapped[bool] = mapped_column(
        name='enabled',
        nullable=False,
        default=False,
        server_default=sql.false(),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="user.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        name='user_id',
        nullable=False,
        unique=True,
    )
    auto_reply_delay: Mapped[int] = mapped_column(
        name='auto_reply_delay',
        nullable=False,
    )

    @classmethod
    def create(
        cls,
        enabled: bool,
        user_id: int,
        auto_reply_delay: int,
    ) -> CommentAutoReplyConfiguration:
        """
        Creates a new instance with provided arguments.

        @param enabled:
            If the auto-reply function is enabled.
        @param user_id:
            To which user this auto-reply is for.
        @param auto_reply_delay:
            After how many seconds the reply will be issued.
        @return:
            The new class instance.
        """
        return cls(
            enabled=enabled,
            user_id=user_id,
            auto_reply_delay=auto_reply_delay,
        )
