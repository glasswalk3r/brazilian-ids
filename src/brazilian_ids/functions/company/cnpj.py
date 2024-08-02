"""Functions to handle Brazilian company identifiers (CNPJ).

CNPJ means "Cadastro Nacional da Pessoa Jurídica" in Brazilian Portuguese.

See also a the `Wikipedia entry <https://en.wikipedia.org/wiki/CNPJ>`_ about it
for more details.
"""

from calendar import c
from http.client import EXPECTATION_FAILED
from random import randint, choice
from dataclasses import dataclass

from brazilian_ids.functions.real_state.sql import (
    EXPECTED_DIGITS,
    EXPECTED_DIGITS_WITHOUT_VERIFICATION,
)
from brazilian_ids.functions.util import NONDIGIT_REGEX
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError


class InvalidCnpjTypeMixin:
    """Mixin class for CNPJ errors."""

    def id_type(self):
        return "CNPJ"


class InvalidCnpjError(InvalidCnpjTypeMixin, InvalidIdError):
    def __init__(self, cnpj: str) -> None:
        super().__init__(id=cnpj)


class InvalidCnpjLengthError(InvalidCnpjTypeMixin, InvalidIdLengthError):
    def __init__(
        self, cnpj: str, expected_digits: int = EXPECTED_DIGITS_WITHOUT_VERIFICATION
    ) -> None:
        super().__init__(id=cnpj, expected_digits=expected_digits)


@dataclass
class CNPJ:
    """Representation of a CNPJ.

    The attributes are as follow:

    - cnpj: the formatted CNPJ. Also returned from ``__str__``.
    - firm: the number of the firm/company, as registered at Receita Federal.
    - establishment: the sequence number
    - first_digit: the first verification digit
    - second_digit: the second verification digit

    Should be obtained from the ``parse`` function."""

    cnpj: str
    firm: int
    establishment: int
    first_digit: int
    second_digit: int

    def __str__(self):
        return self.cnpj


CNPJ_FIRST_WEIGHTS = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
CNPJ_SECOND_WEIGHTS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
EXPECTED_DIGITS = 14
EXPECTED_DIGITS_WITHOUT_VERIFICATION = 12


def is_valid(cnpj: str, autopad: bool = True) -> bool:
    """Check whether CNPJ is valid. Optionally pad if is too short."""
    cnpj = NONDIGIT_REGEX.sub("", cnpj)

    if len(cnpj) < EXPECTED_DIGITS:
        if not autopad:
            return False
        cnpj = pad(cnpj)

    elif len(cnpj) > EXPECTED_DIGITS:
        return False

    # 0 is invalid; smallest valid CNPJ is 191
    if cnpj == "00000000000000":
        return False

    digits = [int(k) for k in cnpj[:13]]  # identifier digits
    # validate the first check digit
    cs = sum(w * k for w, k in zip(CNPJ_FIRST_WEIGHTS, digits[:-1])) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != int(cnpj[12]):
        return False  # first check digit is not correct
    # validate the second check digit
    cs = sum(w * d for w, d in zip(CNPJ_SECOND_WEIGHTS, digits)) % 11
    cs = 0 if cs < 2 else 11 - cs
    if cs != int(cnpj[13]):
        return False  # second check digit is not correct
    # both check digits are correct
    return True


def verification_digits(cnpj: str) -> tuple[int, int]:
    """Find two check digits needed to make a CNPJ valid."""
    cnpj = NONDIGIT_REGEX.sub("", cnpj)

    if len(cnpj) < EXPECTED_DIGITS_WITHOUT_VERIFICATION:
        raise InvalidCnpjLengthError(cnpj=cnpj)

    digits = [int(k) for k in cnpj[:13]]
    # find the first check digit
    cs = sum(w * d for w, d in zip(CNPJ_FIRST_WEIGHTS, digits)) % 11
    check = 0 if cs < 2 else 11 - cs
    # find the second check digit
    digits.append(check)
    cs = sum(w * k for w, k in zip(CNPJ_SECOND_WEIGHTS, digits)) % 11
    if cs < 2:
        return (check, 0)
    return (check, 11 - cs)


def from_firm_id(
    firm: str, establishment: str = "0001", formatted: bool = False
) -> str:
    """Takes first 8 digits of a CNPJ (firm identifier) and builds a valid,
    complete CNPJ by appending an establishment identifier and calculating
    necessary check digits.
    """
    firm = NONDIGIT_REGEX.sub("", firm)
    cnpj = "{0}{1}".format(firm, establishment)
    digits = "".join([str(k) for k in verification_digits(cnpj)])

    if not formatted:
        return cnpj + digits
    else:
        return format(cnpj + digits)


def format(cnpj: str) -> str:
    """Applies typical 00.000.000/0000-00 formatting to CNPJ."""
    cnpj = pad(cnpj)
    fmt = "{0}.{1}.{2}/{3}-{4}"
    return fmt.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])


def pad(cnpj: str, validate_after: bool = False) -> str:
    """Takes a CNPJ and pads it with leading zeros."""
    padded = "%0.014i" % int(cnpj)

    if validate_after:
        if not is_valid(padded):
            raise InvalidCnpjError(cnpj)

    return padded


def parse(cnpj: str) -> CNPJ:
    """Split CNPJ into firm, establishment and check digits.

    Additionally, the CNPJ is also padded and validated before returning.
    """
    cnpj = NONDIGIT_REGEX.sub("", cnpj)
    cnpj = pad(cnpj=cnpj, validate_after=True)
    firm = int(cnpj[:8])
    establishment = int(cnpj[8:12])
    first = int(cnpj[-2])
    second = int(cnpj[-1])

    return CNPJ(
        cnpj=format(cnpj),
        firm=firm,
        establishment=establishment,
        first_digit=first,
        second_digit=second,
    )


def random(formatted: bool = True) -> str:
    """Create a random, valid CNPJ identifier."""
    firm = str(randint(10000000, 99999999))
    establishment = choice(["0001", "0002", "0003", "0004", "0005"])

    if formatted:
        return format(from_firm_id(firm, establishment))

    return from_firm_id(firm, establishment)
