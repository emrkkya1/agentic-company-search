"""Adapters package for external API integrations."""

from src.adapters.base import LLMClient
from src.adapters.geminiadapter import GeminiAdapter
from src.config import settings


def get_adapter() -> LLMClient:
    """Return the configured adapter instance.

    Returns:
        An LLMClient instance based on the configured adapter_type.

    Raises:
        ValueError: If the configured adapter_type is not supported.
    """
    adapters: dict[str, type[LLMClient]] = {
        "gemini": GeminiAdapter,
    }
    adapter_class = adapters.get(settings.adapter_type)
    if not adapter_class:
        raise ValueError(f"Unknown adapter type: {settings.adapter_type}")
    return adapter_class()


__all__ = ["LLMClient", "GeminiAdapter", "get_adapter"]
