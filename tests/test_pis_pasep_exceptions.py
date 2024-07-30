from brazilian_ids.functions.person.pis_pasep import (
    InvalidPISPASEPLengthError,
    InvalidPISPASEPError,
)
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError


def test_invalid_pis_error_class():
    assert issubclass(InvalidPISPASEPError, InvalidIdError)


def test_invalid_pis_pasep_length_error_class():
    assert issubclass(InvalidPISPASEPLengthError, InvalidIdLengthError)


def test_invalid_pis_pasep_length_error_instance():
    instance = InvalidPISPASEPLengthError("1234")
    assert (
        str(instance) == "A PIS/PASEP must have at least 10 digits, '1234' has only 4"
    )
