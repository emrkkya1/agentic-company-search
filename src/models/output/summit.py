"""Summit model for individual conference/summit data."""

from pydantic import Field

from src.models.base import BaseModel


class Summit(BaseModel):
    """Individual tech summit/conference.

    Attributes:
        name: The name of the summit/conference.
        dates: Human-readable date string (e.g., "June 15-17, 2025").
        categories: List of focus areas (e.g., ["AI", "Cloud", "DevOps"]).
        website: URL of the summit website, if available.
        venue: Location/venue of the summit, if available.
    """

    name: str = Field(description="Official summit name, e.g. 'Web Summit 2025'.")
    dates: str = Field(description="Date range as 'Month Day-Day, Year', e.g. 'June 15-17, 2025'.")
    categories: list[str] = Field(description="Focus areas, e.g. ['AI', 'Cloud', 'DevOps'].")
    website: str | None = Field(default=None, description="Full URL, e.g. 'https://websummit.com'.")
    venue: str | None = Field(default=None, description="Location as 'Venue, City' or 'City, Country'.")
