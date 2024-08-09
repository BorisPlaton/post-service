from datetime import date
from typing import Annotated

from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from domain.post.controller.rest.dependency.statistics_range.type import StatisticsRangeType


def get_statistics_range(
    to: Annotated[date | None, Query(alias='to', description="To which date statistics are starting.")] = None,
    from_: Annotated[date | None, Query(alias='from', description="From which date statistics are starting.")] = None,
) -> StatisticsRangeType:
    """
    The FastAPI dependency for statistics date range.
    """
    if from_ and to and from_ > to:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parameter `from` can't be greater than `to`. "
        )

    return StatisticsRangeType(
        to=to,
        from_=from_,
    )
