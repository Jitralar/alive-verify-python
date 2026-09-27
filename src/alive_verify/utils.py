from datetime import date, datetime


def serialize_date(value: date | str) -> str:
    if isinstance(value, datetime):
        raise TypeError("Expected date, not datetime.")

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, str):
        date.fromisoformat(value)
        return value

    raise TypeError("Expected date or ISO date string.")


def serialize_datetime(value: datetime | str) -> str:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must contain timezone information.")

        return value.isoformat()

    if isinstance(value, str):
        parsed = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError(
                "Datetime must contain timezone information."
            )

        return value

    raise TypeError("Expected datetime or ISO datetime string.")


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(
            "API datetime response does not contain timezone information."
        )

    return parsed