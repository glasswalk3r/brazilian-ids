from brazilian_ids.functions.exceptions import InvalidIdLengthError
from brazilian_ids.functions.location.municipio import (
    InvalidMunicipioLengthError,
    InvalidMunicipioFederalUnitError,
)


def test_invalid_municipio_length_error():
    assert issubclass(InvalidMunicipioLengthError, InvalidIdLengthError)


def test_invalid_municipio_length_error_instance():
    invalid_municipio = "1234"
    instance = InvalidMunicipioLengthError(invalid_municipio)
    assert isinstance(instance, InvalidMunicipioLengthError)
    assert hasattr(instance, "id_")
    assert hasattr(instance, "id_type")
    assert instance.id_ == invalid_municipio
    assert instance.id_type() == "município"
    assert str(instance).find("4") != -1


def test_invalid_mun_fed_unit_error():
    assert issubclass(InvalidMunicipioFederalUnitError, ValueError)


def test_invalid_mun_fed_unit_error_instance():
    invalid = "1812333"
    instance = InvalidMunicipioFederalUnitError(invalid)
    assert isinstance(instance, InvalidMunicipioFederalUnitError)
    assert hasattr(instance, "code")
    assert instance.code == invalid
