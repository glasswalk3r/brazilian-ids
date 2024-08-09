import pytest

from brazilian_ids.functions.location.municipio import (
    Municipio,
    is_valid,
    INVALID,
    parse,
)


@pytest.mark.parametrize("county", [county for county in INVALID.keys()])
def test_is_valid_with_exceptions(county):
    assert is_valid(county)


@pytest.mark.parametrize("county", ("1200013", "2900207", "2900306"))
def test_is_valid(county):
    assert is_valid(county)


@pytest.mark.parametrize("county", ("1800013", "200020", "0300306"))
def test_not_is_valid(county):
    assert not is_valid(county)


def test_parse():
    assert parse("1200013") == Municipio(
        unidade_federativa="12", municipio="000", control_digits="13"
    )
