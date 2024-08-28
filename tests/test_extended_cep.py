import pytest

from brazilian_ids.functions.location.extended_cep import (
    CepRangeHttpSource,
    CepRangeSource,
)
from brazilian_ids.functions.location.cep import parse


@pytest.fixture(scope="session")
def instance():
    return CepRangeHttpSource()


def test_range_http_source():
    assert issubclass(CepRangeHttpSource, CepRangeSource)


def test_http_source_states(instance):
    result = instance.valid_states()
    assert result.__class__.__name__ == "tuple"
    assert result == (
        "AC",
        "AL",
        "AM",
        "AP",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MG",
        "MS",
        "MT",
        "PA",
        "PB",
        "PE",
        "PI",
        "PR",
        "RJ",
        "RN",
        "RO",
        "RR",
        "RS",
        "SC",
        "SE",
        "SP",
        "TO",
    )


def test_http_source_range_by_state(instance):
    result = instance.ranges_by_state("DF")
    assert result.__class__.__name__ == "list"
    assert result == [
        tuple([parse("70000-001"), parse("72799-999")]),
        tuple([parse("73000-001"), parse("73699-999")]),
    ]


def test_http_source_pagination(instance):
    result = instance.ranges_by_state("MG")
    assert len(result) > 50
