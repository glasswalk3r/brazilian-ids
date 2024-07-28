"""Functions to handle Brazilian PIS/PASEP identifiers."""

from random import randint

from brazilian_ids.functions.util import NONDIGIT_REGEX


class InvalidPISPASEPError(ValueError):
    def __init__(self, pis_pasep: str):
        msg = f"The PIS/PASEP '{pis_pasep}' is invalid"
        self.pis_pasep = pis_pasep
        super().__init__(msg)


class InvalidPISPASEPLengthError(ValueError):
    def __init__(self, pis_pasep: str):
        msg = "The PIS/PASEP '{0}' {1} length is incorrect: got {2}, expect 10 digits".format(
            pis_pasep, "(without the verification digit)", len(pis_pasep)
        )
        self.pis_pasep = pis_pasep
        super().__init__(msg)


def is_valid(pis_pasep: str, autopad: bool = True) -> bool:
    """Check whether PIS/PASEP is valid. Optionally pad if too short."""
    pis_pasep = NONDIGIT_REGEX.sub("", pis_pasep)

    # all complete PIS/PASEP are 11 digits long
    if len(pis_pasep) < 11:
        if not autopad:
            return False
        pis_pasep = pad(pis_pasep)

    elif len(pis_pasep) > 11:
        return False

    if pis_pasep == "00000000000":
        return False

    return int(pis_pasep[-1]) == validation_digit(pis_pasep)


def validation_digit(pis_pasep: str) -> int:
    """Calculate the validation (last) digit required to make a PIS/PASEP
    valid."""
    pis_pasep = NONDIGIT_REGEX.sub("", pis_pasep)
    pis_weights = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    if len(pis_pasep) < 10:
        raise InvalidPISPASEPLengthError(pis_pasep)

    digits = [int(k) for k in pis_pasep[:11]]

    # find check digit
    result = sum(w * k for w, k in zip(pis_weights, digits)) % 11

    if result < 2:
        return 0

    return 11 - result


def format(pis_pasep: str) -> str:
    """Applies the format '000.0000.000-0' to a PIS/PASEP."""
    pis_pasep = pad(pis_pasep)
    return "{0}.{1}.{2}-{3}".format(
        pis_pasep[:3], pis_pasep[3:7], pis_pasep[7:10], pis_pasep[10]
    )


def pad(pis_pasep: str, validate: bool = False) -> str:
    """Takes a PIS/PASEP that should have leading zeros and pads it."""
    padded = str("%0.011i" % int(pis_pasep))

    if validate:
        if is_valid(padded):
            return padded
        raise InvalidPISPASEPError(padded)

    return padded


def random(formatted=True):
    """Create a random, valid PIS identifier."""
    result = str(randint(1000000000, 9999999999))
    pis_pasep = result + str(validation_digit(result))

    if formatted:
        return format(pis_pasep)
    return pis_pasep
