#!/usr/bin/env python3
"""Command-line interface for the citation formatter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from formatter import format_citation
from universities import get_university_info, is_valid_university, list_universities, print_universities


def parse_authors(authors_str: str) -> list[str]:
    """Split an author string into individual author entries."""
    if not authors_str:
        return []

    normalized = authors_str.replace(" and ", ";")
    return [author.strip() for author in normalized.split(";") if author.strip()]


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    return argparse.ArgumentParser(
        description="Format journal citations in Harvard style.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --authors "Smith, John; Johnson, Amy" --year 2024 \\
    --title "Article Title" --journal "Journal Name" --volume 10 --issue 2 --pages 15-30

  python main.py --list-universities
  python main.py --interactive
        """.strip(),
    )


def configure_parser(parser: argparse.ArgumentParser) -> None:
    """Register all supported CLI arguments."""
    parser.add_argument("--authors", "-a", help="Authors separated by ';' or 'and'")
    parser.add_argument("--year", "-y", help="Publication year")
    parser.add_argument("--title", "-t", help="Article title")
    parser.add_argument("--journal", "-j", help="Journal name")

    parser.add_argument("--volume", "-v", help="Volume number")
    parser.add_argument("--issue", "-i", help="Issue number")
    parser.add_argument("--pages", "-p", help="Page range, for example 15-30")
    parser.add_argument("--doi", "-d", help="Digital Object Identifier")
    parser.add_argument("--url", help="URL")
    parser.add_argument("--accessed", help="Access date in YYYY-MM-DD")
    parser.add_argument("--article-number", help="Article number for online-only journals")
    parser.add_argument("--supplement", help="Supplement value, for example S1 or Supp. 3")
    parser.add_argument(
        "--status",
        choices=["Pre-print", "Post-print"],
        help="Publication status",
    )

    parser.add_argument("--university", "-u", default="leeds", help="University code")
    parser.add_argument("--output", "-o", help="Output file path")

    parser.add_argument("--list-universities", "-l", action="store_true", help="List supported universities")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")


def ensure_valid_university(code: str) -> str:
    """Validate and normalize the university code."""
    normalized = code.lower()
    if is_valid_university(normalized):
        return normalized

    print(f"Error: invalid university code '{code}'.")
    print_universities()
    sys.exit(1)


def ensure_required_args(args: argparse.Namespace) -> None:
    """Ensure all required single-citation arguments are present."""
    missing = [
        option
        for option, value in (
            ("--authors", args.authors),
            ("--year", args.year),
            ("--title", args.title),
            ("--journal", args.journal),
        )
        if not value
    ]

    if not missing:
        return

    print("Error: missing required arguments.")
    print(f"Required: {', '.join(missing)}")
    print("Use -h for help or --interactive for guided input.")
    sys.exit(1)


def build_citation_from_args(args: argparse.Namespace) -> str:
    """Format a citation from parsed CLI arguments."""
    return format_citation(
        authors=parse_authors(args.authors),
        year=args.year,
        title=args.title,
        journal=args.journal,
        volume=args.volume,
        issue=args.issue,
        pages=args.pages,
        doi=args.doi,
        url=args.url,
        accessed=args.accessed,
        article_number=args.article_number,
        supplement=args.supplement,
        status=args.status,
    )


def write_output(citation: str, output_path: str | None) -> None:
    """Write the formatted citation to stdout or to a file."""
    if output_path:
        Path(output_path).write_text(f"{citation}\n", encoding="utf-8")
        print(f"Citation saved to {output_path}")
        return

    print("\n" + "=" * 80)
    print(citation)
    print("=" * 80 + "\n")


def prompt_optional_field(prompt: str) -> str | None:
    """Prompt for an optional field and normalize empty input to None."""
    value = input(prompt).strip()
    return value or None


def select_university_interactively() -> str | None:
    """Prompt the user to choose a university in interactive mode."""
    universities = list_universities()

    print("Available universities:")
    for index, (code, name, _) in enumerate(universities, start=1):
        print(f"  {index:2}. {code:15} - {name}")

    choice = input("\nSelect university (number or code) [1]: ").strip() or "1"

    try:
        if choice.isdigit():
            return universities[int(choice) - 1][0]

        normalized = choice.lower()
        if is_valid_university(normalized):
            return normalized
    except (ValueError, IndexError):
        pass

    print("Error: invalid selection.")
    return None


def interactive_mode() -> None:
    """Run the interactive prompt for a single citation."""
    print("\n" + "=" * 80)
    print("Citation Formatter - Interactive Mode")
    print("=" * 80 + "\n")

    university_code = select_university_interactively()
    if not university_code:
        return

    university = get_university_info(university_code)
    print(f"\nSelected: {university['name']} ({university['style']})\n")

    authors_input = input("Authors (separated by ';' or 'and'): ").strip()
    year = input("Publication year: ").strip() or "n.d."
    title = input("Article title: ").strip()
    journal = input("Journal name: ").strip()

    if not authors_input or not title or not journal:
        print("Error: authors, title, and journal are required.")
        return

    print("\nPress Enter to skip optional fields.\n")
    volume = prompt_optional_field("Volume: ")
    issue = prompt_optional_field("Issue: ")
    pages = prompt_optional_field("Pages: ")
    doi = prompt_optional_field("DOI: ")
    url = prompt_optional_field("URL: ")
    accessed = prompt_optional_field("Access date (YYYY-MM-DD): ")

    citation = format_citation(
        authors=parse_authors(authors_input),
        year=year,
        title=title,
        journal=journal,
        volume=volume,
        issue=issue,
        pages=pages,
        doi=doi,
        url=url,
        accessed=accessed,
    )

    print("\n" + "=" * 80)
    print("Formatted Citation")
    print("=" * 80)
    print(citation)
    print("=" * 80 + "\n")

    if input("Save to file? (y/n) [n]: ").strip().lower() != "y":
        return

    filename = input("Filename [citation.txt]: ").strip() or "citation.txt"
    Path(filename).write_text(f"{citation}\n", encoding="utf-8")
    print(f"Saved to {filename}")


def main() -> None:
    """Entry point for the CLI."""
    parser = build_parser()
    configure_parser(parser)
    args = parser.parse_args()

    if args.list_universities:
        print_universities()
        return

    if args.interactive:
        interactive_mode()
        return

    ensure_required_args(args)
    args.university = ensure_valid_university(args.university)

    citation = build_citation_from_args(args)
    write_output(citation, args.output)


if __name__ == "__main__":
    main()
