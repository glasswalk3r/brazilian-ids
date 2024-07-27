from brazilian_ids.functions.person.cpf import InvalidCPFError, InvalidCPFLenghtError


def test_invalid_cpf_error_class():
    assert issubclass(InvalidCPFError, ValueError)


def test_invalid_cpf_error_instance():
    instance = InvalidCPFError("1234")
    assert hasattr(instance, "cpf")
    assert instance.cpf == "1234"


def test_invalid_cpf_error_custom():
    instance = InvalidCPFError("1234", "foobar")
    assert str(instance).startswith("foobar")


def test_invalid_cpf_length_error_class():
    assert issubclass(InvalidCPFLenghtError, InvalidCPFError)


def test_invalid_cpf_length_error_instance():
    instance = InvalidCPFLenghtError("1234")
    assert str(instance) == "A CPF must have at least 9 digits, '1234' has only 4"
