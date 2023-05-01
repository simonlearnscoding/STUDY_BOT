from datetime import datetime

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
