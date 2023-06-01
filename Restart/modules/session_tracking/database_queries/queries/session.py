import modules.session_tracking.activities as act
from bases.connector import *
from utils.time import time_difference, timestamp

# THIS IS AN EXAMPLE SCRIPT FOR INTERACTING WITH THE DB
# https://prisma-client-py.re
# adthedocs.io/en/stable/getting_started/quickstart/


# --- GET STUFF ---


async def get_ongoing_session(user):
    return await get_ongoing_entry(user, "session")


async def get_ongoing_activity(user):
    print("activitylog")
    return await get_ongoing_entry(user, "activitylog")


async def get_ongoing_entry(user, tablename):
    where = {"AND": [{"userId": int(user.id)}, {"status": "ONGOING"}]}
    try:
        # Find the entry with user id and ONGOING status
        existing_entry = await create_query(tablename, "find_first", where=where)
        return existing_entry
    except Exception as e:
        print(e)
        return None


# --- UPDATE STUFF ---


async def complete_activity(user, table):

    activity = await get_ongoing_entry(user, table)
    start = activity.joinedAt
    where = {"AND": [{"status": "ONGOING"}, {"userId": int(user.id)}]}

    length = time_difference(start)
    now = timestamp()
    # xp = calculate_xp() LATER: calculate xp
    data = {"duration": length, "status": "COMPLETED", "leftAt": now}

    try:
        update = await create_query(table, "update_many", where=where, data=data)
        return update
    except Exception as e:
        print(e)


# --- DELETE STUFF ---


async def delete_all_sessions():
    try:
        await delete_all_from_table("session")
    except Exception as e:
        print(e)


async def delete_all_activities():
    try:
        await delete_all_from_table("activitylog")
    except Exception as e:
        print(e)


# --- CREATE STUFF ---


async def create_activity_if_not_exist(activity):
    where = {"name": activity["name"]}
    try:
        # Check if the activity already exists
        existing_activity = await create_query(
            "ActivityType", "find_first", where=where
        )
    except Exception as e:
        print(e)
        existing_activity = None

    if existing_activity:
        return existing_activity
    else:
        try:
            # Create the activity
            created_activity = await create_object("ActivityType", activity)
            return created_activity
        except Exception as e:
            print(e)
            return None


async def create_activity_log(member, after, sessionId):
    data = {
        # TODO unable to match
        "sessionId": sessionId,
        "activityType": act.getActivityType(after),
        "activity": act.getActivity(after.channel.id),
        "joinedAt": timestamp(),
        "userId": member.id,
        "nick": member.nick,
    }
    return await create_object("activitylog", data)


async def create_session_log(member, after):
    data = {
        "activity": act.getActivity(after.channel.id),
        "joinedAt": timestamp(),
        "userId": member.id,
        "nick": member.nick,
    }
    table = "session"
    try:
        return await create_object(table, data)
    except Exception as e:
        print(e)
