"""Functions to handle Brazilian município (county) codes.

Although the municipio code has a verification digit, there are 9 known codes
where those digits are invalid.

This module contains those municipio codes in the ``INVALID`` dict, but they can
also be verified at
http://www.sefaz.al.gov.br/nfe/notas_tecnicas/NT2008.004.pdf.
"""

from brazilian_ids.functions.real_state.sql import (
    EXPECTED_DIGITS,
    EXPECTED_DIGITS_WITHOUT_VERIFICATION,
)
from brazilian_ids.functions.util import NONDIGIT_REGEX
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError


class InvalidMunicipioTypeMixin:
    """Mixin class for município errors."""

    def id_type(self):
        return "município"


class InvalidMunicipioError(InvalidMunicipioTypeMixin, InvalidIdError):
    """Exception for invalid município errors"""

    def __init__(self, municipio: str) -> None:
        super().__init__(id=municipio)


class InvalidMunicipioLengthError(InvalidMunicipioTypeMixin, InvalidIdLengthError):
    """Exception for invalid município length error."""

    def __init__(
        self,
        municipio: str,
        expected_digits: int = EXPECTED_DIGITS_WITHOUT_VERIFICATION,
    ) -> None:
        super().__init__(id=municipio, expected_digits=expected_digits)


INVALID = {
    "2201919": 9,  # Bom Princípio do Piauí, PI
    "2201988": 8,  # Brejo do Piauí, PI
    "2202251": 1,  # Canavieira, PI
    "2611533": 3,  # Quixaba, PE
    "3117836": 6,  # Cônego Marinho, MG
    "3152131": 1,  # Ponto Chique, MG
    "4305871": 1,  # Coronel Barros, RS
    "5203939": 9,  # Buriti de Goiás, GO
    "5203962": 2,  # Buritinópolis, GO
}

EXPECTED_DIGITS = 7
EXPECTED_DIGITS_WITHOUT_VERIFICATION = 6


def is_valid(municipio: str) -> bool:
    """Check whether município code is valid."""
    municipio = NONDIGIT_REGEX.sub("", municipio)

    if len(municipio) != EXPECTED_DIGITS:
        return False

    if municipio[0] == "0":
        return False

    valid = verification_digit(municipio[:-1]) == municipio[-1]
    return valid or municipio in INVALID  # need to check exceptions list


def verification_digit(municipio: str, validate_length: bool = False) -> int:
    """Calculate the verification digit needed to make a valid municipio code."""
    municipio = NONDIGIT_REGEX.sub("", municipio)

    if validate_length:
        if len(municipio) < EXPECTED_DIGITS_WITHOUT_VERIFICATION:
            raise InvalidMunicipioLengthError(municipio)

    if municipio in INVALID:
        return INVALID[municipio]

    digits = [int(k) for k in municipio[:7]]
    weights = [1, 2, 1, 2, 1, 2]
    digmul = (w * d for w, d in zip(weights, digits))
    digsum = sum(n if n < 10 else 1 + (n % 10) for n in digmul)
    modulo = digsum % 10

    if modulo == 0:
        return 0

    return 10 - modulo
