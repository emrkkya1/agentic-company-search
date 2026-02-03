"""Abstract base interface for LLM adapters."""

from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

# Type variable for Pydantic models
T = TypeVar("T", bound=BaseModel)


class LLMClient(ABC):
    """Abstract interface for LLM adapters.

    All LLM adapters must implement this interface to ensure consistent
    method signatures across different providers (Gemini, OpenAI, etc.).
    """

    @abstractmethod
    def generate_content(self, prompt: str, google_grounding: bool = False) -> str:
        """Generate text content from a prompt.

        Args:
            prompt: The text prompt to send to the model.
            google_grounding: If True, enables web search grounding for
                up-to-date information (if supported by the adapter).

        Returns:
            The generated text response from the model.
        """
        ...

    @abstractmethod
    def generate_content_with_schema(
        self,
        prompt: str,
        response_schema: type[T],
        google_grounding: bool = False,
    ) -> T:
        """Generate content constrained to a Pydantic schema.

        Args:
            prompt: The text prompt to send to the model.
            response_schema: A Pydantic BaseModel class defining the expected
                response structure.
            google_grounding: If True, enables web search grounding for
                up-to-date information (if supported by the adapter).

        Returns:
            A validated instance of the provided Pydantic model.
        """
        ...
