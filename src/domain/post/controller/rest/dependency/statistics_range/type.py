from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, kw_only=True)
class StatisticsRangeType:
    """
    The dataclass that contains data range.
    """
    from_: date
    to: date
