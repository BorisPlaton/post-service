from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, kw_only=True)
class PostBlockStatistics:
    """
    Represents the following statistics:
    * How many posts were written in the specific day.
    * How many posts were blocked in the specific day.
    """
    date: date
    created: int
    blocked: int
