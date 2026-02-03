"""Companies search agent for finding companies at tech summits."""

from src.agents.base import BaseAgent
from src.agents.internal import StructurizeAgent
from src.models.enums import CompanyField, CompanyScale
from src.models.input.companies import CompaniesInput
from src.models.output.companies import CompaniesOutput

# Build enum value lists for the prompt
_SCALE_VALUES = ", ".join([s.value for s in CompanyScale])
_FIELD_VALUES = ", ".join([f.value for f in CompanyField])

COMPANIES_PROMPT = """Search for companies that participated in or sponsored the tech summit: {summit_name}.

Summit details:
- Name: {summit_name}
- Dates: {summit_dates}
- Website: {summit_website}
- Venue: {summit_venue}

Find an extensive list of companies that have participated in, sponsored, exhibited at, or presented at this summit.

For each company, provide:
1. name: The official company name
2. origin_country: The country where the company is headquartered
3. field: Must be one of: {field_values}
4. scale: Must be one of: {scale_values}

Include all types of participants: major sponsors, exhibitors, startups in startup alleys, presenting companies, and any other corporate participants.

Return as many companies as you can find that are associated with this summit."""


class CompaniesAgent(BaseAgent):
    """Agent for searching companies at tech summits.

    Uses the configured LLM adapter to search for companies that
    participated in a given summit with Google grounding for
    up-to-date information. Results are then structured using
    the StructurizeAgent.
    """

    def __init__(self) -> None:
        """Initialize the agent with the configured LLM adapter and structurizer."""
        super().__init__()
        self.structurizer = StructurizeAgent()

    def search(self, input_data: CompaniesInput) -> CompaniesOutput:
        """Search for companies that participated in a summit.

        Args:
            input_data: The search criteria containing the summit to search.

        Returns:
            CompaniesOutput containing a list of found companies.
        """
        summit = input_data.summit
        self.logger.info("Searching companies for summit: %s", summit.name)

        prompt = COMPANIES_PROMPT.format(
            summit_name=summit.name,
            summit_dates=summit.dates,
            summit_categories=", ".join(summit.categories) if summit.categories else "N/A",
            summit_website=summit.website or "N/A",
            summit_venue=summit.venue or "N/A",
            field_values=_FIELD_VALUES,
            scale_values=_SCALE_VALUES,
        )

        # Step 1: Get raw text with google grounding (with retry)
        raw_text = self._retry_with_backoff(
            lambda: self.client.generate_content(prompt=prompt, google_grounding=True)
        )
        self.logger.debug("Raw companies search response length: %d chars", len(raw_text))

        # Step 2: Structure the text using StructurizeAgent
        result = self.structurizer.structurize(text=raw_text, response_schema=CompaniesOutput)
        self.logger.info("Found %d companies for %s", len(result.companies), summit.name)
        return result
