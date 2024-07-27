"""Helper functions for validating identifiers."""

import re


NONDIGIT_REGEX = re.compile(r"[^0-9]")


def clean_id(identifier: str) -> str:
    """Remove non-numeric characters from an ID."""
    return NONDIGIT_REGEX.sub("", identifier)


def pad_id(identifier: str, fmt: str) -> str:
    """Pad an ID with a given format."""
    return fmt % clean_id(identifier)
