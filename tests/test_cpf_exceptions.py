from brazilian_ids.functions.person.cpf import InvalidCpfError, InvalidCpfLengthError
from brazilian_ids.functions.exceptions import InvalidIdLengthError, InvalidIdError


def test_invalid_cpf_error_class():
    assert issubclass(InvalidCpfError, InvalidIdError)


def test_invalid_cpf_error_instance():
    instance = InvalidCpfError("1234")
    assert hasattr(instance, "id")
    assert instance.id == "1234"


def test_invalid_cpf_error_custom():
    instance = InvalidCpfError("1234")
    assert str(instance).startswith("The CPF")


def test_invalid_cpf_length_error_class():
    assert issubclass(InvalidCpfLengthError, InvalidIdLengthError)


def test_invalid_cpf_length_error_instance():
    instance = InvalidCpfLengthError("1234")
    assert str(instance) == "A CPF must have at least 9 digits, '1234' has only 4"
