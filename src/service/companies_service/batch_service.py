"""Service for running the company finder logic for a batch of cities."""

import json
import time
from datetime import date
from pathlib import Path
from uuid import uuid4

from src.config import get_logger
from src.models.input.time_interval import TimeInterval
from src.service.companies_service.service import CompaniesService

logger = get_logger(__name__)


class BatchCompanyService:
    """Service to run company finding logic for a list of locations."""

    EUROPE_TECH_HUBS = [
        "Berlin",        # Germany
        "Amsterdam",     # Netherlands
        "Paris",         # France
        "Barcelona",     # Spain
        "Dublin",        # Ireland
        "Lisbon",        # Portugal
        "Munich",        # Germany
        "Madrid",        # Spain
        "Stockholm",     # Sweden
        "Milan",         # Italy
        "Vienna",        # Austria
        "Copenhagen",    # Denmark
        "Helsinki",      # Finland
        "Warsaw",        # Poland
        "Prague",        # Czech Republic
    ]

    SLEEP_SUCCESS: int = 60
    SLEEP_ERROR: int = 180

    def __init__(self) -> None:
        self.companies_service = CompaniesService()

    def run(self, locations: list[str], start_date: date, end_date: date, output_dir: Path | None = None) -> None:
        """Run the company finder for the given locations."""
        logger.info("Starting batch run for %d locations: %s", len(locations), locations)
        logger.info("Time range: %s to %s", start_date, end_date)
        
        success_count = 0
        error_count = 0
        failed_locations: list[str] = []
        time_interval = TimeInterval(start_date=start_date, end_date=end_date)
        
        total = len(locations)
        
        for i, location in enumerate(locations, 1):
            logger.info("[%d/%d] Processing location: %s", i, total, location)
            
            try:
                results = self.companies_service.get_companies_by_location(
                    location=location,
                    time_interval=time_interval,
                )
                
                self._save_results(location, results, output_dir)
                
                success_count += 1
                logger.info("Successfully processed: %s", location)
                
                if i < total:
                    logger.info("Sleeping for %d seconds before next location...", self.SLEEP_SUCCESS)
                    time.sleep(self.SLEEP_SUCCESS)
                    
            except Exception as e:
                logger.error("Error processing %s: %s", location, e, exc_info=True)
                error_count += 1
                failed_locations.append(location)
                
                if i < total:
                    logger.info("Error occurred. Sleeping for %d seconds before next location...", self.SLEEP_ERROR)
                    time.sleep(self.SLEEP_ERROR)

        self._print_summary(success_count, error_count, failed_locations, total)

    def _save_results(self, location: str, results: list, output_dir: Path | None) -> None:
        """Save the results to a JSON file."""
        payload = [entry.model_dump() for entry in results]
        
        if output_dir is None:
            output_dir = Path("results")
            
        filename = f"summits-companies-{location.lower().replace(' ', '-')}-{uuid4()}.json"
        output_path = output_dir / filename
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.info("Results saved to %s", output_path)

    def _print_summary(self, success_count: int, error_count: int, failed_locations: list[str], total: int) -> None:
        """Print the execution summary."""
        logger.info("========================================")
        logger.info("SUMMARY")
        logger.info("========================================")
        logger.info("Total locations processed: %d", total)
        logger.info("Successful: %d", success_count)
        logger.info("Failed: %d", error_count)
        
        if failed_locations:
            logger.info("")
            logger.info("Failed locations:")
            for loc in failed_locations:
                logger.info("  - %s", loc)
        
        logger.info("========================================")
