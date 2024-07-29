from brazilian_ids.functions.person.pis_pasep import InvalidPISPASEPLengthError


def test_invalid_pis_pasep_length_error_class():
    assert issubclass(InvalidPISPASEPLengthError, ValueError)


def test_invalid_pis_pasep_length_error_instance():
    instance = InvalidPISPASEPLengthError("1234")
    assert (
        str(instance) == "A PIS/PASEP must have at least 10 digits, '1234' has only 4"
    )
