"""Functions and classes to validate CEPs against the ViaCEP external service.

Unlike ``brazilian_ids.functions.location.cep``, which only relies on statically known per-state numeric ranges,
this module queries `ViaCEP <https://viacep.com.br/>`_ over HTTP to validate a CEP against its actual registered
state ("estado") and neighborhood ("bairro").

This module has third-party dependencies (``httpx`` and ``pydantic``) that are not part of the package's regular
runtime dependencies.
"""

from __future__ import annotations

import weakref
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache

import httpx
from pydantic import BaseModel

from brazilian_ids.functions.location.cep import format as format_cep
from brazilian_ids.functions.location.cep import is_valid
from brazilian_ids.functions.util import NONDIGIT_REGEX

DEFAULT_CACHE_SIZE = 300


class ViaCepResponse(BaseModel):
    """Representation of the JSON response returned by the ViaCEP API.

    See also `ViaCEP <https://viacep.com.br/>`_.
    """

    cep: str = ""
    logradouro: str = ""
    complemento: str = ""
    unidade: str = ""
    bairro: str = ""
    localidade: str = ""
    uf: str = ""
    estado: str = ""
    regiao: str = ""
    ibge: str = ""
    gia: str = ""
    ddd: str = ""
    siafi: str = ""
    erro: bool = False


class CepNotFoundError(ValueError):
    """Raised when the external source has no record for the given CEP."""

    def __init__(self, cep: str) -> None:
        super().__init__(f"The CEP '{cep}' was not found")
        self.cep = cep


class ViaCepClient(ABC):
    """Abstract interface for a client able to fetch CEP details from a ViaCEP-compatible source."""

    @abstractmethod
    def fetch(self, cep: str) -> ViaCepResponse:
        """Fetch the details for the given CEP.

        Implementations must raise ``CepNotFoundError`` if the source has no record for ``cep``.
        """
        raise NotImplementedError


class ViaCepHttpClient(ViaCepClient):
    """Fetches CEP details from the public ViaCEP REST API over HTTP, using ``httpx``.

    For example, a request for the CEP ``01001000`` is made against
    ``https://viacep.com.br/ws/01001000/json/``.
    """

    __base_url = "https://viacep.com.br/ws"

    def __init__(self, client: httpx.Client | None = None) -> None:
        if client is None:
            self.__client = httpx.Client()
            weakref.finalize(self, self.__client.close)
        else:
            self.__client = client

    def fetch(self, cep: str) -> ViaCepResponse:
        digits = NONDIGIT_REGEX.sub("", format_cep(cep))
        url = f"{self.__base_url}/{digits}/json/"

        response = self.__client.get(url)
        response.raise_for_status()

        parsed = ViaCepResponse.model_validate(response.json())

        if parsed.erro:
            raise CepNotFoundError(cep)

        return parsed


@dataclass(frozen=True, slots=True)
class CepDetails:
    """Minimal, read-only representation of the CEP fields actually used by ``ExternalSourceCepValidation``."""

    state: str
    location: str


class ExternalSourceCepValidation:
    """Validates CEPs against an external source, caching lookups in memory using a LRU strategy.

    ``state`` and ``location``, as used by this class's methods, correspond respectively to the ``estado`` and
    ``bairro`` attributes of ``ViaCepResponse``.
    """

    def __init__(self, source: ViaCepClient, cache_size: int = DEFAULT_CACHE_SIZE) -> None:
        self.__source = source
        self.__fetch: Callable[[str], CepDetails] = lru_cache(maxsize=cache_size)(self.__fetch_details)

    def __fetch_details(self, cep: str) -> CepDetails:
        response = self.__source.fetch(cep)
        return CepDetails(state=response.estado, location=response.bairro)

    def by_state(self, cep: str, state: str) -> bool:
        if not is_valid(cep):
            return False

        try:
            details = self.__fetch(cep)
        except CepNotFoundError:
            return False

        return details.state == state

    def by_location(self, cep: str, state: str, location: str) -> bool:
        if not is_valid(cep):
            return False

        try:
            details = self.__fetch(cep)
        except CepNotFoundError:
            return False

        return details.state == state and details.location == location
