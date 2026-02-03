"""Time interval model for date range inputs."""

from datetime import date

from src.models.base import BaseModel


class TimeInterval(BaseModel):
    """Time interval with human-readable LLM formatting.

    Represents a date range that can be formatted in a way that's
    easy for LLMs to understand.

    Attributes:
        start_date: The beginning of the time interval.
        end_date: The end of the time interval.
    """

    start_date: date
    end_date: date

    def format_for_llm(self) -> str:
        """Format the time interval for LLM understanding.

        Returns:
            A human-readable string like 'From June 2025 to December 2025'.
        """
        start = self.start_date.strftime("%B %Y")
        end = self.end_date.strftime("%B %Y")
        return f"From {start} to {end}"
