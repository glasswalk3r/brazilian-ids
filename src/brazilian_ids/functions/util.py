"""Helper to validate identifiers.

For internal use only.
"""

import re

NONDIGIT_REGEX = re.compile(r"[^0-9]")
