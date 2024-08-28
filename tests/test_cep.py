import pytest

from brazilian_ids.functions.location.cep import format, parse, CEP, is_valid


@pytest.fixture
def masp_cep():
    return "01310-200"


def test_format(masp_cep):
    assert format("01310200") == masp_cep


def test_parse(masp_cep):
    result = parse(masp_cep)
    assert isinstance(result, CEP)


def test_parse_formated(masp_cep):
    result = parse(masp_cep)
    assert isinstance(result, CEP)


def test_cep_instance(masp_cep):
    instance = CEP(
        region=0,
        sub_region=1,
        sector=3,
        sub_sector=1,
        division=0,
        suffix="200",
        formatted_cep=masp_cep,
    )

    attribs = ("region", "sub_region", "sector", "sub_sector", "division", "suffix")

    for attribute in attribs:
        assert hasattr(instance, attribute)

    assert instance.region == 0
    assert instance.sub_region == 1
    assert instance.sector == 3
    assert instance.sub_sector == 1
    assert instance.division == 0
    assert instance.suffix == "200"
    assert instance.formatted_cep == masp_cep


@pytest.mark.parametrize(
    "a, b",
    (
        ("39884-999", "39880-000"),
        ("39880-001", "39880-000"),
        ("39881-000", "39880-999"),
    ),
)
def test_cep_instances_ge_comparison(a, b):
    a_instance = parse(a)
    b_instance = parse(b)

    assert a_instance >= b_instance


@pytest.mark.parametrize(
    "a, b",
    (
        ("39880-000", "39884-999"),
        ("39880-000", "39880-001"),
        ("39880-999", "39881-000"),
    ),
)
def test_cep_instances_le_comparison(a, b):
    a_instance = parse(a)
    b_instance = parse(b)

    assert a_instance <= b_instance


def test_cep_instances_between():
    first = parse("39140-000")
    last = parse("39149-999")
    between = parse("39149-512")

    assert between >= first and between <= last


@pytest.mark.parametrize("valid_cep", ("39880-000", "39884-999"))
def test_is_valid_with_valid(valid_cep):
    assert is_valid(valid_cep)


@pytest.mark.parametrize("invalid_cep", ("123", "123456", "123456789"))
def test_is_valid_with_invalid(invalid_cep):
    assert not is_valid(invalid_cep)
