
from collections import defaultdict, namedtuple
def sum_durations(input_array):
    user_durations = defaultdict(int)
    user_status = defaultdict(bool)  # dictionary to track user status
    user_nicknames = {}  # dictionary to store user nicknames

    for log in input_array:
        user_id = log.userId
        duration = log.duration
        if log.nick is not None:
            user_nick = log.nick
        else:
            user_nick = f"User {user_id}"

        user_durations[user_id] += duration
        user_nicknames[user_id] = user_nick  # Store the user_nick
        if log.status == "ONGOING":
            user_status[user_id] = True

    output_array = []
    for user_id, duration in user_durations.items():
        online = user_status[user_id]

        # Get the user_nick from the user_nicknames dictionary
        user_nick = user_nicknames[user_id]

        # Convert duration to hours, minutes, and seconds
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        output_array.append(
            {
                "nick": user_nick,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
                "online": online,
            }
        )

    # Sort the output_array by duration in descending order
    sorted_output_array = sorted(
        output_array,
        key=lambda x: (x["hours"], x["minutes"], x["seconds"]),
        reverse=True,
    )

    return sorted_output_array


async def get_sum_duration_by_user():
    results = await create_query(
        "find_many",
        "activitylog",
    )
    return results
