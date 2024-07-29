from brazilian_ids.functions.person.cpf import InvalidCPFError, InvalidCPFLenghtError
from brazilian_ids.functions.exceptions import InvalidIdLenghtError


def test_invalid_cpf_error_class():
    assert issubclass(InvalidCPFError, ValueError)


def test_invalid_cpf_error_instance():
    instance = InvalidCPFError("1234")
    assert hasattr(instance, "id")
    assert instance.id == "1234"


def test_invalid_cpf_error_custom():
    instance = InvalidCPFError("1234")
    assert str(instance).startswith("The CPF")


def test_invalid_cpf_length_error_class():
    assert issubclass(InvalidCPFLenghtError, InvalidIdLenghtError)


def test_invalid_cpf_length_error_instance():
    instance = InvalidCPFLenghtError("1234")
    assert str(instance) == "A CPF must have at least 9 digits, '1234' has only 4"
