from datetime import date

from pydantic import BaseModel
from pydantic import Field


class PostBlockStatisticsOutputContract(BaseModel):
    """
    Represents the following statistics:
    * How many posts were written in the specific day.
    * How many posts were blocked in the specific day.
    """
    date_: date = Field(
        examples=['2024-10-12'],
        description='The date of the blocked posts statistics.',
        alias='date',
    )
    created: int = Field(
        ge=0,
        examples=[76],
        description="How many posts were created at this date."
    )
    blocked: int = Field(
        ge=0,
        examples=[23],
        description="How many posts were blocked at this date."
    )
