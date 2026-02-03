"""Base agent class with retry and exponential backoff mechanisms."""

import time
from abc import ABC
from collections.abc import Callable
from typing import TypeVar

from src.adapters import get_adapter
from src.adapters.base import LLMClient
from src.config import get_logger, settings

# Type variable for generic return types
T = TypeVar("T")


class BaseAgent(ABC):
    """Abstract base class for all agents with retry capabilities.

    Provides common functionality including:
    - Automatic LLM client initialization
    - Retry mechanism with exponential backoff for transient failures
    - Configurable retry settings via application config

    Subclasses should use _retry_with_backoff() to wrap LLM API calls
    for automatic retry handling on transient errors.
    """

    def __init__(self) -> None:
        """Initialize the agent with the configured LLM adapter."""
        self.client: LLMClient = get_adapter()
        self.logger = get_logger(self.__class__.__module__)

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate the delay before the next retry attempt.

        Uses exponential backoff with jitter, capped at max_delay.

        Args:
            attempt: The current attempt number (0-indexed).

        Returns:
            The delay in seconds before the next retry.
        """
        delay = settings.retry_base_delay * (settings.retry_exponential_base ** attempt)
        return min(delay, settings.retry_max_delay)

    def _retry_with_backoff(
        self,
        func: Callable[[], T],
        max_attempts: int | None = None,
    ) -> T:
        """Execute a function with retry and exponential backoff.

        Retries the given function on failure, using exponential backoff
        between attempts. Useful for handling transient API errors such as
        rate limits or temporary network issues.

        Args:
            func: A callable that takes no arguments and returns a value.
                  Typically a lambda wrapping an LLM API call.
            max_attempts: Override the default maximum retry attempts.
                          If None, uses settings.retry_max_attempts.

        Returns:
            The return value of the function on success.

        Raises:
            Exception: Re-raises the last exception if all retries are exhausted.

        Example:
            ```python
            result = self._retry_with_backoff(
                lambda: self.client.generate_content(prompt)
            )
            ```
        """
        attempts = max_attempts if max_attempts is not None else settings.retry_max_attempts
        last_exception: Exception | None = None

        for attempt in range(attempts):
            try:
                return func()
            except Exception as e:
                last_exception = e
                if attempt < attempts - 1:
                    delay = self._calculate_delay(attempt)
                    self.logger.warning(
                        "Attempt %d/%d failed: %s. Retrying in %.1fs...",
                        attempt + 1,
                        attempts,
                        str(e),
                        delay,
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(
                        "All %d attempts failed. Last error: %s",
                        attempts,
                        str(e),
                    )

        # This should never be reached due to the raise in the loop,
        # but satisfies type checker
        raise last_exception  # type: ignore[misc]
