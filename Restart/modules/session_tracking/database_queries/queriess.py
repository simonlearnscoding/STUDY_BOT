from modules.session_tracking.database_queries.queries.session import *


# THIS IS AN EXAMPLE SCRIPT FOR INTERACTING WITH THE DB
# https://prisma-client-py.re
# adthedocs.io/en/stable/getting_started/quickstart/


async def create_if_not_exist(activity):
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
        print(f"Activity {activity['name']} already exists.")
        return existing_activity
    else:
        try:
            # Create the activity
            created_activity = await create_object("ActivityType", activity)
            return created_activity
        except Exception as e:
            print(e)
            return None


async def get_user(member):
    where = {"id": int(member.id)}
    try:
        user = await create_query("user", "find_first", where=where)
        return user
    except Exception as e:
        print(e)

#TODO: this function exists twice (in user_queries aswell, I need to refactor the DB module badly!

async def create_user(member):
    # LATER: Debug This
    data = {
        "id": member.id,
        "name": member.name,
    }
    await create_object("user", data)


# --- PLAYGROUND ---


async def get_all_ongoing_entries(user, tablename):
    where = {"userId": int(user.id), "status": "ONGOING"}
    try:
        # Find all entries with user id and ONGOING status
        ongoing_entries = await create_query(tablename, "find_many", where=where)
        return ongoing_entries
    except Exception as e:
        print(e)
        return None


async def change_all_ongoing_to_completed(user, tablename):
    # Get all the entries with user id and ONGOING status
    ongoing_entries = await get_all_ongoing_entries(user, tablename)

    if ongoing_entries:
        # Change the status of all the ongoing entries to COMPLETED
        updated_entries = await change_to_completed(ongoing_entries, tablename)
        return updated_entries
    else:
        print(f"No ongoing entries found with user id {user.id}")
        return None


async def get_user_ongoing_entry(user, tablename):
    where = {"userId": int(user.id), "status": "ONGOING"}
    try:
        # Find the entry with user id and ONGOING status
        existing_entry = await create_query(tablename, "find_first", where=where)
        return existing_entry
    except Exception as e:
        print(e)
        return None


async def change_to_completed(entries, tablename):
    if not isinstance(entries, list):
        entries = [entries]

    updated_entries = []
    for entry in entries:
        where = {"id": entry["id"]}
        try:
            # Update the status to COMPLETED
            data = {"status": "COMPLETED"}
            updated_entry = await create_query(
                tablename, "update", where=where, data=data
            )
            print(f"Updated entry {entry} to COMPLETED")
            updated_entries.append(updated_entry)
        except Exception as e:
            print(e)

    return updated_entries


async def update_user_ongoing_to_completed(user, tablename):
    # Get the entry with user id and ONGOING status
    existing_entry = await get_user_ongoing_entry(user, tablename)

    if existing_entry:
        # Change the status of the entry to COMPLETED
        updated_entry = await change_to_completed(existing_entry, tablename)
        return updated_entry
    else:
        print(f"No entry found with user id {user.id} and status ONGOING")
        return None


async def delete_all():
    try:
        await create_query("user", "delete_many")
    except Exception as e:
        print(e)


async def get_all(table):
    try:
        all = await create_query(table, "find_many", take=5)
        return all
    except Exception as e:
        print(e)


async def create_activity_log(member, after, sessionId):
    data = {
        # TODO unable to match
        "sessionId": sessionId,
        "activityType": act.getActivityType(after),
        "activity": act.getActivity(after.channel.id),
        "joinedAt": timestamp(),
        "userId": member.id,
        "nick": member.name,
    }
    try:
        await create_object("activitylog", data)
    except Exception as e:
        print(e)

async def create_session_log(member, after):
    data = {
        "activity": act.getActivity(after.channel.id),
        "joinedAt": timestamp(),
        "userId": member.id,
    }
    table = "session"
    try:
        return await create_object(table, data)
    except Exception as e:
        print(e)


async def create_object(table, data):
    try:
        object = await create_query(table, "create", data=data)
        print(f"created {table} object: {object}")
        return object
    except Exception as e:
        print(e)
