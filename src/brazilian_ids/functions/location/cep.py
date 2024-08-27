"""Functions to work with CEP ("Código de Endereçamento Postal", in Brazilian
Portuguese), which is the equivalent of zipcodes.

The meaning of numeric codes for region, sub region, etc, are in strict control
of a private company in Brazil called Correios. The company has the monopoly in
Brazil and doesn't provide data besides simply queries with limited results and
restricted by captchas to making data scraping more difficult.

See also:

- `Correios <https://pt.wikipedia.org/wiki/Empresa_Brasileira_de_Correios_e_Tel%C3%A9grafos>`_
- `CEP <https://pt.wikipedia.org/wiki/C%C3%B3digo_de_Endere%C3%A7amento_Postal>`_
"""

from dataclasses import dataclass


@dataclass
class CEP:
    """Representation of a CEP.

    Should be obtained from the ``parse`` function.
    """

    formatted_cep: str
    region: int
    sub_region: int
    sector: int
    sub_sector: int
    division: int
    suffix: str

    def __ge__(self, other):
        test_sequence = ("region", "sub_region", "sub_sector", "division")

        for digit in test_sequence:
            if getattr(self, digit) > getattr(other, digit):
                return True
            elif getattr(self, digit) == getattr(other, digit):
                continue
            else:
                return False

        a = int(self.suffix)
        b = int(other.suffix)

        return a >= b

    def __le__(self, other):
        test_sequence = ("region", "sub_region", "sub_sector", "division")

        for digit in test_sequence:
            if getattr(self, digit) < getattr(other, digit):
                return True
            elif getattr(self, digit) == getattr(other, digit):
                continue
            else:
                return False

        a = int(self.suffix)
        b = int(other.suffix)

        return a <= b


def is_valid(cep: str, raw: bool = True, digits: int = 0) -> bool:
    if raw:
        cep = cep.replace("-", "")

    if digits == 0:
        digits = len(cep)

    expected = set([4, 5, 7, 8])
    return digits in expected


def format(cep: str) -> str:
    """Applies typical 00000-000 formatting to CEP."""
    cep = cep.replace("-", "")
    total_digits = len(cep)

    if not is_valid(cep=cep, raw=False, digits=total_digits):
        # TODO: custom exception
        raise ValueError("Invalid CEP code: {0}".format(cep))

    if total_digits == 4 or total_digits == 5:
        cep = "0" * (5 - total_digits) + cep + "000"
    else:
        cep = "0" * (8 - total_digits) + cep

    return "{0}-{1}".format(cep[:-3], cep[-3:])


def parse(cep: str) -> CEP:
    """Split a CEP into region, sub-region, sector, subsector, division."""
    fmtcep = format(cep)
    geo = [fmtcep[:i] for i in range(1, 6)]
    suffix = fmtcep[-3:]

    return CEP(
        formatted_cep=fmtcep,
        region=int(geo[0]),
        sub_region=int(geo[1]),
        sector=int(geo[2]),
        sub_sector=int(geo[3]),
        division=int(geo[4]),
        suffix=suffix,
    )
