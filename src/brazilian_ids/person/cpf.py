"""Functions to handle a CPF."""

import random

from brazilian_ids.util import clean_id, NONDIGIT_REGEX


CPF_WEIGHTS = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class InvalidCPFError(ValueError):
    """Exception for an invalid CPF."""

    def __init__(self, cpf: str, message: None | str = None):
        self.cpf = cpf

        if message is None:
            msg = f"The CPF '{cpf}' is invalid"
        else:
            msg = message
        super().__init__(msg)


class InvalidCPFLenghtError(InvalidCPFError):
    """Exception for an invalid CPF with less than 9 digits."""

    def __init__(self, cpf: str):
        msg = "A CPF must have at least 9 digits, '{0}' has only {1}".format(
            cpf, len(cpf)
        )
        super().__init__(cpf=cpf, message=msg)


def is_cpf_valid(cpf: str, autopad: bool = True):
    """Check whether CPF is valid."""
    cpf = clean_id(cpf)

    # all complete CPF are 11 digits long
    if len(cpf) < 11:
        if not autopad:
            return False

        cpf = pad_cpf(cpf)

    elif len(cpf) > 11:
        return False

    if cpf == "00000000000":
        return False

    digits = [int(k) for k in cpf]  # identifier digits
    # validate the first check digit
    cs = (sum(w * k for w, k in zip(CPF_WEIGHTS, digits[:-2])) % 11) % 10

    if cs != digits[-2]:
        return False  # first check digit is not correct

    # validate the second check digit
    cs = (sum(w * k for w, k in zip(CPF_WEIGHTS, digits[1:-1])) % 11) % 10

    if cs != digits[-1]:
        return False  # second check digit is not correct

    # both check digits are correct
    return True


def verification_digits(cpf: str) -> tuple[int, int]:
    """Find the two check digits that are required to make a CPF valid.

    If the length of the CPF is less than 9 characters, the
    InvalidCPFLengthError is raised.
    """
    cpf = clean_id(cpf)

    if len(cpf) < 9:
        raise InvalidCPFLenghtError(cpf)

    digits = [int(k) for k in cpf[:10]]
    # find the first check digit
    cs = (sum(w * k for w, k in zip(CPF_WEIGHTS, digits)) % 11) % 10
    # find the second check digit
    digits.append(cs)
    return (cs, ((sum(w * k for w, k in zip(CPF_WEIGHTS, digits[1:])) % 11) % 10))


def format(cpf: str) -> str:
    """Applies the typical 000.000.000-00 formatting to CPF."""
    cpf = pad_cpf(cpf)
    fmt = "{0}.{1}.{2}-{3}"
    return fmt.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])


def pad_cpf(cpf: str) -> str:
    """Takes a CPF that has leading zeros and pads it.

    If the given CPF is invalid, the ``InvalidCPFError`` exception is raised.
    """
    padded = "%0.011i" % int(cpf)

    if not is_cpf_valid(cpf=cpf, autopad=False):
        raise InvalidCPFError(cpf)

    return padded


def random_cpf(formatted: bool = True) -> str:
    """Create a random, valid CPF identifier."""
    stem = str(random.randint(100000000, 999999999))
    digits = verification_digits(stem)
    cpf = "{0}{1}{2}".format(stem, digits[0], digits[1])

    if formatted:
        return format(cpf)
    return cpf
