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
    gmt_plus_two = pytz.timezone("Etc/GMT-2")
    now = datetime.now(gmt_plus_two)
    [start, end] = [None, now]  # end is always set as now timestamp

    if timeframe == "today":
        start = datetime.combine(now.date(), time(0, 0, tzinfo=gmt_plus_two))
    elif timeframe == "this_week":
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    elif timeframe == "this_month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return {"start": start, "end": end}