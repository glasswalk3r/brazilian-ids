"""Functions to handle Numeração Única de Processo Judicial identifier.

This number is a standard created by the "Conselho Nacional de Justiça" (CNJ).

The name of this module is an acronym for the "Numeração Única de Processo
Judicial", and the name of parameters in the functions of this module as well.

References:

- `CNJ <https://www.cnj.jus.br/programas-e-acoes/numeracao-unica>`_
- `Resolução nº 65, de 16 de dezembro de 2008 <https://atos.cnj.jus.br/atos/detalhar/atos-normativos?documento=119>`_
- `Resolução nº 12 do Conselho Nacional de Justiça, de 14 de fevereiro de 2006 <https://atos.cnj.jus.br/atos/detalhar/atos-normativos?documento=206>`_
- `Lista de Código do tribunal <https://www.tjsp.jus.br/cac/scp/Arquivos/Documentos/TJSP_DEPRE_Layout_de_Importa%C3%A7%C3%A3o_v2.1.pdf>`_
"""

from dataclasses import dataclass
from collections import deque

from brazilian_ids.functions.util import NONDIGIT_REGEX
from brazilian_ids.functions.exceptions import InvalidIdError


class InvalidCourtIdError(ValueError):
    def __init__(self, court_id: int) -> None:
        self.court_id = court_id
        msg = "The court_id {0} is invalid: it must be between 1 and {1}".format(
            court_id, Courts.total_courts()
        )
        super().__init__(self, msg)


class InvalidNupjTypeMixin:
    """Mixin class for NUPJ errors."""

    def id_type(self):
        return "Numeração Única de Processo Judicial"


class InvalidNupjError(InvalidNupjTypeMixin, InvalidIdError):
    """Exception for invalid NUPJ errors"""

    def __init__(self, nupj: str) -> None:
        super().__init__(id=nupj)


class Court:
    def __init__(self, id: int, acronym: str) -> None:
        if id == 0:
            raise InvalidCourtIdError(id)

        try:
            description = self.__courts[id]
        except IndexError:
            raise InvalidCourtIdError(id)

        self.__id = id
        self.__acronym = acronym
        self.__description = description

    @property
    def id(self):
        return self.__id

    @property
    def acronym(self):
        return self.__acronym

    @property
    def description(self):
        return self.__description

    def __str__(self):
        return f"{self.__acronym}: {self.__description}"


SEGMENTS = (
    None,
    "Supremo Tribunal Federal",
    "Conselho Nacional de Justiça",
    "Superior Tribunal de Justiça",
    "Justiça Federal",
    "Justiça do Trabalho",
    "Justiça Eleitoral",
    "Justiça Militar da União",
    "Justiça dos Estados e do Distrito Federal e Territórios",
    "Justiça Militar Estadual",
)


class Courts:
    # segments IDs are the keys, see SEGMENTS
    __courts = {
        4: (
            None,
            "TRIBUNAL REGIONAL FEDERAL DA 1ª REGIÃO",
            "TRIBUNAL REGIONAL FEDERAL DA 2ª REGIÃO",
            "TRIBUNAL REGIONAL FEDERAL DA 3ª REGIÃO",
            "TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO",
            "TRIBUNAL REGIONAL FEDERAL DA 5ª REGIÃO",
            "TRIBUNAL REGIONAL FEDERAL DA 6ª REGIÃO",
        ),
        5: (
            None,
            "TRIBUNAL REGIONAL DO TRABALHO DA 1ª REGIÃO - RIO DE JANEIRO",
            "TRIBUNAL REGIONAL DO TRABALHO DA 2ª REGIÃO - SÃO PAULO",
            "TRIBUNAL REGIONAL DO TRABALHO DA 3ª REGIÃO - BELO HORIZONTE",
            "TRIBUNAL REGIONAL DO TRABALHO DA 4ª REGIÃO - PORTO ALEGRE",
            "TRIBUNAL REGIONAL DO TRABALHO DA 5ª REGIÃO - SALVADOR",
            "TRIBUNAL REGIONAL DO TRABALHO DA 6ª REGIÃO - RECIFE",
            "TRIBUNAL REGIONAL DO TRABALHO DA 7ª REGIÃO - FORTALEZA",
            "TRIBUNAL REGIONAL DO TRABALHO DA 8ª REGIÃO - BELÉM",
            "TRIBUNAL REGIONAL DO TRABALHO DA 9ª REGIÃO - CURITIBA",
            "TRIBUNAL REGIONAL DO TRABALHO DA 10ª REGIÃO - BRASÍLIA",
            "TRIBUNAL REGIONAL DO TRABALHO DA 11ª REGIÃO - MANAUS",
            "TRIBUNAL REGIONAL DO TRABALHO DA 12ª REGIÃO - FLORIANÓPOLIS",
            "TRIBUNAL REGIONAL DO TRABALHO DA 13ª REGIÃO - JOÃO PESSOA",
            "TRIBUNAL REGIONAL DO TRABALHO DA 14ª REGIÃO - PORTO VELHO",
            "TRIBUNAL REGIONAL DO TRABALHO DA 15ª REGIÃO - CAMPINAS",
            "TRIBUNAL REGIONAL DO TRABALHO DA 16ª REGIÃO - SÃO LUIZ",
            "TRIBUNAL REGIONAL DO TRABALHO DA 17ª REGIÃO - VITÓRIA",
            "TRIBUNAL REGIONAL DO TRABALHO DA 18ª REGIÃO - GOIÂNIA",
            "TRIBUNAL REGIONAL DO TRABALHO DA 19ª REGIÃO - MACEIÓ",
            "TRIBUNAL REGIONAL DO TRABALHO DA 20ª REGIÃO - ARACAJU",
            "TRIBUNAL REGIONAL DO TRABALHO DA 21ª REGIÃO - NATAL",
            "TRIBUNAL REGIONAL DO TRABALHO DA 22ª REGIÃO - TERESINA",
            "TRIBUNAL REGIONAL DO TRABALHO DA 23ª REGIÃO - CUIABÁ",
            "TRIBUNAL REGIONAL DO TRABALHO DA 24ª REGIÃO - CAMPO GRANDE",
        ),
        6: (
            None,
            "TRIBUNAL REGIONAL ELEITORAL do Acre",
            "TRIBUNAL REGIONAL ELEITORAL de Alagoas",
            "TRIBUNAL REGIONAL ELEITORAL da Amazonas",
            "TRIBUNAL REGIONAL ELEITORAL da Bahia",
            "TRIBUNAL REGIONAL ELEITORAL do Ceará",
            "TRIBUNAL REGIONAL ELEITORAL do Distrito Federal",
            "TRIBUNAL REGIONAL ELEITORAL do Espírito Santo",
            "TRIBUNAL REGIONAL ELEITORAL de Goiás",
            "TRIBUNAL REGIONAL ELEITORAL do Maranhão",
            "TRIBUNAL REGIONAL ELEITORAL do Mato Grosso",
            "TRIBUNAL REGIONAL ELEITORAL do Mato Grosso do Sul",
            "TRIBUNAL REGIONAL ELEITORAL de Minas Gerais",
            "TRIBUNAL REGIONAL ELEITORAL do Pará",
            "TRIBUNAL REGIONAL ELEITORAL da Paraíba",
            "TRIBUNAL REGIONAL ELEITORAL do Paraná",
            "TRIBUNAL REGIONAL ELEITORAL de Pernambuco",
            "TRIBUNAL REGIONAL ELEITORAL do Piauí",
            "TRIBUNAL REGIONAL ELEITORAL do Rio de Janeiro",
            "TRIBUNAL REGIONAL ELEITORAL do Rio Grande do Norte",
            "TRIBUNAL REGIONAL ELEITORAL do Rio Grande do Sul",
            "TRIBUNAL REGIONAL ELEITORAL de Rondônia",
            "TRIBUNAL REGIONAL ELEITORAL de Roraima",
            "TRIBUNAL REGIONAL ELEITORAL de Santa Catarina",
            "TRIBUNAL REGIONAL ELEITORAL de São Paulo",
            "TRIBUNAL REGIONAL ELEITORAL de Sergipe",
            "TRIBUNAL REGIONAL ELEITORAL do Tocantins",
            "TRIBUNAL REGIONAL ELEITORAL do Maranhão",
        ),
        7: (
            None,
            "Circunscrição Judiciária Militar do Estado de São Paulo (1ª Região)",
            "Circunscrição Judiciária Militar do Estado do Rio de Janeiro (2ª Região)",
            "Circunscrição Judiciária Militar do Estado de Minas Gerais (3ª Região)",
            "Circunscrição Judiciária Militar do Estado do Rio Grande do Sul (4ª Região)",
            "Circunscrição Judiciária Militar do Estado de Pernambuco (5ª Região)",
            "Circunscrição Judiciária Militar do Estado do Pará (6ª Região)",
            "Circunscrição Judiciária Militar do Estado da Bahia (7ª Região)",
            "Circunscrição Judiciária Militar do Estado do Espírito Santo (8ª Região)",
            "Circunscrição Judiciária Militar do Estado do Ceará (9ª Região)",
            "Circunscrição Judiciária Militar do Estado do Maranhão (10ª Região)",
            "Circunscrição Judiciária Militar do Estado do Mato Grosso (11ª Região)",
            "Circunscrição Judiciária Militar do Estado de Goiás (12ª Região)",
        ),
        8: (
            None,
            "Tribunal de Justiça do Acre",
            "Tribunal de Justiça de Alagoas",
            "Tribunal de Justiça do Amazonas",
            "Tribunal de Justiça da Bahia",
            "Tribunal de Justiça do Ceará",
            "Tribunal de Justiça do Distrito Federal e Territórios",
            "Tribunal de Justiça do Espírito Santo",
            "Tribunal de Justiça de Goiás",
            "Tribunal de Justiça do Maranhão",
            "Tribunal de Justiça do Mato Grosso",
            "Tribunal de Justiça do Mato Grosso do Sul",
            "Tribunal de Justiça de Minas Gerais",
            "Tribunal de Justiça do Pará",
            "Tribunal de Justiça da Paraíba",
            "Tribunal de Justiça do Paraná" "Tribunal de Justiça de Pernambuco",
            "Tribunal de Justiça do Piauí" "Tribunal de Justiça do Rio de Janeiro",
            "Tribunal de Justiça do Rio Grande do Norte",
            "Tribunal de Justiça do Rio Grande do Sul",
            "Tribunal de Justiça de Rondônia",
            "Tribunal de Justiça de Roraima",
            "Tribunal de Justiça de Santa Catarina",
            "Tribunal de Justiça de São Paulo",
            "Tribunal de Justiça de Sergipe",
            "Tribunal de Justiça do Tocantins",
            "Tribunal de Justiça do Maranhão",
        ),
        9: {
            13: "Tribunal Militar de Minas Gerais",
            21: "Tribunal Militar do Rio Grande do Sul",
            26: "Tribunal Militar de São Paulo",
        },
    }

    @classmethod
    def court_acronym(klass, segment: int, court_id: int) -> str:
        if court_id == 0:
            raise InvalidCourtIdError(court_id)

        try:
            acronym = klass.__courts[court_id]
        except IndexError:
            raise InvalidCourtIdError(court_id)

        return acronym

    @classmethod
    def court(klass, court_id: int) -> Court:
        return Court(id=court_id, acronym=klass.court_acronym(court_id))

    @classmethod
    def total_courts(klass) -> int:
        return len(klass.__courts)


@dataclass
class NUPJ:
    """Class representing the fields of a NUPJ as instance attributes.

    Usually you will use the function ``parse`` from this package to get a
    instance.
    """

    lawsuit_id: str
    first_digit: int
    second_digit: int
    year: int
    segment: int
    court_id: str
    lawsuit_city: str

    def __str__(self) -> str:
        return "{}".format(self.lawsuit_id)

    def digits(self) -> str:
        return f"{self.first_digit}{self.second_digit}"


EXPECTED_DIGITS = 20

# saving some memory
__zero_tr = (set(("00",)),)
__1_to_27_tr = set(["%02d" % i for i in range(1, 28)])

COURTS_TRS: dict[int, set[str]] = {
    1: __zero_tr,
    2: __zero_tr,
    3: __zero_tr,
    4: set(("01", "02", "03", "04", "05", "06")),
    5: set(["%02d" % i for i in range(1, 25)]),
    6: __1_to_27_tr,
    7: set(["%02d" % i for i in range(1, 13)]),
    8: __1_to_27_tr,
    9: set(("13", "21", "26")),
}


def pad(nupj: str) -> str:
    """Pad a NUPJ with zeros, if it's length is less than ``EXPECTED_DIGITS``."""
    if len(nupj) == 0 or nupj == "":
        raise InvalidNupjError(nupj)

    nupj = NONDIGIT_REGEX.sub("", nupj)

    if len(nupj) < EXPECTED_DIGITS:
        tmp = deque(nupj)
        padded = ["0" for i in range(EXPECTED_DIGITS)]
        start = EXPECTED_DIGITS - 1

        for i in range(start, 0, -1):
            if len(tmp) > 0:
                padded[i] = tmp.pop()

        return "".join(padded)

    return nupj


def parse(nupj: str) -> NUPJ:
    """Parse a NUPJ."""
    nupj = NONDIGIT_REGEX.sub("", nupj)
    nupj = pad(nupj)
    # NNNNNNN-DD.AAAA.J.TR.OOOO
    lawsuit = nupj[:7]
    first = int(nupj[7])
    second = int(nupj[8])
    year = int(nupj[9:13])
    segment = int(nupj[13])
    court = nupj[14:16]
    l_city = nupj[16:20]

    return NUPJ(
        lawsuit_id=lawsuit,
        first_digit=first,
        second_digit=second,
        year=year,
        segment=segment,
        court_id=court,
        lawsuit_city=l_city,
    )


def is_valid(nupj: str) -> bool:
    """Determine is a given NUPJ is valid or not.

    It is a known issue that the justice segments
    "Tribunal Superior do Trabalho", "Tribunal Superior Eleitoral" and
    "Superior Tribunal Militar" don't have a documented ID!

    That means there is no way to associate the proper court ID with the
    justice segment in the NUPJ, and in those cases where every check fails but
    the court ID is "90", this function will continue checking other aspects
    instead of returning ``False``.
    """
    parsed = parse(nupj)

    # the year of the creation of the law
    if parsed.year < 2008:
        return False

    try:
        result = SEGMENTS[parsed.segment]
    except IndexError:
        return False
    else:
        if result is None:
            return False

    # "Conselho da Justiça Federal" and "Conselho Superior da Justiça do Trabalho" uses "90"
    if parsed.court_id != "90" and parsed.court_id not in COURTS_TRS[parsed.segment]:
        if parsed.court_id != "00":
            return False

    divisor = 97
    partial_1 = str(int(parsed.lawsuit_id) % divisor)
    partial_2 = str(
        int(
            "{0}{1}{2}{3}".format(
                partial_1, parsed.year, parsed.segment, parsed.court_id
            )
        )
        % divisor
    )
    result = (
        int("{0}{1}{2}".format(partial_2, parsed.lawsuit_city, parsed.digits()))
        % divisor
    )

    return result == 1
