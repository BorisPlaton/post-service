from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import CHAR

from infrastructure.database.sqlalchemy.base import Base
from infrastructure.database.sqlalchemy.mixins import IdMixin


class User(IdMixin, Base):
    """
    User model. It contains only credentials.
    """
    __tablename__ = 'user'

    login: Mapped[str] = mapped_column(
        String(
            length=128,
        ),
        name='login',
        nullable=False,
        unique=True,
    )
    password: Mapped[str | None] = mapped_column(
        CHAR(
            length=64,
        ),
        name='password',
        nullable=False,
    )

    @classmethod
    def create(
        cls,
        login: str,
        password: str,
    ) -> User:
        """
        Creates a new user record.

        @param login:
            User's login.
        @param password:
            User's hashed password. Must be length of 64.
        @return:
            The user record.
        """
        return User(
            login=login,
            password=password,
        )
