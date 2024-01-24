

# I want to get all session_data that is part of a session
# where the sessions start today. so I need to pass a timezone that constitutes today start of day

from model_managers_tortoise.vc_events import calculate_time_difference
from tortoise_models import SessionData


async def get_all_sessiondata(server):
    start_of_day = 0  # todo get timestamp of start of day based on server timezone
    return await SessionData.filter(joined_at > start_of_day).all()


async def get_sessions_type_of_day(sessions, activity_record_type):
    session_datas = await sessions.filter(activity_record_type=activity_record_type).all()


async def collect_all_sessiondata(session_datas, users={}):
    for session in session_datas:
        if users{session_datas}:
            users{session.user_id} += session.duration_in_seconds
        else:
            users{session.user_id} = session.duration_in_seconds
    return users


def calculate_inbetreen(session, activity_type, midnight):
    pass
    total_time = session.total_time_in_seconds
    midnight = get_midnight_timestamp(server)
    time_after_midnight = calculate_time_difference_from_midnight(midnight, session.left_at)
    percent_to_count = calculate_percent(time_after_midnight, total_time)
    return percent_to_count


def get_time_in_percent(time, percent):
    return int((time / 100) * percent)


def calculate_percent(partial, total):
    # TODO: calculate how much partial is from total in percent
    # Return an int
    pass


def get_midnight_timestamp(server):
    pass  # TODO: this function


def calculate_time_difference_from_midnight(midnight, left_at):
    duration_in_seconds = int(round((midnight_timestamp - left_at).total_seconds())) + 3600


async def main(server):
    records_that_count = ['SS', 'BOTH', 'CAM']
    users = {}
    session_data_of_day = get_all_sessiondata(server)
    for record in records_that_count:
        sessions = await get_sessions_type_of_day(session_data_of_day, record)
        users = await collect_all_sessiondata(users, sessions)

    # TODO: get active sessions
    # TODO: get inbetween sessions


async def get_in_between_sessions(server):
    return await SessionData.filter(joined_at < start_of_day, left_at > start_of_day).all()
