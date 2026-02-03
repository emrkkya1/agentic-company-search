"""Input model for company search."""

from src.models.base import BaseModel
from src.models.output.summit import Summit


class CompaniesInput(BaseModel):
    """Input model for company search.

    Attributes:
        summit: The summit to search for participating companies.
    """

    summit: Summit
