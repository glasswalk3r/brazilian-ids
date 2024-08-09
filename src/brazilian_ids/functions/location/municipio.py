"""Functions to handle Brazilian município (county) codes.

Although the municipio code has a verification digit, there are 9 known codes
where those digits are invalid.

This module contains those municipio codes in the ``INVALID`` ``dict``.

See also:
- `'Nota ténica 2008' <http://www.sefaz.al.gov.br/nfe/notas_tecnicas/NT2008.004.pdf>`_
- `IBGE <https://www.ibge.gov.br/explica/codigos-dos-municipios.php>`_
"""

from brazilian_ids.functions.exceptions import InvalidIdLengthError


class InvalidMunicipioFederalUnitError(ValueError):
    def __init__(self, federal_unit):
        self.code = federal_unit
        super().__init__(f"The federal unit code '{federal_unit}' is invalid")


class Municipio:
    """Representation of a município based on it's complete code."""

    @staticmethod
    def federal_units() -> dict[str, str]:
        return {
            "11": "Rondônia",
            "12": "Acre",
            "13": "Amazonas",
            "14": "Roraima",
            "15": "Pará",
            "16": "Amapá",
            "17": "Tocantins",
            "21": "Maranhão",
            "22": "Piauí",
            "23": "Ceará",
            "24": "Rio",
            "25": "Paraíba",
            "26": "Pernambuco",
            "27": "Alagoas",
            "28": "Sergipe",
            "29": "Bahia",
            "31": "Minas",
            "32": "Espírito",
            "33": "Rio",
            "35": "São",
            "41": "Paraná",
            "42": "Santa",
            "43": "Rio",
            "50": "Mato",
            "51": "Mato",
            "52": "Goiás",
            "53": "Distrito",
        }

    def __init__(
        self, unidade_federativa: str, municipio: str, control_digits: str
    ) -> None:
        if len(unidade_federativa) != 2:
            raise ValueError("Federal unit must have two digits")

        if len(municipio) != 3:
            raise ValueError("Municipio must have 3 digits")

        if len(control_digits) != 2:
            raise ValueError("The control digits must be 2")

        try:
            self.__federal_unit = self.federal_units()[unidade_federativa]
        except KeyError as e:
            raise InvalidMunicipioFederalUnitError(str(e))

        self.__fed_unit_code = unidade_federativa
        self.__muni = municipio
        self.__digits = control_digits

    @property
    def federal_unit(self) -> str:
        """Return the name of the Brazilian UF."""
        return self.__federal_unit

    @property
    def federal_unit_code(self) -> str:
        """Return the code of the 'unidade federativa' (UF), corresponding to one of the
        Brazil states or the capital."""
        return self.__fed_unit_code

    @property
    def municipio(self) -> str:
        """Return the município code."""
        return self.__muni

    @property
    def control_digits(self) -> str:
        """Return the 'control digits' created by IBGE."""
        return self.__digits

    def __eq__(self, other: object) -> bool:
        if (
            not hasattr(other, "federal_unit_code")
            or not hasattr(other, "municipio")
            or not hasattr(other, "control_digits")
        ):
            return False

        return (
            self.federal_unit_code == other.federal_unit_code
            and self.municipio == other.municipio
            and self.control_digits == other.control_digits
        )

    def __str__(self):
        return "{0} in {1}".format(
            self.__muni, self.federal_units()[self._fed_unit_code]
        )

    def __repr__(self):
        return 'Municipio(unidade_federativa="{0}", municipio="{1}", control_digits="{2}")'.format(
            self.__fed_unit_code, self.__muni, self.__digits
        )


EXPECTED_DIGITS = 7


def __split_municipio(municipio: str) -> tuple[str, str, str]:
    if len(municipio) < EXPECTED_DIGITS:
        raise InvalidMunicipioLengthError(municipio)

    return (municipio[:2], municipio[2:5], municipio[5:])


def parse(municipio: str) -> Municipio:
    data = __split_municipio(municipio)
    return Municipio(
        unidade_federativa=data[0], municipio=data[1], control_digits=data[2]
    )


class InvalidMunicipioTypeMixin:
    """Mixin class for município errors."""

    def id_type(self):
        return "município"


class InvalidMunicipioLengthError(InvalidMunicipioTypeMixin, InvalidIdLengthError):
    """Exception for invalid município length error."""

    def __init__(
        self,
        municipio: str,
        expected_digits: int = EXPECTED_DIGITS,
    ) -> None:
        super().__init__(id=municipio, expected_digits=expected_digits)


INVALID = {
    "2201919": 9,  # Bom Princípio do Piauí, PI
    "2201988": 8,  # Brejo do Piauí, PI
    "2202251": 1,  # Canavieira, PI
    "2611533": 3,  # Quixaba, PE
    "3117836": 6,  # Cônego Marinho, MG
    "3152131": 1,  # Ponto Chique, MG
    "4305871": 1,  # Coronel Barros, RS
    "5203939": 9,  # Buriti de Goiás, GO
    "5203962": 2,  # Buritinópolis, GO
}


def is_valid(municipio: str) -> bool:
    """Check whether município code is valid.

    It's hard to check if a code is valid completely since the control digits
    are defined internally by IBGE and, to this date, there are 5,570
    municípios in Brazil.

    This function tries to check more basic aspects that are possible without
    copying a large amount of text to the Python code.

    Also, those codes are always changing.
    """
    if len(municipio) != EXPECTED_DIGITS:
        return False

    if municipio[0] == "0":
        return False

    if municipio in INVALID.keys():  # need to check exceptions list
        return True

    try:
        parse(municipio)
    except InvalidMunicipioFederalUnitError:
        return False

    return True
