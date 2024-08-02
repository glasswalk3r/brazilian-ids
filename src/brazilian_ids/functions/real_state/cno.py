"""Functions to handle Brazilian CNO identifier.

CNO means "Cadastro Nacional de Obras" in Brazilian Portuguese, and it is a
database that contains information about the all civilian real state
constructions and can be associate with a person (CPF) or a company (CNPJ).

The CNO ID replaces the old CEI (Cadastro Específico do INSS) ID, but basically
the functions are the same.

See also:

- `CEI <https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/cei>`_
- `CNO <http://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=122299#2314933>`_
"""

from random import randint

from brazilian_ids.functions.util import NONDIGIT_REGEX
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError


class InvalidCnoTypeMixin:
    """Mixin class for CNO errors."""

    def id_type(self):
        return "CNO"


class InvalidCnoError(InvalidCnoTypeMixin, InvalidIdError):
    """Exception for invalid CNO errors"""

    def __init__(self, cno: str) -> None:
        super().__init__(id=cno)


class InvalidCnoLengthError(InvalidCnoTypeMixin, InvalidIdLengthError):
    """Exception for invalid CNO length error."""

    def __init__(self, cno: str, expected_digits: int = 11) -> None:
        super().__init__(id=cno, expected_digits=expected_digits)


def is_valid(cno: str, autopad: bool = True) -> bool:
    """Check whether CEI is valid. Optionally pad if too short."""
    cno = NONDIGIT_REGEX.sub("", cno)

    # all complete CEI are 12 digits long
    if len(cno) < 12:
        if not autopad:
            return False
        cei = pad(cno)

    elif len(cno) > 12:
        return False

    if cno == "000000000000":
        return False

    digits = [int(k) for k in cno]  # identifier digits
    return verification_digit(str(digits[:-1])) == digits[-1]


def verification_digit(cno: str, validate_length: bool = False) -> int:
    """Calculate check digit from iterable of integers."""
    cno = NONDIGIT_REGEX.sub("", cno)

    if validate_length and len(cno) < 11:
        raise InvalidCnoLengthError(cno=cno)

    digits = [int(k) for k in cno[:12]]
    cei_weights = [7, 4, 1, 8, 5, 2, 1, 6, 3, 7, 4]
    digsum = sum(w * k for w, k in zip(cei_weights, digits))
    mod = sum(divmod(digsum % 100, 10)) % 10

    if mod == 0:
        return 0

    return 10 - mod


def format(cno: str) -> str:
    """Applies typical 00.000.00000/00 formatting to CEI."""
    cno = pad(cno)
    fmt = "{0}.{1}.{2}/{3}"
    return fmt.format(cno[:2], cno[2:5], cno[5:10], cno[10:])


def pad(cno: str, validate_after=False) -> str:
    """Takes a CEI that probably had leading zeros and pads it."""
    padded = "%0.012i" % int(cno)

    if validate_after:
        if is_valid(padded):
            return padded
        else:
            raise InvalidCnoError(cno)
    return padded


def random(formatted: bool = True) -> str:
    """Create a random, valid CNO identifier."""
    uf = randint(11, 53)
    stem = "{0}{1}".format(uf, randint(100000000, 999999999))
    cno = "{0}{1}".format(stem, verification_digit(stem))

    if formatted:
        return format(cno)
    return cno
