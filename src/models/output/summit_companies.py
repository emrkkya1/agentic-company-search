"""Output model for summit + companies pairs."""

from src.models.base import BaseModel
from src.models.output.company import Company
from src.models.output.summit import Summit


class SummitCompanies(BaseModel):
    """Summit paired with its participating companies.

    Attributes:
        summit: The summit details.
        companies: List of companies participating in the summit.
    """

    summit: Summit
    companies: list[Company]
