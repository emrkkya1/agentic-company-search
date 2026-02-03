"""CLI entry point for the application."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from uuid import uuid4

import typer

from src.config import get_logger, setup_logging
from src.models.input.time_interval import TimeInterval
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


def main() -> None:
    """Main function."""
    app()


if __name__ == "__main__":
    main()
