import pytest

from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError
from brazilian_ids.functions.location.municipio import (
    InvalidMunicipioError,
    InvalidMunicipioLengthError,
)


@pytest.fixture
def invalid_municipio():
    return "1234"


def test_invalid_municipio_error():
    assert issubclass(InvalidMunicipioError, InvalidIdError)


def test_invalid_municipio_error_instance(invalid_municipio):
    instance = InvalidMunicipioError(invalid_municipio)
    assert isinstance(instance, InvalidMunicipioError)
    assert hasattr(instance, "id")
    assert hasattr(instance, "id_type")
    assert instance.id == invalid_municipio
    assert instance.id_type() == "município"


def test_invalid_municipio_length_error():
    assert issubclass(InvalidMunicipioLengthError, InvalidIdLengthError)


def test_invalid_municipio_length_error_instance(invalid_municipio):
    instance = InvalidMunicipioLengthError(invalid_municipio)
    assert isinstance(instance, InvalidMunicipioLengthError)
    assert hasattr(instance, "id")
    assert hasattr(instance, "id_type")
    assert instance.id == invalid_municipio
    assert instance.id_type() == "município"
    assert str(instance).find("4") != -1
