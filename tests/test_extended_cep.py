import pytest

from brazilian_ids.functions.location.extended_cep import (
    CepRangeHttpSource,
    CepRangeSource,
    CepValidationByRange,
)
from brazilian_ids.functions.location.cep import parse


@pytest.fixture(scope="session")
def scraper():
    return CepRangeHttpSource()


@pytest.fixture()
def default_state():
    return "MG"


def test_range_http_source():
    assert issubclass(CepRangeHttpSource, CepRangeSource)


def test_http_source_states(scraper):
    result = scraper.valid_states()
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


def test_http_source_range_by_state(scraper):
    result = scraper.ranges_by_state("DF")
    assert result.__class__.__name__ == "list"
    assert result == [
        tuple([parse("70000-001"), parse("72799-999")]),
        tuple([parse("73000-001"), parse("73699-999")]),
    ]


def test_http_source_pagination(scraper, default_state):
    result = scraper.ranges_by_state(default_state)
    assert len(result) > 50


@pytest.mark.parametrize("cep", ("38180001", "38188999", "38188998", "38187000"))
def test_cep_validation_is_valid_by_location(scraper, default_state, cep):
    instance = CepValidationByRange(scraper)
    assert instance.is_valid_by_location(cep=cep, state=default_state, location="Araxá")
