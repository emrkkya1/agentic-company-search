"""Output model for company search results."""

from pydantic import Field

from src.models.base import BaseModel
from src.models.output.company import Company


class CompaniesOutput(BaseModel):
    """Output model containing list of companies.

    Attributes:
        companies: List of Company objects found at the summit.
    """

    companies: list[Company] = Field(description="List of participating companies, no duplicates.")
