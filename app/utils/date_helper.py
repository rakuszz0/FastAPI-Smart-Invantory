from datetime import datetime
from zoneinfo import ZoneInfo


JAKARTA_TZ = ZoneInfo("Asia/Jakarta")


def now():

    return datetime.now(JAKARTA_TZ)


def format_datetime(
    dt: datetime,
    fmt: str = "%Y-%m-%d %H:%M:%S"
):

    if dt is None:
        return None

    return dt.strftime(fmt)


def to_iso(
    dt: datetime
):

    if dt is None:
        return None

    return dt.isoformat()


def parse_datetime(
    value: str,
    fmt: str = "%Y-%m-%d %H:%M:%S"
):

    return datetime.strptime(
        value,
        fmt
    )