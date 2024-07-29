from brazilian_ids.functions.location.cep import format, parse, CEP


masp_cep = "01310-200"


def test_format():
    assert format("01310200") == masp_cep


def test_parse():
    result = parse("01310200")
    assert isinstance(result, CEP)


def test_parse_formated():
    result = parse(masp_cep)
    assert isinstance(result, CEP)


def test_cep_instance():
    instance = CEP(
        region="0",
        sub_region="1",
        sector="3",
        sub_sector="1",
        division="0",
        suffix="200",
        formatted_cep=masp_cep,
    )

    attribs = ("region", "sub_region", "sector", "sub_sector", "division", "suffix")

    for attribute in attribs:
        assert hasattr(instance, attribute)

    assert instance.region == "0"
    assert instance.formatted_cep == masp_cep
