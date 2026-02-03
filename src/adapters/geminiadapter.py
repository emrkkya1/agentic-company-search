"""Gemini API adapter for simple LLM interactions."""

import time
from typing import TypeVar

from google import genai
from pydantic import BaseModel

from src.adapters.base import LLMClient
from src.config import get_logger, settings

# Type variable for Pydantic models
T = TypeVar("T", bound=BaseModel)

logger = get_logger(__name__)


class GeminiAdapter(LLMClient):
    """Adapter for interacting with Google's Gemini API.

    Provides a simple interface for generating content using the Gemini models.
    Configuration is loaded from environment variables via the settings module.
    """

    def __init__(self) -> None:
        """Initialize the Gemini client with API key from settings."""
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model
        logger.info("Initialized GeminiAdapter with model=%s", self.model)

    def generate_content(
        self,
        prompt: str,
        google_grounding: bool = False,
    ) -> str:
        """Generate content from a text prompt.

        Args:
            prompt: The text prompt to send to the model.
            google_grounding: If True, enables Google Search grounding for
                up-to-date information.

        Returns:
            The generated text response from the model.
        """
        config = {}
        if google_grounding:
            config["tools"] = [{"google_search": {}}]

        logger.debug("LLM request: grounding=%s, prompt_len=%d", google_grounding, len(prompt))
        start = time.perf_counter()

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config if config else None,
        )

        elapsed = time.perf_counter() - start
        logger.info("LLM response: %.2fs, output_len=%d", elapsed, len(response.text))
        return response.text

    def generate_content_with_config(
        self,
        prompt: str,
        model: str | None = None,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
        google_grounding: bool = False,
    ) -> str:
        """Generate content with custom configuration options.

        Args:
            prompt: The text prompt to send to the model.
            model: Override the default model name.
            max_output_tokens: Maximum number of tokens in the response.
            temperature: Controls randomness in generation (0.0 to 2.0).
            google_grounding: If True, enables Google Search grounding for
                up-to-date information.

        Returns:
            The generated text response from the model.
        """
        model_name = model or self.model

        # Build generation config from provided or default settings
        config_params: dict = {}
        if max_output_tokens is not None or settings.gemini_max_output_tokens is not None:
            config_params["max_output_tokens"] = (
                max_output_tokens or settings.gemini_max_output_tokens
            )
        if temperature is not None or settings.gemini_temperature is not None:
            config_params["temperature"] = temperature or settings.gemini_temperature

        if google_grounding:
            config_params["tools"] = [{"google_search": {}}]

        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config_params if config_params else None,
        )
        return response.text

    def generate_content_with_schema(
        self,
        prompt: str,
        response_schema: type[T],
        model: str | None = None,
        google_grounding: bool = False,
    ) -> T:
        """Generate content constrained to a Pydantic schema.

        Uses Gemini's structured output feature to return a validated
        Pydantic model instance.

        Args:
            prompt: The text prompt to send to the model.
            response_schema: A Pydantic BaseModel class defining the expected
                response structure.
            model: Override the default model name.
            google_grounding: If True, enables Google Search grounding for
                up-to-date information.

        Returns:
            A validated instance of the provided Pydantic model.

        Example:
            ```python
            from pydantic import BaseModel

            class Recipe(BaseModel):
                name: str
                ingredients: list[str]
                instructions: list[str]

            adapter = GeminiAdapter()
            recipe = adapter.generate_content_with_schema(
                prompt="Give me a recipe for chocolate chip cookies",
                response_schema=Recipe,
            )
            print(recipe.name)
            ```
        """
        model_name = model or self.model

        config: dict = {
            "response_mime_type": "application/json",
            "response_json_schema": response_schema.model_json_schema(),
        }

        if google_grounding:
            config["tools"] = [{"google_search": {}}]

        logger.debug("LLM schema request: schema=%s, grounding=%s", response_schema.__name__, google_grounding)
        start = time.perf_counter()

        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config,
        )

        elapsed = time.perf_counter() - start
        logger.info("LLM schema response: %.2fs, schema=%s", elapsed, response_schema.__name__)

        # Parse and validate the JSON response into the Pydantic model
        return response_schema.model_validate_json(response.text)
