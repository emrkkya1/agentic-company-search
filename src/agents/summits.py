"""Summit search agent for finding tech conferences and summits."""

from src.agents.base import BaseAgent
from src.agents.internal import StructurizeAgent
from src.models.input.summits import SummitsInput
from src.models.output.summits import SummitsOutput

SUMMIT_SEARCH_PROMPT = """Search for technology summits and conferences in {location} {time_interval}.

Return a list of summits with: name, dates, categories (focus areas), website URL, and venue."""


class SummitAgent(BaseAgent):
    """Agent for searching tech summits and conferences.

    Uses the configured LLM adapter to search for technology summits
    in a given location and time period with Google grounding for
    up-to-date information. Results are then structured using
    the StructurizeAgent.
    """

    def __init__(self) -> None:
        """Initialize the agent with the configured LLM adapter and structurizer."""
        super().__init__()
        self.structurizer = StructurizeAgent()

    def search(self, input_data: SummitsInput) -> SummitsOutput:
        """Search for tech summits based on input criteria.

        Args:
            input_data: The search criteria containing location and time interval.

        Returns:
            SummitsOutput containing a list of found summits.
        """
        self.logger.info("Searching summits: location=%s, period=%s",
                         input_data.location, input_data.time_interval.format_for_llm())

        prompt = SUMMIT_SEARCH_PROMPT.format(
            location=input_data.location,
            time_interval=input_data.time_interval.format_for_llm(),
        )

        # Step 1: Get raw text with google grounding (with retry)
        raw_text = self._retry_with_backoff(
            lambda: self.client.generate_content(prompt=prompt, google_grounding=True)
        )
        self.logger.debug("Raw summit search response length: %d chars", len(raw_text))

        # Step 2: Structure the text using StructurizeAgent
        result = self.structurizer.structurize(text=raw_text, response_schema=SummitsOutput)
        self.logger.info("Found %d summits", len(result.summits))
        return result
