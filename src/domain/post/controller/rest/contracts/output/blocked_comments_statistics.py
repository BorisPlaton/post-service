from datetime import date

from pydantic import BaseModel
from pydantic import Field


class PostCommentBlockStatisticsOutputContract(BaseModel):
    """
    Represents the following statistics:
    * How many comments were written in the specific day.
    * How many comments were blocked in the specific day.
    """
    date_: date = Field(
        examples=['2024-10-12'],
        description='The date of the blocked comments statistics.',
        alias='date',
    )
    created: int = Field(
        ge=0,
        examples=[76],
        description="How many comments were created at this date."
    )
    blocked: int = Field(
        ge=0,
        examples=[23],
        description="How many comments were blocked at this date."
    )
