from prisma import Prisma


class Database:
    def __init__(self, db):
        self.db = db

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()

    @classmethod
    async def create(cls):
        db = Prisma(
            datasource={
                "provider": "mysql",
                "url": "mysql://simon:spqr-server@192.53.122.228/discordjs",
            }
        )
        instance = cls(db)
        await instance.connect()
        return instance


# --- DELETE STUFF ---


async def delete_all_from_table(table):
    try:
        await create_query(table, "delete_many")
    except Exception as e:
        print(e)


# --- CREATE STUFF ---


async def create_object(table, data):
    try:
        object = await create_query(table, "create", data=data)
        print(f"created {table} object: {object}")
        return object
    except Exception as e:
        print(e)


# --- UPDATE STUFF ---
async def update_entries(where, data, tablename):
    try:
        # Update the status to COMPLETED
        updated_entries = await create_query(
            tablename, "update", where=where, data=data
        )
        return updated_entries
    except Exception as e:
        print(e)


# --- GET STUFF ---


async def get_all(table):
    try:
        all = await create_query(table, "find_many", take=5)
        return all
    except Exception as e:
        print(e)


# --- BASICS ---
async def raw_query(query):
    db = await Database.create()
    try:
        return await db.query_raw(query)
    except Exception as e:
        print(e)
    await db.disconnect()


async def update(where, data):
    db = await Database.create()
    try:
        return await db.db.activitylog.update_many(where=where, data=data)
    except Exception as e:
        print(e)


async def create_query(table, action, **options):
    db = await Database.create()
    try:
        taybl = getattr(db.db, table)
        method = getattr(taybl, action)  # Get the method from the db instance
        return await method(**options)  # Call the method with the given arguments
    except Exception as e:
        print(e)
    await db.disconnect()
