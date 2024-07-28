import pytest

from brazilian_ids.functions.person.pis_pasep import (
    random,
    format,
    validation_digit,
    pad,
    InvalidPISPASEPError,
    InvalidPISPASEPLengthError,
)


def test_random():
    result = random()
    assert result.find(".") != -1
    assert result.find("-") != -1


def test_format():
    result = format("27333549246")
    assert result == "273.3354.924-6"


def test_validation_digit():
    pis_pased = "27333549246"
    last_index = len(pis_pased)
    result = validation_digit(pis_pased[:last_index])
    assert result == int(pis_pased[-1:])


def test_validation_digit_with_exception():
    pis_pased = "273335492"
    last_index = len(pis_pased)

    with pytest.raises(InvalidPISPASEPLengthError):
        validation_digit(pis_pased[:last_index])


def test_pad():
    result = pad("27333549")
    assert isinstance(result, str)
    assert result == "00027333549"


def test_pad_with_exception():
    with pytest.raises(InvalidPISPASEPError):
        pad(pis_pasep="0000000000", validate=True)
