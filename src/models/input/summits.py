"""Input model for summit search."""

from src.models.base import BaseModel
from src.models.input.time_interval import TimeInterval


class SummitsInput(BaseModel):
    """Input model for summit search.

    Attributes:
        location: The location to search for summits (country or city).
        time_interval: The time range to search within.
    """

    location: str
    time_interval: TimeInterval
