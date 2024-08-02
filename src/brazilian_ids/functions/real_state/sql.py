"""Functions to handle SQL codes.

Do not confuse SQL with the name of the query language for relational
databases.

SQL in this context means "Setor, Quadra e Lote" in Brazilian Portuguese, and
it's used to provide a unique identifier to a real state property and is also
related to the IPTU tax from governament.

SQL is also known as "número do contribuinte" or "cadastro do imóvel".
"""

from collections import deque

from brazilian_ids.functions.util import NONDIGIT_REGEX
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError

EXPECTED_DIGITS = 11
EXPECTED_DIGITS_WITHOUT_VERIFICATION = 10
VERIFICATION_DIGITS_WEIGHT = (10, 1, 2, 3, 4, 5, 6, 7, 8, 9)


class InvalidSqlTypeMixin:
    """Mixin class for SQL errors."""

    def id_type(self):
        return "SQL"


class InvalidSqlError(InvalidSqlTypeMixin, InvalidIdError):
    """Exception for invalid SQL errors"""

    def __init__(self, sql: str) -> None:
        super().__init__(id=sql)


class InvalidSqlLengthError(InvalidSqlTypeMixin, InvalidIdLengthError):
    """Exception for invalid SQL length error."""

    def __init__(
        self, sql: str, expected_digits: int = EXPECTED_DIGITS_WITHOUT_VERIFICATION
    ) -> None:
        super().__init__(id=sql, expected_digits=expected_digits)


def is_valid(sql: str) -> bool:
    """Check if a given SQL is valid or not.

    Non-numeric characters will be removed before testing.
    """
    sql = NONDIGIT_REGEX.sub("", sql)

    if len(sql) != EXPECTED_DIGITS:
        return False

    return sql[-1] == verification_digit(sql)


def verification_digit(sql: str, validate_length: bool = False) -> str:
    """Calculate the verification digit needed to make a SQL code value.

    If you have a SQL which length is less than ``EXPECTED_DIGITS``, than use
    ``pad`` first in it, otherwise the exception ``InvalidSqlLengthError`` will
    be raised (if ``validate_Length`` is ``True``) or the digit calculated will
    be just invalid."""
    sql = NONDIGIT_REGEX.sub("", sql)
    sql = sql[:-1]

    if validate_length:
        if len(sql) != EXPECTED_DIGITS_WITHOUT_VERIFICATION:
            raise InvalidSqlLengthError(sql)

    digits = (int(i) for i in sql)
    digits_times_weights = (w * d for w, d in zip(VERIFICATION_DIGITS_WEIGHT, digits))
    result = (sum(digits_times_weights)) % 11

    if result == 10:
        return "1"

    return str(result)


def format(sql: str) -> str:
    """Format the SQL string as ``NNN.NNN.NNNN-N``.

    If you have a SQL which length is less than ``EXPECTED_DIGITS``, than use
    ``pad`` with it before calling format to avoid the ``InvalidSqlError``
    exception.
    """
    sql = NONDIGIT_REGEX.sub("", sql)

    if len(sql) < EXPECTED_DIGITS:
        raise InvalidSqlError(sql)

    return "{0}.{1}.{2}-{3}".format(sql[:3], sql[3:6], sql[6:10], sql[-1])


def pad(sql: str) -> str:
    """Includes 0 at the left of a SQL that length is less than
    ``EXPECTED_DIGITS``."""
    sql = NONDIGIT_REGEX.sub("", sql)

    if len(sql) < EXPECTED_DIGITS:
        tmp = deque(sql)
        padded = ["0" for i in range(11)]

        for i in range(10, 0, -1):
            if len(tmp) > 0:
                padded[i] = tmp.pop()

        return "".join(padded)

    return sql
