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

async def create_query(table, action, **options):
    db = await Database.create()
    try:
        taybl = getattr(db.db, table)
        method = getattr(taybl, action) # Get the method from the db instance
        return await method(**options)  # Call the method with the given arguments
    except Exception as e:
        print(e)
    await db.disconnect()

