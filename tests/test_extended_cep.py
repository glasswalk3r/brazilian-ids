import dataclasses

import pytest

from brazilian_ids.functions.location.extended_cep import (
    CepDetails,
    CepNotFoundError,
    ExternalSourceCepValidation,
    ViaCepClient,
    ViaCepHttpClient,
    ViaCepResponse,
)


class FakeViaCepClient(ViaCepClient):
    """A ``ViaCepClient`` that never hits the network, tracking how many times it was called."""

    def __init__(self):
        self.calls = 0

    def fetch(self, cep: str) -> ViaCepResponse:
        self.calls += 1

        if cep == "99999999":
            raise CepNotFoundError(cep)

        return ViaCepResponse(estado="São Paulo", bairro="Sé")


@pytest.fixture
def fake_client():
    return FakeViaCepClient()


@pytest.fixture
def validator(fake_client):
    return ExternalSourceCepValidation(source=fake_client, cache_size=2)


def test_via_cep_client_is_abstract():
    with pytest.raises(TypeError):
        ViaCepClient()


def test_via_cep_http_client_is_a_via_cep_client():
    assert issubclass(ViaCepHttpClient, ViaCepClient)


def test_via_cep_response_parses_a_real_shaped_payload():
    payload = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
        "estado": "São Paulo",
        "regiao": "Sudeste",
    }

    result = ViaCepResponse.model_validate(payload)

    assert result.estado == "São Paulo"
    assert result.bairro == "Sé"


def test_via_cep_response_parses_erro_field():
    result = ViaCepResponse.model_validate({"erro": True})
    assert result.erro is True


def test_cep_details_is_read_only():
    instance = CepDetails(state="SP", location="Sé")

    with pytest.raises(dataclasses.FrozenInstanceError):
        instance.state = "RJ"


def test_cep_details_uses_slots():
    instance = CepDetails(state="SP", location="Sé")
    assert not hasattr(instance, "__dict__")


def test_external_source_cep_validation_by_state(validator):
    assert validator.by_state("01001000", "São Paulo") is True


def test_external_source_cep_validation_by_location(validator):
    assert validator.by_location("01001000", "São Paulo", "Sé") is True


def test_external_source_cep_validation_caches_lookups(validator, fake_client):
    validator.by_state("01001000", "São Paulo")
    validator.by_location("01001000", "São Paulo", "Sé")

    assert fake_client.calls == 1


def test_external_source_cep_validation_not_found_returns_false(validator):
    assert validator.by_state("99999999", "São Paulo") is False


def test_external_source_cep_validation_malformed_cep_returns_false_without_calling_source(validator, fake_client):
    assert validator.by_state("123", "São Paulo") is False
    assert fake_client.calls == 0
