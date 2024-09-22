"""Functions to work with CEP ("Código de Endereçamento Postal", in Brazilian
Portuguese), which is the equivalent of zipcodes.

The meaning of numeric codes for region, sub region, etc, are in strict control
of a private company in Brazil called Correios. The company has the monopoly in

Brazil and doesn't provide data besides simply queries with limited results and
restricted by captchas to making data scraping more difficult.

See also:

- `Correios <https://pt.wikipedia.org/wiki/Empresa_Brasileira_de_Correios_e_Tel%C3%A9grafos>`_
- `CEP <https://pt.wikipedia.org/wiki/C%C3%B3digo_de_Endere%C3%A7amento_Postal>`_
"""

from dataclasses import dataclass
from typing import Generator

from brazilian_ids.functions.exceptions import InvalidIdError


@dataclass(frozen=True, slots=True, repr=False)
class CEP:
    """Representation of a CEP.

    Should be obtained from the ``parse`` function.
    """

    formatted_cep: str
    region: int
    sub_region: int
    sector: int
    sub_sector: int
    division: int
    suffix: str

    def __repr__(self):
        return self.formatted_cep

    def __ge__(self, other):
        test_sequence = ("region", "sub_region", "sub_sector", "division")

        for digit in test_sequence:
            if getattr(self, digit) > getattr(other, digit):
                return True
            elif getattr(self, digit) == getattr(other, digit):
                continue
            else:
                return False

        a = int(self.suffix)
        b = int(other.suffix)

        return a >= b

    def __le__(self, other):
        test_sequence = ("region", "sub_region", "sub_sector", "division")

        for digit in test_sequence:
            if getattr(self, digit) < getattr(other, digit):
                return True
            elif getattr(self, digit) == getattr(other, digit):
                continue
            else:
                return False

        a = int(self.suffix)
        b = int(other.suffix)

        return a <= b


class Singleton(type):
    """Implement the singleton pattern."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CepInvalidStateError(ValueError):
    """Error for CEP associated with a invalid state code."""
    def __init__(self, state_code):
        super().__init__(f"The state '{state_code}' does not exist")
        self.state_code = state_code


class CepRange(metaclass=Singleton):
    """Representation of all the CEPs range by state, as documented by Correios."""
    __slots__ = "__ranges"

    def __init__(self):
        self.__ranges = {
            "SP": ("01000-000", "05999-999"),
            "RJ": ("20000-000", "28999-999"),
            "MG": ("30000-000", "39999-999"),
            "BA": ("40000-000", "48999-999"),
            "RS": ("90000-000", "99999-999"),
            "CE": ("60000-000", "63999-999"),
            "PE": ("50000-000", "55999-999"),
            "PB": ("58000-000", "58999-999"),
            "MA": ("65000-000", "65999-999"),
            "AL": ("57000-000", "57999-999"),
            "SE": ("49000-000", "49999-999"),
            "GO": ("74000-000", "76999-999"),
            "DF": ("70000-000", "71999-999"),
            "TO": ("77000-000", "77999-999"),
            "PA": ("66000-000", "68899-999"),
            "AM": ("69000-000", "69299-999"),
            "AP": ("68900-000", "68999-999"),
            "RR": ("69300-000", "69399-999"),
            "MT": ("78000-000", "78899-999"),
            "MS": ("79000-000", "79999-999"),
            "PI": ("64000-000", "64999-999"),
            "SC": ("88000-000", "88999-999"),
            "ES": ("29000-000", "29999-999"),
        }

    def ranges_by_state(self, state: str) -> tuple[CEP, CEP]:
        """Return the a pair of CEPs related to a given state code.

        See ``brazilian_ids.functions.location.states`` module for all valid states codes.
        """
        if state not in self.__ranges:
            raise CepInvalidStateError(state)

        pair = self.__ranges[state]
        return (parse(pair[0]), parse(pair[1]))

    def all_ranges(self) -> Generator[tuple[CEP, CEP], None, None]:
        """Go through all the CEP ranges per state, returning a pair ``CEP`` instances, where the index 0 is the
        first CEP in the range and the index 2 the last one.
        """
        for start, end in self.__ranges.values():
            yield (parse(start), parse(end))

    def __repr__(self):
        return "{0}, total of ranges: {1}".format(self.__class__.__name__, len(self.__ranges))


def is_valid(cep: str, raw: bool = False, digits: int = 0) -> bool:
    """Check if a CEP is valid or not.

    The ``raw`` parameter is a small optimization: if you're sure that the CEP string only contains numbers, then you
    you can skip one of the steps required to validate it. If you're unsure, just use the default value.

    The ``digits`` parameter is also used to skip one of the validations steps, if you already know before hand the
    length of the ``cep`` string (for any reason). Of course, if you didn't need this information elsewhere, there is
    use to do ``len(cep)`` before calling this function and passing the result as ``digits``.
    """
    if not raw:
        cep = cep.replace("-", "")

    if digits == 0:
        digits = len(cep)

    expected = set([4, 5, 7, 8])
    return digits in expected


def is_valid_extended(cep: str, raw: bool = False, digits: int = 0, state: str | None=None) -> bool:
    """Check if a CEP is valid or not.

    This function does everything that ``is_valid`` function does, plus some additional verifications that will take a
    longer time to finish.

    Those verifications are not perfect, since Correios doesn't allow anymore online verifications, but it does rely
    on published information that is still public.

    If you're are able to inform the ``state`` that you believe the CEP should be part of, then that will speed up the
    validation process.
    """
    if not is_valid(cep=cep, raw=raw, digits=digits):
        return False

    ranges = CepRange()
    candidate = parse(cep)

    if state is not None:
        start, end = ranges.ranges_by_state(state)
        return candidate >= start and candidate <= end

    for start, end in ranges.all_ranges():
        if candidate >= start and candidate <= end:
            return True

    return False

class InvalidCepError(InvalidIdError):
    """Exception for an invalid CEP."""
    def id_type(self, cep: str):
        return f"Invalid CEP code '{cep}'"


def format(cep: str) -> str:
    """Applies typical 00000-000 formatting to CEP."""
    cep = cep.replace("-", "")
    total_digits = len(cep)

    if not is_valid(cep=cep, raw=False, digits=total_digits):
        raise InvalidCepError(cep)

    if total_digits == 4 or total_digits == 5:
        cep = "0" * (5 - total_digits) + cep + "000"
    else:
        cep = "0" * (8 - total_digits) + cep

    return "{0}-{1}".format(cep[:-3], cep[-3:])


def parse(cep: str) -> CEP:
    """Split a CEP into region, sub-region, sector, subsector, division."""
    fmtcep = format(cep)
    geo = [fmtcep[:i] for i in range(1, 6)]
    suffix = fmtcep[-3:]

    return CEP(
        formatted_cep=fmtcep,
        region=int(geo[0]),
        sub_region=int(geo[1]),
        sector=int(geo[2]),
        sub_sector=int(geo[3]),
        division=int(geo[4]),
        suffix=suffix,
    )
