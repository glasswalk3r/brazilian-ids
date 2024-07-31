import pytest

from brazilian_ids.functions.company.cnpj import (
    is_valid,
    verification_digits,
    pad,
    format,
    parse,
    random,
    from_firm_id,
)


@pytest.mark.parametrize(
    "cnpj",
    (
        "60746948000112",
        "60701190000104",
        "00360305000104",
        "61472676000172",
        "58160789000128",
    ),
)
def test_is_valid(cnpj):
    assert is_valid(cnpj)


@pytest.mark.parametrize(
    "cnpj",
    (
        "60.746.948/0001-12",
        "60.701.190/0001-04",
        "00.360.305/0001-04",
        "61.472.676/0001-72",
        "58.160.789/0001-28",
    ),
)
def test_is_valid_formatted(cnpj):
    assert is_valid(cnpj)


@pytest.mark.parametrize(
    "cnpj,pair",
    (
        ("607469480001", (1, 2)),
        ("607011900001", (0, 4)),
        ("003603050001", (0, 4)),
        ("614726760001", (7, 2)),
        ("581607890001", (2, 8)),
    ),
)
def test_verification_digits(cnpj, pair):
    assert verification_digits(cnpj) == pair


def test_pad():
    assert pad("360305000104") == "00360305000104"


def test_format():
    assert format("58160789000128") == "58.160.789/0001-28"


def test_parse_formatted():
    sample = "58.160.789/0001-28"
    cnpj = parse(sample)
    assert cnpj.cnpj == sample
    assert str(cnpj) == sample
    assert cnpj.firm == 58160789
    assert cnpj.establishment == 1
    assert cnpj.first_digit == 2
    assert cnpj.second_digit == 8


def test_random():
    sample = random(formatted=False)
    assert is_valid(sample)
    assert sample.find(".") == -1
    assert sample.find("/") == -1


def test_random_formatted():
    sample = random(formatted=True)
    assert is_valid(sample)
    assert sample.find(".") != -1
    assert sample.find("/") != -1


@pytest.mark.parametrize(
    "firm_id,establishment,expected",
    (("60746948", "0001", "60746948000112"), ("6070119", "00001", "60701190000104")),
)
def test_from_firm_id(firm_id, establishment, expected):
    assert from_firm_id(firm=firm_id, establishment=establishment) == expected


@pytest.mark.parametrize(
    "firm_id,establishment,expected",
    (
        ("60746948", "0001", "60.746.948/0001-12"),
        ("6070119", "00001", "60.701.190/0001-04"),
    ),
)
def test_from_firm_id_formatted(firm_id, establishment, expected):
    assert (
        from_firm_id(firm=firm_id, establishment=establishment, formatted=True)
        == expected
    )


def test_from_firm_id_default_establishment():
    assert from_firm_id("58160789") == "58160789000128"
