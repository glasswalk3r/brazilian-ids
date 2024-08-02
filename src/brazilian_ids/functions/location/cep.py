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
from brazilian_ids.functions.util import NONDIGIT_REGEX


@dataclass
class CEP:
    """Representation of a CEP.

    Should be obtained from the ``parse`` function.
    """

    formatted_cep: str
    region: str
    sub_region: str
    sector: str
    sub_sector: str
    division: str
    suffix: str


def format(cep: str) -> str:
    """Applies typical 00000-000 formatting to CEP."""
    cep = NONDIGIT_REGEX.sub("", cep)
    dig = len(cep)

    if dig == 4 or dig == 5:
        cep = "0" * (5 - dig) + cep + "000"
    elif dig == 7 or dig == 8:
        cep = "0" * (8 - dig) + cep
    else:
        raise ValueError("Invalid CEP code: {0}".format(cep))

    return "{0}-{1}".format(cep[:-3], cep[-3:])


def parse(cep: str) -> CEP:
    """Split a CEP into region, sub-region, sector, subsector, division."""
    fmtcep = format(cep)
    cep = fmtcep
    geo = [fmtcep[:i] for i in range(1, 6)]
    suffix = fmtcep[-3:]

    return CEP(
        formatted_cep=cep,
        region=geo[0],
        sub_region=geo[1],
        sector=geo[2],
        sub_sector=geo[3],
        division=geo[4],
        suffix=suffix,
    )
