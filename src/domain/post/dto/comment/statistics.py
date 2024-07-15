from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, kw_only=True)
class CommentBlockStatistics:
    """
    Represents the following statistics:
    * How many comments were written in the specific day.
    * How many comments were blocked in the specific day.
    """
    date_: date
    created: int
    blocked: int
