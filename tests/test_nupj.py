import pytest

from brazilian_ids.functions.labor_dispute.nupj import (
    is_valid,
    parse,
    pad,
    NUPJ,
    Court,
    Courts,
)

# NUPJ generator
# https://processogerador.paulosales.com.br/


@pytest.mark.parametrize("nupj", ("62367378320244025398", "7666699020243004820"))
def test_is_valid(nupj):
    assert is_valid(nupj)


@pytest.mark.parametrize(
    "nupj", ("6236737-83.2024.4.02.5398", "766669-90.2024.3.00.4820")
)
def test_is_valid_formatted(nupj):
    assert is_valid(nupj)


@pytest.mark.parametrize(
    "given,expected",
    (("766669-90.2024.3.00.4820", "07666699020243004820"),),
)
def test_pad(given, expected):
    assert pad(given) == expected


@pytest.mark.parametrize(
    "given,expected",
    (
        (
            "6236737-83.2024.4.02.5398",
            NUPJ(
                lawsuit_id="6236737",
                first_digit=8,
                second_digit=3,
                year=2024,
                segment=4,
                court_id="02",
                lawsuit_city="5398",
            ),
        ),
        (
            "766669-90.2024.3.00.4820",
            NUPJ(
                lawsuit_id="0766669",
                first_digit=9,
                second_digit=0,
                year=2024,
                segment=3,
                court_id="00",
                lawsuit_city="4820",
            ),
        ),
    ),
)
def test_parse(given, expected):
    assert parse(given) == expected
