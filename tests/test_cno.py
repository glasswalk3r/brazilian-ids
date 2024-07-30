import pytest
from brazilian_ids.functions.real_state.cno import (
    InvalidCnoLengthError,
    random,
    is_valid,
    format,
    verification_digit,
    pad,
    InvalidCnoError,
)


@pytest.fixture
def cno_sample():
    return "352386646120"


@pytest.fixture
def cno_formatted_sample():
    return "35.238.66461/20"


def test_validate(cno_sample):
    assert is_valid(cno_sample)


def test_validate_formatted(cno_formatted_sample):
    assert is_valid(cno_formatted_sample)


def test_validate_too_long(cno_sample):
    assert not is_valid(cno_sample * 2)


def test_random():
    cno = random(formatted=False)
    assert is_valid(cno)


def test_random_formatted():
    cno = random(formatted=True)
    assert is_valid(cno)


def test_format(cno_sample, cno_formatted_sample):
    assert format(cno_sample) == cno_formatted_sample


def test_verification_digit(cno_sample):
    assert verification_digit(cno_sample[:-1]) == int(cno_sample[-1:])


def test_verification_digit_raises_exception():
    with pytest.raises(InvalidCnoLengthError):
        verification_digit("1234567891", validate_length=True)


def test_pad():
    assert pad("1233456789") == "001233456789"


def test_pad_with_validation():
    assert pad("1233456782", validate_after=True) == "001233456782"


def test_pad_raises_exception():
    with pytest.raises(InvalidCnoError):
        assert pad("1233456789", validate_after=True)
