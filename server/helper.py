from datetime import date, datetime
from typing import Optional


def parse_iso_date_str(s: Optional[str], default: date) -> date:
    if s is None:
        return default
    else:
        return date.fromisoformat(s)


def parse_iso_datetime_str(s: Optional[str], default: datetime) -> datetime:
    if s is None:
        return default
    else:
        return datetime.fromisoformat(s)
