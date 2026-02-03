"""Enumerations for categorizing data in the application."""

from enum import Enum


class CompanyScale(str, Enum):
    """Company size/scale classification.

    Categories based on typical employee count and market presence.
    """

    STARTUP = "startup"  # Early-stage, typically < 50 employees
    SMALL = "small"  # Small business, typically 50-200 employees
    MEDIUM = "medium"  # Mid-size company, typically 200-1000 employees
    LARGE = "large"  # Large company, typically 1000-10000 employees
    ENTERPRISE = "enterprise"  # Major corporation, typically 10000+ employees


class CompanyField(str, Enum):
    """Company industry/field classification.

    Categories for common technology and business sectors.
    """

    # Technology sectors
    SOFTWARE = "software"
    ARTIFICIAL_INTELLIGENCE = "artificial_intelligence"
    CLOUD_COMPUTING = "cloud_computing"
    CYBERSECURITY = "cybersecurity"
    DATA_ANALYTICS = "data_analytics"
    GAMING = "gaming"
    HARDWARE = "hardware"
    SEMICONDUCTORS = "semiconductors"
    TELECOMMUNICATIONS = "telecommunications"

    # Business sectors
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    E_COMMERCE = "e_commerce"
    AUTOMOTIVE = "automotive"
    AEROSPACE = "aerospace"
    ENERGY = "energy"
    MANUFACTURING = "manufacturing"
    MEDIA_ENTERTAINMENT = "media_entertainment"
    EDUCATION = "education"
    CONSULTING = "consulting"

    # Other
    OTHER = "other"
