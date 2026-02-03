"""Application configuration using Pydantic Settings."""

import logging
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Add your configuration variables here
    app_name: str = "LLM Internship Finder"
    debug: bool = False

    # Adapter Configuration
    adapter_type: str = "gemini"  # Options: "gemini"

    # Gemini API Configuration
    gemini_api_key: str = ""  # Required, loaded from GEMINI_API_KEY env var
    gemini_model: str = "gemini-2.5-flash"  # Default model
    gemini_max_output_tokens: int | None = None  # Optional limit
    gemini_temperature: float | None = None  # Optional temperature (0.0 to 2.0)

    # Logging Configuration
    log_level: str = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR

    # Retry Configuration
    retry_max_attempts: int = 3  # Maximum number of retry attempts
    retry_base_delay: float = 1.0  # Base delay between retries in seconds
    retry_max_delay: float = 60.0  # Maximum delay between retries in seconds
    retry_exponential_base: float = 2.0  # Multiplier for exponential backoff


# Global settings instance
settings = Settings()


def setup_logging() -> None:
    """Configure application logging with readable, concise output."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    log_format = "%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
    date_format = "%H:%M:%S"

    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)
