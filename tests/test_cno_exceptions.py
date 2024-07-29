from brazilian_ids.functions.real_state.cno import (
    InvalidCNOError,
    InvalidCNOLengthError,
)
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLenghtError


def test_invalid_cno_error_class():
    issubclass(InvalidCNOError, InvalidIdError)


def test_invalid_cno_error_instance():
    instance = InvalidCNOError("1234")
    hasattr(instance, "id")
    hasattr(instance, "id_type")


def test_invalid_cno_error_length_class():
    issubclass(InvalidCNOLengthError, InvalidIdLenghtError)


def test_invalid_cno_error_length_instance():
    instance = InvalidCNOLengthError(cno="1234")
    hasattr(instance, "id")
    hasattr(instance, "id_type")
    hasattr(instance, "expected_length")
