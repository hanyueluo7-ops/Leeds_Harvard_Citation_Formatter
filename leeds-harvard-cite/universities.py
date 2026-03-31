"""University metadata used by the CLI and web interface."""

from __future__ import annotations

from typing import Optional

UniversityInfo = dict[str, str]

UNIVERSITIES: dict[str, UniversityInfo] = {
    "leeds": {
        "name": "University of Leeds",
        "style": "Leeds Harvard",
        "description": "Formal institutional Harvard variation",
        "website": "https://library.leeds.ac.uk",
    },
    "oxford": {
        "name": "University of Oxford",
        "style": "Harvard (flexible by college)",
        "description": "Harvard style with departmental variations",
        "website": "https://www.ox.ac.uk",
    },
    "cambridge": {
        "name": "University of Cambridge",
        "style": "Harvard (discipline-specific)",
        "description": "Harvard style adapted by discipline",
        "website": "https://www.cam.ac.uk",
    },
    "imperial": {
        "name": "Imperial College London",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.imperial.ac.uk",
    },
    "ucl": {
        "name": "UCL (University College London)",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.ucl.ac.uk",
    },
    "lse": {
        "name": "London School of Economics",
        "style": "Harvard",
        "description": "Standard Harvard with APA alternative",
        "website": "https://www.lse.ac.uk",
    },
    "manchester": {
        "name": "University of Manchester",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.manchester.ac.uk",
    },
    "warwick": {
        "name": "University of Warwick",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.warwick.ac.uk",
    },
    "durham": {
        "name": "University of Durham",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.durham.ac.uk",
    },
    "bristol": {
        "name": "University of Bristol",
        "style": "Harvard (most flexible)",
        "description": "Harvard with support for 8+ citation styles",
        "website": "https://www.bristol.ac.uk",
    },
    "edinburgh": {
        "name": "University of Edinburgh",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.ed.ac.uk",
    },
    "southampton": {
        "name": "University of Southampton",
        "style": "Harvard (department choice)",
        "description": "Harvard with departmental flexibility",
        "website": "https://www.southampton.ac.uk",
    },
    "birmingham": {
        "name": "University of Birmingham",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.birmingham.ac.uk",
    },
    "york": {
        "name": "University of York",
        "style": "Harvard",
        "description": "Standard Harvard citation style",
        "website": "https://www.york.ac.uk",
    },
    "kcl": {
        "name": "King's College London",
        "style": "Harvard/APA",
        "description": "Harvard with faculty-specific variations",
        "website": "https://www.kcl.ac.uk",
    },
}


def list_universities() -> list[tuple[str, str, str]]:
    """Return a compact list of supported universities."""
    return [(code, info["name"], info["style"]) for code, info in UNIVERSITIES.items()]


def is_valid_university(code: str) -> bool:
    """Return True when the given university code is supported."""
    return code.lower() in UNIVERSITIES


def get_university_info(code: str) -> Optional[UniversityInfo]:
    """Return the metadata for a specific university code."""
    return UNIVERSITIES.get(code.lower())


def print_universities() -> None:
    """Print a human-readable list of supported universities."""
    print("\nSupported Universities (15 UK institutions):\n")
    for index, (code, name, style) in enumerate(list_universities(), start=1):
        print(f"  {index:2}. {code:15} - {name:40} ({style})")
    print()
