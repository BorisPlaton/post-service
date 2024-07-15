from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IdMixin:
    """
    The mixin for the SQLAlchemy model.

    It contains only one id field.
    """
    id: Mapped[int] = mapped_column(
        primary_key=True,
        name='id',
    )
