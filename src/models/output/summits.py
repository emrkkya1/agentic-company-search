"""Output model for summit search results."""

from pydantic import Field

from src.models.base import BaseModel
from src.models.output.summit import Summit


class SummitsOutput(BaseModel):
    """Output model containing list of summits.

    Attributes:
        summits: List of Summit objects found in the search.
    """

    summits: list[Summit] = Field(description="List of matching summits, no duplicates.")
