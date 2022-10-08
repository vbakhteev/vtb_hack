import datetime
from zoneinfo import ZoneInfo


def get_current_datetime() -> datetime.datetime:
    return datetime.datetime.now(ZoneInfo("Europe/Moscow"))
