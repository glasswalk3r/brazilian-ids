from brazilian_ids.functions.person.pis_pasep import InvalidPISPASEPLengthError


def test_invalid_pis_pasep_length_error_class():
    assert issubclass(InvalidPISPASEPLengthError, ValueError)


def test_invalid_pis_pasep_length_error_instance():
    instance = InvalidPISPASEPLengthError("1234")
    assert (
        str(instance)
        == "The PIS/PASEP '1234' (without the verification digit) length is incorrect: got 4, expect 10 digits"
    )
