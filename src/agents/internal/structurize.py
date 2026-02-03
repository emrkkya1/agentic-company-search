"""Structurize agent for converting unstructured text into structured data."""

from typing import TypeVar

from pydantic import BaseModel

from src.agents.base import BaseAgent

# Type variable for Pydantic models
T = TypeVar("T", bound=BaseModel)

STRUCTURIZE_PROMPT = """Extract and structure all information from the following text into the required JSON format.

Important: Ensure NO data from the text is missed. Extract every relevant piece of information that matches the schema fields.

Text to structure:
{text}

Return a complete JSON object matching the required schema."""


class StructurizeAgent(BaseAgent):
    """Agent for converting unstructured text into structured data.

    Uses the configured LLM adapter to extract information from raw text
    and structure it according to a provided Pydantic schema.
    """

    def __init__(self) -> None:
        """Initialize the agent with the configured LLM adapter."""
        super().__init__()

    def structurize(self, text: str, response_schema: type[T]) -> T:
        """Convert unstructured text into a structured Pydantic model instance.

        Args:
            text: The raw text containing information to extract.
            response_schema: A Pydantic BaseModel class defining the expected
                structure of the extracted data.

        Returns:
            A validated instance of the provided Pydantic model with data
            extracted from the input text.

        Example:
            ```python
            from pydantic import BaseModel

            class Person(BaseModel):
                name: str
                age: int
                occupation: str

            agent = StructurizeAgent()
            result = agent.structurize(
                text="John Smith is a 35-year-old software engineer.",
                response_schema=Person,
            )
            # result.name == "John Smith"
            # result.age == 35
            # result.occupation == "software engineer"
            ```
        """
        self.logger.debug("Structurizing text (%d chars) into %s", len(text), response_schema.__name__)
        prompt = STRUCTURIZE_PROMPT.format(text=text)
        result = self._retry_with_backoff(
            lambda: self.client.generate_content_with_schema(
                prompt=prompt,
                response_schema=response_schema,
            )
        )
        self.logger.debug("Structurization complete: %s", response_schema.__name__)
        return result
