#!/usr/bin/env python3
"""
Process JSON files in the results folder and generate a deduplicated list
of startup, small, and medium companies.
"""

import json
import os
from pathlib import Path


def load_json_files(results_dir: Path) -> list[dict]:
    """Load all JSON files from the results directory."""
    all_data = []
    for json_file in results_dir.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    return all_data


def extract_companies(summit_data: list[dict]) -> list[dict]:
    """Extract all companies from summit data."""
    companies = []
    for entry in summit_data:
        if "companies" in entry:
            for company in entry["companies"]:
                # Add summit info to company for context
                company_with_summit = {
                    **company,
                    "summit": entry.get("summit", {}).get("name", "Unknown")
                }
                companies.append(company_with_summit)
    return companies


def filter_by_scale(companies: list[dict], allowed_scales: set[str]) -> list[dict]:
    """Filter companies by scale."""
    return [c for c in companies if c.get("scale", "").lower() in allowed_scales]


def filter_out_countries(companies: list[dict], excluded_countries: set[str]) -> list[dict]:
    """Filter out companies from specified countries."""
    return [c for c in companies if c.get("origin_country", "").lower() not in excluded_countries]


def remove_duplicates(companies: list[dict]) -> list[dict]:
    """Remove duplicate companies by name, keeping the first occurrence."""
    seen = set()
    unique_companies = []
    for company in companies:
        name = company.get("name", "").strip().lower()
        if name and name not in seen:
            seen.add(name)
            # Remove summit field for cleaner output, store summits as list
            company_clean = {
                "name": company.get("name"),
                "origin_country": company.get("origin_country"),
                "field": company.get("field"),
                "scale": company.get("scale"),
            }
            unique_companies.append(company_clean)
    return unique_companies


def main():
    # Configuration
    results_dir = Path(__file__).parent / "results"
    output_file = Path(__file__).parent / "filtered_companies.json"
    allowed_scales = {"startup", "small", "medium"}
    excluded_countries = {"united states"}

    print(f"Processing JSON files from: {results_dir}")

    # Load all JSON files
    summit_data = load_json_files(results_dir)
    print(f"Loaded {len(summit_data)} summit entries")

    # Extract all companies
    all_companies = extract_companies(summit_data)
    print(f"Found {len(all_companies)} total company entries")

    # Filter by scale
    filtered_companies = filter_by_scale(all_companies, allowed_scales)
    print(f"After filtering by scale ({', '.join(allowed_scales)}): {len(filtered_companies)} companies")

    # Filter out excluded countries
    filtered_companies = filter_out_countries(filtered_companies, excluded_countries)
    print(f"After excluding countries ({', '.join(excluded_countries)}): {len(filtered_companies)} companies")

    # Remove duplicates
    unique_companies = remove_duplicates(filtered_companies)
    print(f"After removing duplicates: {len(unique_companies)} unique companies")

    # Sort by name for consistency
    unique_companies.sort(key=lambda x: x.get("name", "").lower())

    # Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_companies, f, indent=2, ensure_ascii=False)

    print(f"\nOutput saved to: {output_file}")

    # Print summary by scale
    print("\nSummary by scale:")
    for scale in allowed_scales:
        count = sum(1 for c in unique_companies if c.get("scale") == scale)
        print(f"  {scale}: {count}")

    # Print summary by field
    print("\nTop 10 fields:")
    field_counts = {}
    for c in unique_companies:
        field = c.get("field", "unknown")
        field_counts[field] = field_counts.get(field, 0) + 1
    for field, count in sorted(field_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {field}: {count}")


if __name__ == "__main__":
    main()
