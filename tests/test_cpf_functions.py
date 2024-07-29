import os
import pytest
from collections import deque, namedtuple

from brazilian_ids.functions.person.cpf import (
    is_valid,
    InvalidCPFError,
    format,
    verification_digits,
    random,
)


csv = os.path.join("tests", "fixtures", "cpf.csv")
CPFRecord = namedtuple("CPFRecord", "raw_cpf formated_cpf")


@pytest.fixture(scope="module")
def read_csv() -> tuple[CPFRecord, ...]:
    data: deque[CPFRecord] = deque()

    with open(csv, "r") as fp:
        for line in fp:
            cpf = CPFRecord._make(line.rstrip().split(","))
            data.append(cpf)

    return tuple(data)


def test_is_valid(read_csv):
    for cpf in read_csv:
        assert is_valid(cpf.raw_cpf)


def test_not_valid_cpf():
    with pytest.raises(InvalidCPFError):
        is_valid("123456")


def test_too_short_cpf():
    assert not is_valid(cpf="12345", autopad=False)


def test_too_long_cpf():
    assert not is_valid(cpf="123456789101", autopad=False)


def test_format(read_csv):
    for cpf in read_csv:
        assert format(cpf.raw_cpf) == cpf.formated_cpf


def test_verification_digits(read_csv):
    for cpf in read_csv:
        length_raw = len(cpf.raw_cpf)
        trimmed = cpf.raw_cpf[:-2]
        expected_digits = cpf.raw_cpf[(length_raw - 2) :]
        assert verification_digits(cpf.raw_cpf) == (
            int(expected_digits[0]),
            int(expected_digits[1]),
        )


def test_random_raw(read_csv):
    for cpf in read_csv:
        assert is_valid(random(formatted=False))


def test_random_formated(read_csv):
    for cpf in read_csv:
        assert is_valid(random(formatted=True))
