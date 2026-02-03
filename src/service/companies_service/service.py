"""Service for aggregating summits with participating companies."""

from src.agents.companies import CompaniesAgent
from src.agents.summits import SummitAgent
from src.config import get_logger
from src.models.input.companies import CompaniesInput
from src.models.input.summits import SummitsInput
from src.models.input.time_interval import TimeInterval
from src.models.output.summit_companies import SummitCompanies

logger = get_logger(__name__)


class CompaniesService:
    """Service for fetching summits and their companies."""

    def __init__(self) -> None:
        self.summit_agent = SummitAgent()
        self.companies_agent = CompaniesAgent()

    def get_companies_by_location(
        self,
        location: str,
        time_interval: TimeInterval,
    ) -> list[SummitCompanies]:
        """Get summit/company pairs for a location and time range."""
        logger.info("Starting company search: location=%s, %s to %s",
                    location, time_interval.start_date, time_interval.end_date)

        summits_input = SummitsInput(location=location, time_interval=time_interval)
        summits_output = self.summit_agent.search(summits_input)

        results: list[SummitCompanies] = []
        for i, summit in enumerate(summits_output.summits, 1):
            logger.info("Processing summit %d/%d: %s", i, len(summits_output.summits), summit.name)
            companies_input = CompaniesInput(summit=summit)
            companies_output = self.companies_agent.search(companies_input)
            results.append(
                SummitCompanies(
                    summit=summit,
                    companies=companies_output.companies,
                )
            )

        total_companies = sum(len(r.companies) for r in results)
        logger.info("Search complete: %d summits, %d total companies", len(results), total_companies)
        return results
