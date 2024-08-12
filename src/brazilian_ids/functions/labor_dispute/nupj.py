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
        msg = f"The court_id '{court_id}' is invalid"
        super().__init__(self, msg)


class InvalidSegmentIdError(ValueError):
    def __init__(self, segment_id: int) -> None:
        self.court_id = segment_id
        msg = f"The segment_id '{segment_id}' is invalid"
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
    def __init__(self, id: str, acronym: str, description: str) -> None:
        if id == 0:
            raise InvalidCourtIdError(court_id=id)

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
        return f"Court {self.__acronym}, {self.__description}"

    def __repr__(self):
        return f'Court(id={self.__id}, acronym="{self.__acronym}", description="{self.description}")'


class Courts:
    """Class factory to build court instances based on rules.

    Although all digits from a NUPJ are strings, for segment an integer is
    expected instead, since this data type is shorter in bytes and well suited
    for the context.
    """

    __segments = (
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

    __courts_descriptions_prefix = {
        4: "Tribunal Regional Federal da",
        5: "Tribunal Regional do Trabalho da",
        6: "Tribunal Regional Eleitoral",
        7: "Circunscrição Judiciária Militar da",
        8: "Tribunal de Justiça",
        9: "Tribunal de Justiça Militar",
    }

    __unknown_court = {"00": ("N/D", "Não Disponível")}

    __segments_courts = {
        1: __unknown_court,
        2: __unknown_court,
        3: __unknown_court,
        4: {
            "01": ("TRF01", "1ª Região"),
            "02": ("TRF02", "2ª Região"),
            "03": ("TRF03", "3ª Região"),
            "04": ("TRF04", "4ª Região"),
            "05": ("TRF05", "5ª Região"),
            "06": ("TRF06", "6ª Região"),
        },
        5: {
            "01": ("TRT06", "1ª Região - Rio de Janeiro"),
            "02": ("TRT02", "2ª Região - São Paulo"),
            "03": ("TRT03", "3ª Região - Belo Horizonte"),
            "04": ("TRT04", "4ª Região - Porto Alegre"),
            "05": ("TRT05", "5ª Região - Salvador"),
            "06": ("TRT06", "6ª Região - Recife"),
            "07": ("TRT07", "7ª Região - Fortaleza"),
            "08": ("TRT08", "8ª Região - Belém"),
            "09": ("TRT09", "9ª Região - Curitiba"),
            "10": ("TRT10", "10ª Região - Brasília"),
            "11": ("TRT11", "11ª Região - Manaus"),
            "12": ("TRT12", "12ª Região - Florianópolis"),
            "13": ("TRT13", "13ª Região - João Pessoa"),
            "14": ("TRT14", "14ª Região - Porto Velho"),
            "15": ("TRT15", "15ª Região - Campinas"),
            "16": ("TRT16", "16ª Região - São Luiz"),
            "17": ("TRT17", "17ª Região - Vitória"),
            "18": ("TRT18", "18ª Região - Goiânia"),
            "19": ("TRT19", "19ª Região - Maceió"),
            "20": ("TRT20", "20ª Região - Aracaju"),
            "21": ("TRT21", "21ª Região - Natal"),
            "22": ("TRT22", "22ª Região - Teresina"),
            "23": ("TRT23", "23ª Região - Cuiabá"),
            "24": ("TRT24", "24ª Região - Campo Grande"),
        },
        6: {
            "01": ("TRE-AC", "do Acre"),
            "02": ("TRE-AL", "de Alagoas"),
            "03": ("TRE-AM", "da Amazonas"),
            "04": ("TRE-BA", "da Bahia"),
            "05": ("TRE-CE", "do Ceará"),
            "06": ("TRE-DF", "do Distrito Federal"),
            "07": ("TRE-ES", "do Espírito Santo"),
            "08": ("TRE-GO", "de Goiás"),
            "09": ("TRE-MA", "do Maranhão"),
            "10": ("TRE-MT", "do Mato Grosso"),
            "11": ("TRE-MS", "do Mato Grosso do Sul"),
            "12": ("TRE-MG", "de Minas Gerais"),
            "13": ("TRE-PA", "do Pará"),
            "14": ("TRE-PB", "da Paraíba"),
            "15": ("TRE-PR", "do Paraná"),
            "16": ("TRE-PE", "de Pernambuco"),
            "17": ("TRE-PI", "do Piauí"),
            "18": ("TRE-RJ", "do Rio de Janeiro"),
            "19": ("TRE-RN", "do Rio Grande do Norte"),
            "20": ("TRE-RS", "do Rio Grande do Sul"),
            "21": ("TRE-RO", "de Rondônia"),
            "22": ("TRE-RR", "de Roraima"),
            "23": ("TRE-SC", "de Santa Catarina"),
            "24": ("TRE-SP", "de São Paulo"),
            "25": ("TRE-SE", "de Sergipe"),
            "26": ("TRE-TO", "do Tocantins"),
        },
        7: {
            "01": ("CJM-1", "1ª Região (Brasília)"),
            "02": (
                "CJM-2",
                "2ª Região (São Paulo)",
            ),
            "03": (
                "CJM-3",
                "3ª Região (Minas Gerais)",
            ),
            "04": (
                "CJM-4",
                "4ª Região (Rio de Janeiro)",
            ),
            "05": ("CJM-5", "5ª Região (Belém)"),
            "06": ("CJM-6", "6ª Região (Recife)"),
            "07": ("CJM-7", "7ª Região (Salvador)"),
            "08": (
                "CJM-8",
                "8ª Região (Porto Alegre)",
            ),
            "09": ("CJM-9", "9ª Região (Manaus)"),
            "10": (
                "CJM-10",
                "10ª Região (Fortaleza)",
            ),
            "11": (
                "CJM-11",
                "11ª Região (Campo Grande)",
            ),
            "12": (
                "CJM-12",
                "12ª Região (Curitiba)",
            ),
        },
        8: {
            "01": ("TJAC", "do Acre"),
            "02": ("TJAL", "de Alagoas"),
            "03": ("TJAP", "do Amapá"),
            "04": ("TJAM", "do Amazonas"),
            "05": ("TJBA", "da Bahia"),
            "06": ("TJCE", "do Ceará"),
            "07": ("TJDF", "do Distrito Federal e Territórios"),
            "08": ("TJES", "do Espírito Santo"),
            "09": ("TJGO", "de Goiás"),
            "10": ("TJMA", "do Maranhão"),
            "11": ("TJMT", "do Mato Grosso"),
            "12": ("TJMS", "do Mato Grosso do Sul"),
            "13": ("TJMG", "de Minas Gerais"),
            "14": ("TJPA", "do Pará"),
            "15": ("TJPB", "da Paraíba"),
            "16": ("TJPR", "do Paraná"),
            "17": ("TJPE", "de Pernambuco"),
            "18": ("TJPI", "do Piauí"),
            "19": ("TJRJ", "do Rio de Janeiro"),
            "20": ("TJRN", "do Rio Grande do Norte"),
            "21": ("TJRS", "do Rio Grande do Sul"),
            "22": ("TJRO", "de Rondônia"),
            "23": ("TJRR", "de Roraima"),
            "24": ("TJSC", "de Santa Catarina"),
            "25": ("TJSP", "de São Paulo"),
            "26": ("TJSE", "de Sergipe"),
            "27": ("TJTO", "do Tocantins"),
        },
        9: {
            "13": ("TJMMG", "de Minas Gerais"),
            "21": ("TJMSP", "do Rio Grande do Sul"),
            "26": ("TJMRS", "de São Paulo"),
        },
    }

    @classmethod
    def __court(klass, segment_id: int, court_id: str) -> str:
        if klass.__segments[segment_id] is None:
            raise InvalidSegmentIdError(segment_id)

        try:
            courts = klass.__segments_courts[segment_id]
        except IndexError as e:
            raise InvalidSegmentIdError(e)

        try:
            court = courts[court_id]
        except KeyError as e:
            raise InvalidCourtIdError(e)

        if court is None:
            raise InvalidCourtIdError(court_id)

        return court

    @classmethod
    def court_acronym(klass, segment_id: int, court_id: str) -> str:
        """Return a court acronym, based on segment and court ID."""
        court = klass.__court(segment_id=segment_id, court_id=court_id)
        return court[0]

    @classmethod
    def court(klass, segment_id: int, court_id: str) -> Court:
        court = klass.__court(segment_id=segment_id, court_id=court_id)
        return Court(
            id=court_id,
            acronym=court[0],
            description="{0} {1}".format(
                klass.__courts_descriptions_prefix[segment_id], court[1]
            ),
        )

    @classmethod
    def total_courts(klass) -> int:
        return len(klass.__segments_courts)

    @classmethod
    def segment(klass, id: int) -> str:
        try:
            description = klass.__segments[id]
        except IndexError as e:
            raise InvalidSegmentIdError(e)
        except KeyError as e:
            raise InvalidSegmentIdError(e)

        if description is None:
            raise InvalidSegmentIdError(id)

        return description


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
        result = Courts.segment(parsed.segment)
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
