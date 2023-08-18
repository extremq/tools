import datetime


def date_to_timestamp_start(date: str) -> int:
    # This is at 00:00:00
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date = date.replace(hour=0, minute=0, second=0)
    return int(date.timestamp())


def date_to_timestamp_end(date: str, utc_offset: int = 0) -> int:
    # This is at 23:59:59
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date = date.replace(hour=23, minute=59, second=59)
    return int(date.timestamp())


def timestamp_milis_to_datetime(timestamp: int, utc_offset: int = 0):
    date = datetime.datetime.fromtimestamp(timestamp / 1000)
    date = date.replace(tzinfo=datetime.timezone.utc)
    date = date.astimezone(datetime.timezone(datetime.timedelta(hours=utc_offset)))
    return date
