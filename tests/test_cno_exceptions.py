from brazilian_ids.functions.real_state.cno import (
    InvalidCnoError,
    InvalidCnoLengthError,
)
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError


def test_invalid_cno_error_class():
    issubclass(InvalidCnoError, InvalidIdError)


def test_invalid_cno_error_instance():
    instance = InvalidCnoError("1234")
    hasattr(instance, "id")
    hasattr(instance, "id_type")


def test_invalid_cno_error_length_class():
    issubclass(InvalidCnoLengthError, InvalidIdLengthError)


def test_invalid_cno_error_length_instance():
    instance = InvalidCnoLengthError(cno="1234")
    hasattr(instance, "id")
    hasattr(instance, "id_type")
    hasattr(instance, "expected_length")
