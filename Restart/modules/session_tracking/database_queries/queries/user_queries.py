import bases.connector as db


# THIS IS AN EXAMPLE SCRIPT FOR INTERACTING WITH THE DB
# https://prisma-client-py.re
# adthedocs.io/en/stable/getting_started/quickstart/


# --- GET THINGS ---
async def get_user(member):
    where = {"id": int(member.id)}
    try:
        user = await db.create_query("user", "find_first", where=where)
        return user
    except Exception as e:
        print(e)

async def change_user_filter(member, filter):
    #TODO: I HAVE TO REPLACE THIS WITH
    where = {"id": int(member.id)}
    data = {"filter": filter}
    try:
        await db.create_query("user", "update", where=where, data=data)
    except Exception as e:
        print(e)

# REVIEW: Do I need to create a user for py if they don't exist?
async def create_user(member):
    # LATER: Debug This
    data = {
        "id": member.id,
        "name": member.name,
    }
    await db.create_object("user", data)

async def delete_all_users():
    try:
        await db.delete_all_from_table("user")
    except Exception as e:
        print(e)
