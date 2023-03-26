from datetime import datetime

import pytz

cet_timezone = pytz.timezone("CET")


def timestamp():
    timestamp = datetime.now(cet_timezone)
    timestamp = timestamp.isoformat()
    return timestamp
