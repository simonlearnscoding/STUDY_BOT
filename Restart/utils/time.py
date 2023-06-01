from datetime import datetime, time, timedelta, timezone

import pytz

cet_timezone = pytz.timezone("CET")


# HI DERK
def timestamp():
    timestamp = datetime.now(cet_timezone)
    timestamp = timestamp.isoformat()
    return timestamp


def time_difference(start):
    # takes two time objects and Calculates the time diff between two points in seconds
    now = datetime.now(cet_timezone)

    length = now - start
    td_in_sec = length.total_seconds()
    seconds = int(td_in_sec)
    return int(seconds)


def get_start_end(timeframe):
    gmt_plus_one = pytz.timezone("etc/gmt-1")
    now = datetime.now(gmt_plus_one)

    [start, end] = [None, None]
    if timeframe == "today":
        start = datetime.combine(now.date(), time(0, 0, tzinfo=gmt_plus_one))
        end = start + timedelta(days=1)
    elif timeframe == "week":
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=7)

    return {"start": start, "end": end}
