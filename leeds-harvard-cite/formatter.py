"""Core formatting helpers for Harvard-style journal citations."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Mapping, Optional, Sequence, Union

AuthorInput = Union[str, Mapping[str, str]]

DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y/%m/%d",
    "%d %B %Y",
    "%B %d, %Y",
)

MONTH_NAMES = (
    None,
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def parse_date_value(date_value: Union[str, datetime, None]) -> datetime | None:
    """Parse a supported input date into a datetime object."""
    if date_value is None:
        return None
    if isinstance(date_value, datetime):
        return date_value

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(str(date_value), date_format)
        except ValueError:
            continue

    return None


def format_date(date_value: Union[str, datetime, None]) -> str:
    """Format an accessed date as '[Accessed DD Month YYYY]'."""
    parsed_date = parse_date_value(date_value)
    if parsed_date is None:
        if date_value is None:
            parsed_date = datetime.now()
        else:
            return f"[Accessed {date_value}]"

    return f"[Accessed {parsed_date.day} {MONTH_NAMES[parsed_date.month]} {parsed_date.year}]"


def get_initials(given_names: str) -> str:
    """Convert a given-name string to dotted initials."""
    parts = [part for part in re.split(r"[\s\-\u00A0]+", given_names.strip()) if part]
    return "".join(f"{part[0].upper()}." for part in parts)


def normalize_author(author: AuthorInput) -> dict[str, str]:
    """Normalize author input into family / given / initials fields."""
    if isinstance(author, Mapping):
        family = author.get("family", "").strip()
        given = author.get("given", "").strip()
        initials = given if given and "." in given else get_initials(given)
        return {"family": family, "given": given, "initials": initials}

    author_text = str(author).strip().rstrip(",")

    if "," in author_text:
        family, given = [part.strip() for part in author_text.split(",", 1)]
        initials = given if "." in given else get_initials(given)
        return {"family": family, "given": given, "initials": initials}

    tokens = author_text.split()
    if len(tokens) <= 1:
        family = tokens[0] if tokens else ""
        return {"family": family, "given": "", "initials": ""}

    family = tokens[-1]
    given = " ".join(tokens[:-1])
    return {"family": family, "given": given, "initials": get_initials(given)}


def format_authors(authors: Sequence[AuthorInput]) -> str:
    """Format one or more authors in Harvard reference-list style."""
    normalized_authors = [normalize_author(author) for author in authors if str(author).strip()]
    if not normalized_authors:
        return ""

    formatted = []
    for author in normalized_authors:
        if author["initials"]:
            formatted.append(f"{author['family']}, {author['initials']}")
        else:
            formatted.append(author["family"])

    if len(formatted) == 1:
        return formatted[0]
    if len(formatted) == 2:
        return f"{formatted[0]} and {formatted[1]}"

    return f"{', '.join(formatted[:-1])} and {formatted[-1]}"


def format_pages(pages: Optional[str]) -> str:
    """Format a page range with the Harvard 'pp.' prefix."""
    if not pages:
        return ""

    cleaned = str(pages).strip()
    return cleaned if cleaned.lower().startswith("pp.") else f"pp.{cleaned}"


def normalize_supplement(supplement: str) -> str:
    """Normalize supplement values such as S1 or Supp. 3."""
    cleaned = supplement.strip()
    if re.fullmatch(r"[Ss]\d+", cleaned):
        return f"Supp. {cleaned[1:]}"

    if cleaned.lower().startswith("supp"):
        number = re.sub(r"[^0-9]+", "", cleaned)
        return f"Supp. {number}" if number else "Supp."

    return cleaned


def format_issue(issue: Optional[str], supplement: Optional[str]) -> str:
    """Format issue or supplement information inside parentheses."""
    if supplement:
        return f"({normalize_supplement(str(supplement))})"
    if issue:
        return f"({str(issue).strip()})"
    return ""


def format_location(doi: Optional[str], url: Optional[str]) -> str:
    """Prefer DOI over URL and normalize DOI to its full web form."""
    if doi:
        cleaned = str(doi).strip()
        if cleaned.lower().startswith("http"):
            return cleaned
        return f"https://doi.org/{cleaned.replace('doi:', '').strip()}"

    if url:
        return str(url).strip()

    return ""


def build_online_block(
    volume: Optional[str],
    issue: Optional[str],
    pages: Optional[str],
    article_number: Optional[str],
    supplement: Optional[str],
) -> str:
    """Build the '[Online]. ...' block for the final citation."""
    issue_text = format_issue(issue, supplement)
    volume_text = str(volume).strip() if volume else ""
    page_text = format_pages(pages)

    if volume_text:
        if article_number:
            return f"[Online]. {volume_text}{issue_text}, article no: {article_number} [no pagination]."
        if page_text:
            return f"[Online]. {volume_text}{issue_text}, {page_text}."
        return f"[Online]. {volume_text}{issue_text}."

    if article_number:
        return f"[Online]. article no: {article_number} [no pagination]."
    if page_text:
        return f"[Online]. {page_text}."
    return "[Online]."


def clean_segment(value: str) -> str:
    """Trim whitespace and trailing periods from title-like segments."""
    return str(value).strip().rstrip(".")


def format_citation(
    authors: Sequence[AuthorInput],
    year: Union[int, str, None],
    title: str,
    journal: str,
    volume: Optional[str] = None,
    issue: Optional[str] = None,
    pages: Optional[str] = None,
    doi: Optional[str] = None,
    url: Optional[str] = None,
    accessed: Optional[Union[str, datetime]] = None,
    article_number: Optional[str] = None,
    supplement: Optional[str] = None,
    status: Optional[str] = None,
) -> str:
    """Format a journal citation in a Harvard-style reference format."""
    author_part = format_authors(authors)
    year_part = str(year) if year is not None else "n.d."
    title_part = clean_segment(title)
    journal_part = clean_segment(journal)
    accessed_part = format_date(accessed or datetime.now())
    location_part = format_location(doi, url)

    if status in {"Pre-print", "Post-print"}:
        year_part = f"{year_part}. [{status}]."
    else:
        year_part = f"{year_part}."

    citation_parts = [
        f"{author_part}." if author_part else "",
        year_part,
        f"{title_part}." if title_part else "",
        f"{journal_part}." if journal_part else "",
        build_online_block(volume, issue, pages, article_number, supplement),
        f"{accessed_part}.",
        f"Available from: {location_part}" if location_part else "",
    ]

    citation = " ".join(part for part in citation_parts if part)
    citation = re.sub(r"\s+\.", ".", citation)
    citation = re.sub(r"\.\.", ".", citation)
    citation = re.sub(r"\]\.\s+([A-Za-z])", r"]. \1", citation)
    citation = re.sub(r"\s+", " ", citation)
    return citation.strip()
