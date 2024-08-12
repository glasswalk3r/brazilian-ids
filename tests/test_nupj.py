import pytest
import inspect

from brazilian_ids.functions.labor_dispute.nupj import (
    is_valid,
    parse,
    pad,
    NUPJ,
    Court,
    Courts,
    InvalidCourtIdError,
    InvalidSegmentIdError,
)

# NUPJ generator
# https://processogerador.paulosales.com.br/


@pytest.mark.parametrize("nupj", ("62367378320244025398", "7666699020243004820"))
def test_is_valid(nupj):
    assert is_valid(nupj)


@pytest.mark.parametrize(
    "nupj", ("6236737-83.2024.4.02.5398", "766669-90.2024.3.00.4820")
)
def test_is_valid_formatted(nupj):
    assert is_valid(nupj)


@pytest.mark.parametrize(
    "given,expected",
    (("766669-90.2024.3.00.4820", "07666699020243004820"),),
)
def test_pad(given, expected):
    assert pad(given) == expected


@pytest.mark.parametrize(
    "given,expected",
    (
        (
            "6236737-83.2024.4.02.5398",
            NUPJ(
                lawsuit_id="6236737",
                first_digit=8,
                second_digit=3,
                year=2024,
                segment=4,
                court_id="02",
                lawsuit_city="5398",
            ),
        ),
        (
            "766669-90.2024.3.00.4820",
            NUPJ(
                lawsuit_id="0766669",
                first_digit=9,
                second_digit=0,
                year=2024,
                segment=3,
                court_id="00",
                lawsuit_city="4820",
            ),
        ),
    ),
)
def test_parse(given, expected):
    assert parse(given) == expected


def test_court_class():
    assert inspect.isclass(Court)


def test_court_class_invalid_id():
    with pytest.raises(InvalidCourtIdError):
        Court(id=0, acronym="foobar", description="barfoo")


def test_court_instance():
    instance = Court(id=1, acronym="foobar", description="barfoo")
    wanted = ("acronym", "id", "description")

    for attrib in wanted:
        assert hasattr(instance, attrib)

    with pytest.raises(AttributeError):
        instance.id = 2

    with pytest.raises(AttributeError):
        instance.acronym = "xxx"

    with pytest.raises(AttributeError):
        instance.description = "yyyyy"

    assert str(instance) == "Court foobar, barfoo"
    assert repr(instance) == 'Court(id=1, acronym="foobar", description="barfoo")'


def test_courts_class():
    assert inspect.isclass(Courts)
    assert inspect.ismethod(Courts.court)
    assert inspect.ismethod(Courts.court_acronym)
    assert inspect.ismethod(Courts.segment)
    assert inspect.ismethod(Courts.total_courts)


def test_court_acronym():
    assert Courts.court_acronym(segment_id=9, court_id="13") == "TJMMG"


def test_court_acronym_invalid_segment_id():
    with pytest.raises(InvalidSegmentIdError):
        Courts.court_acronym(segment_id=0, court_id="13")


def test_court_acronym_invalid_court_id():
    with pytest.raises(InvalidCourtIdError):
        Courts.court_acronym(segment_id=4, court_id=0)


def test_courts_court():
    instance = Courts.court(segment_id=4, court_id="04")
    assert isinstance(instance, Court)
    assert instance.id == "04"
    assert instance.acronym == "TRF04"
    assert instance.description == "Tribunal Regional Federal da 4ª Região"


def test_courts_total_courts():
    assert Courts.total_courts() == 9


def test_courts_segment():
    assert Courts.segment(1) == "Supremo Tribunal Federal"


def test_courts_segment_invalid_id():
    with pytest.raises(InvalidSegmentIdError):
        Courts.segment(0)

    with pytest.raises(InvalidSegmentIdError):
        Courts.segment(99)
