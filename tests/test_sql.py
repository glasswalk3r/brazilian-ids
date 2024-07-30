import pytest

from brazilian_ids.functions.real_state.sql import (
    InvalidSqlLengthError,
    format,
    pad,
    is_valid,
    verification_digit,
    EXPECTED_DIGITS,
)


def test_format():
    assert format("27100300205") == "271.003.0020-5"


def test_format_padded():
    assert format("00100300022") == "001.003.0002-2"


def test_pad():
    assert pad("100300022") == "00100300022"


def test_pad_formatted():
    assert pad("001.003.0002-2") == "00100300022"


def test_is_valid():
    assert is_valid("27100300205")


@pytest.mark.parametrize(
    "sql,expected_digit",
    [("27100300205", "5"), ("00100300022", "2"), ("100300022", "2")],
)
def test_verification_digit(sql, expected_digit):
    if len(sql) < EXPECTED_DIGITS:
        sql = pad(sql)

    assert verification_digit(sql) == expected_digit


@pytest.mark.parametrize(
    "sql,expected_digit",
    [("27100300205", "5"), ("00100300022", "2")],
)
def test_verification_digit_with_length_validated(sql, expected_digit):
    assert verification_digit(sql=sql, validate_length=True) == expected_digit


def test_verification_digit_with_exception():
    with pytest.raises(InvalidSqlLengthError):
        assert verification_digit("100300022", True)
