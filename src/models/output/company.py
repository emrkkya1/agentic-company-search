"""Company model for individual company data."""

from pydantic import Field

from src.models.base import BaseModel
from src.models.enums import CompanyField, CompanyScale


class Company(BaseModel):
    """Individual company from a summit.

    Attributes:
        name: The official name of the company.
        origin_country: The country where the company is headquartered.
        field: The primary industry/field the company operates in.
        scale: The size/scale classification of the company.
    """

    name: str = Field(description="Official company name, e.g. 'Google LLC'.")
    origin_country: str = Field(description="Headquarters country in English, e.g. 'United States'.")
    field: CompanyField = Field(description="Primary industry based on main product/service.")
    scale: CompanyScale = Field(description="Size: startup(<50), small(50-200), medium(200-1k), large(1k-10k), enterprise(10k+).")
