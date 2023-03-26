
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
