from datetime import date, datetime, timezone

import pytest

from alive_verify.utils import (
    parse_date,
    parse_datetime,
    serialize_date,
    serialize_datetime,
)


def test_serialize_date():
    result = serialize_date(
        date(2026, 9, 27)
    )

    assert result == "2026-09-27"


def test_serialize_datetime():
    value = datetime(
        2026,
        9,
        27,
        10,
        30,
        tzinfo=timezone.utc,
    )

    result = serialize_datetime(value)

    assert result == "2026-09-27T10:30:00+00:00"


def test_datetime_without_timezone_fails():
    value = datetime(
        2026,
        9,
        27,
        10,
        30,
    )

    with pytest.raises(ValueError):
        serialize_datetime(value)


def test_parse_date():
    result = parse_date("2026-09-27")

    assert result == date(2026, 9, 27)


def test_parse_datetime():
    result = parse_datetime(
        "2026-09-27T10:30:00+00:00"
    )

    assert result == datetime(
        2026,
        9,
        27,
        10,
        30,
        tzinfo=timezone.utc,
    )