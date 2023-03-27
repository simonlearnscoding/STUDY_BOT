from datetime import datetime

import pytz

cet_timezone = pytz.timezone("CET")


# HI DERK
def timestamp():
    timestamp = datetime.now(cet_timezone)
    timestamp = timestamp.isoformat()
    return timestamp
