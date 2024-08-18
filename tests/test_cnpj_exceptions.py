import pytest

from brazilian_ids.functions.company.cnpj import (
    InvalidCnpjError,
    InvalidCnpjLengthError,
    EXPECTED_DIGITS_WITHOUT_VERIFICATION,
)
from brazilian_ids.functions.exceptions import InvalidIdError, InvalidIdLengthError


@pytest.mark.parametrize(
    "parent,child",
    (
        (InvalidCnpjError, InvalidIdError),
        (InvalidCnpjLengthError, InvalidIdLengthError),
    ),
)
def test_invalid_class(parent, child):
    assert issubclass(parent, child)


@pytest.mark.parametrize(
    "klass,error_piece",
    (
        (InvalidCnpjError, "invalid"),
        (InvalidCnpjLengthError, str(EXPECTED_DIGITS_WITHOUT_VERIFICATION)),
    ),
)
def test_instance(klass, error_piece):
    invalid_id = "1234"
    instance = klass(invalid_id)
    assert isinstance(instance, klass)
    assert hasattr(instance, "id_type")
    assert instance.id_ == invalid_id
    assert instance.id_type() == "CNPJ"
    assert str(instance).find(error_piece) != -1
