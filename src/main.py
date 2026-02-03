"""CLI entry point for the application."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from uuid import uuid4

import typer

from src.config import get_logger, setup_logging
from src.models.input.time_interval import TimeInterval
from src.service.companies_service.batch_service import BatchCompanyService
from src.service.companies_service.service import CompaniesService

# Initialize logging early
setup_logging()
logger = get_logger(__name__)

app = typer.Typer(help="Find companies attending tech summits.")


def parse_iso_date(value: str) -> date:
    """Parse an ISO date (YYYY-MM-DD) or raise a CLI error."""
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise typer.BadParameter("Use ISO date format YYYY-MM-DD.") from exc


@app.command()
def find_companies(
    location: str = typer.Argument(..., help="City or country to search."),
    time_start: str = typer.Argument(..., help="Start date (YYYY-MM-DD)."),
    time_end: str = typer.Argument(..., help="End date (YYYY-MM-DD)."),
    save_result: bool = typer.Option(
        True,
        "--save-result/--no-save-result",
        help="Save results as JSON.",
    ),
    output_path: Path | None = typer.Option(
        None,
        "--output-path",
        help="Output JSON path. Default: results/summits-companies-<uuid4>.json",
    ),
) -> None:
    """Find companies for summits in a location and time range."""
    logger.info("CLI invoked: location=%s, time=%s to %s", location, time_start, time_end)

    start_date = parse_iso_date(time_start)
    end_date = parse_iso_date(time_end)
    time_interval = TimeInterval(start_date=start_date, end_date=end_date)

    service = CompaniesService()
    results = service.get_companies_by_location(location=location, time_interval=time_interval)

    payload = [entry.model_dump() for entry in results]

    if save_result:
        if output_path is None:
            output_path = Path("results") / f"summits-companies-{uuid4()}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.info("Results saved to %s", output_path)
        typer.echo(f"Saved {len(payload)} results to {output_path}")
    else:
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))


@app.command()
def run_batch(
    locations: list[str] = typer.Argument(
        None,
        help="List of cities or countries to search.",
    ),
    europe: bool = typer.Option(
        False,
        "--europe",
        help="Include major European tech hubs.",
    ),
    time_start: str = typer.Option(
        "2025-01-01",
        "--time-start",
        help="Start date (YYYY-MM-DD). Default: 2025-01-01",
    ),
    time_end: str = typer.Option(
        "2025-12-31",
        "--time-end",
        help="End date (YYYY-MM-DD). Default: 2025-12-31",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        help="Directory to save JSON results. Default: results/",
    ),
) -> None:
    """Run the company finder for a batch of locations."""
    start_date = parse_iso_date(time_start)
    end_date = parse_iso_date(time_end)

    target_locations = []
    if locations:
        target_locations.extend(locations)
    
    if europe:
        target_locations.extend(BatchCompanyService.EUROPE_TECH_HUBS)
    
    # Remove duplicates while preserving order
    target_locations = list(dict.fromkeys(target_locations))
    
    if not target_locations:
        typer.echo("Error: No locations provided. Use arguments or --europe flag.")
        raise typer.Exit(code=1)

    service = BatchCompanyService()
    service.run(locations=target_locations, start_date=start_date, end_date=end_date, output_dir=output_dir)


def main() -> None:
    """Main function."""
    app()


if __name__ == "__main__":
    main()
