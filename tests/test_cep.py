import pytest
import inspect

from brazilian_ids.functions.location.cep import format, parse, CEP, is_valid, is_valid_extended, CepRange, CepInvalidStateError


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


@pytest.mark.parametrize("valid_cep", ("39880000", "39884999"))
def test_is_valid_with_valid_and_raw(valid_cep):
    assert is_valid(cep=valid_cep, raw=True)


@pytest.mark.parametrize("invalid_cep", ("123", "123456", "123456789"))
def test_is_valid_with_invalid(invalid_cep):
    assert not is_valid(cep=invalid_cep, raw=False)


@pytest.mark.parametrize("invalid_cep", ("123", "123456", "123456789"))
def test_is_valid_extended_with_simple_invalid(invalid_cep):
    assert not is_valid(cep=invalid_cep, raw=False)


def test_cep_range_class():
    assert inspect.isclass(CepRange)


def test_cep_range_instance():
    instance = CepRange()
    expected = ("ranges_by_state", "all_ranges")

    for method_name in expected:
        assert inspect.ismethod(getattr(instance, method_name))


def test_cep_range_singleton():
    i1 = CepRange()
    i2 = CepRange()
    assert i1 == i2


def test_cep_range_all_ranges():
    instance = CepRange()
    result = instance.all_ranges()
    assert result.__class__.__name__ == "generator"
    pair = next(result)
    assert pair.__class__.__name__ == "tuple"

    for i in pair:
        assert pair[i].__class__.__name__ == "CEP"


@pytest.mark.parametrize("invalid_cep", ("72000-000", "73000-000"))
def test_is_valid_extended_with_complex_invalid(invalid_cep):
    assert not is_valid_extended(cep=invalid_cep, raw=False)


def test_is_valid_extended_with_invalid_state():
    invalid_state = "XY"
    with pytest.raises(CepInvalidStateError) as e:
        is_valid_extended(cep="72000-000", state=invalid_state)

    assert invalid_state in str(e.value)


def test_is_valid_extended_with_valid_state():
    assert is_valid_extended(cep="88100-000", state="SC")
