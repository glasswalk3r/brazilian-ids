import pytest

from brazilian_ids.functions.real_state.sql import (
    InvalidSqlError,
    InvalidSqlLengthError,
    EXPECTED_DIGITS,
)
from brazilian_ids.functions.exceptions import InvalidIdLengthError, InvalidIdError


@pytest.fixture
def invalid_sql():
    return "1234"


def test_invalid_sql_error_class():
    assert issubclass(InvalidSqlError, InvalidIdError)


def test_invalid_sql_error_instance(invalid_sql):
    instance = InvalidSqlError(invalid_sql)
    assert isinstance(instance, InvalidSqlError)
    assert hasattr(instance, "id_")
    assert hasattr(instance, "id_type")
    assert instance.id_type() == "SQL"
    assert instance.id_ == invalid_sql


def test_invalid_sql_length_error_class():
    assert issubclass(InvalidSqlLengthError, InvalidIdLengthError)


def test_invalid_sql_length_error_instance(invalid_sql):
    instance = InvalidSqlLengthError(sql=invalid_sql, expected_digits=EXPECTED_DIGITS)
    assert isinstance(instance, InvalidSqlLengthError)
    assert hasattr(instance, "id_")
    assert hasattr(instance, "id_type")
    assert instance.id_type() == "SQL"
    assert instance.id_ == invalid_sql
