from brazilian_ids.functions.labor_dispute.nupj import (
    InvalidCourtIdError,
    InvalidNupjError,
    InvalidSegmentIdError,
    InvalidNupjTypeMixin,
)
from brazilian_ids.functions.exceptions import InvalidIdError


def test_invalid_court_id_error():
    assert issubclass(InvalidCourtIdError, ValueError)


def test_invalid_court_id_error_instance():
    instance = InvalidCourtIdError("99")
    assert isinstance(instance, InvalidCourtIdError)
    assert hasattr(instance, "id")
    assert instance.id == "99"


def test_invalid_nupj_error():
    assert issubclass(InvalidNupjError, InvalidIdError)
    assert issubclass(InvalidNupjError, InvalidNupjTypeMixin)


def test_invalid_nupj_error_instance():
    instance = InvalidNupjError("1234")
    assert isinstance(instance, InvalidNupjError)
    assert hasattr(instance, "id")
    assert hasattr(instance, "id_type")


def test_invalid_segment_id_error():
    assert issubclass(InvalidSegmentIdError, ValueError)


def test_invalid_segment_id_error_instance():
    instance = InvalidSegmentIdError("99")
    assert isinstance(instance, InvalidSegmentIdError)
    assert hasattr(instance, "id")
    assert instance.id == "99"
