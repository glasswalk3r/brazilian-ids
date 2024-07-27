"""Helper functions and regular expressions for validating identifiers."""

import re


NONDIGIT_REGEX = re.compile(r"[^0-9]")


def pad_id(identifier: str, fmt: str) -> str:
    """Pad an ID with a given format."""
    identifier = NONDIGIT_REGEX.sub("", identifier)
    return fmt % identifier
