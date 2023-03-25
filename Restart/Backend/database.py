import asyncio
from contextlib import asynccontextmanager

from prisma import Prisma

# THIS IS AN EXAMPLE SCRIPT FOR INTERACTING WITH THE DB
# https://prisma-client-py.re
# adthedocs.io/en/stable/getting_started/quickstart/


class Database:
    def __init__(self, db):
        self.db = db

    async def connect(self):
        await self.db.connect()

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

    async def createMomentLogEntry(self, member, after, type):
        # TODO: Create a log entry for the user in the database
        pass

    def getUserMomentLog(self, member, after):
        # TODO GET FROM DB
        return {}

    def deleteMomentLog(self, log):
        # TODO delete user log
        pass

    async def isUserInDatabase(self, member):
        # TODO: Check if the user is in the database
        pass

    def getUserDailyLog(self, member, ActivityType):
        # TODO: Find user object in Daily logs of Today where ActivityType == the activity he just did
        pass

    def updateUserDailyLog(self, log, member):
        TodayLog = self.getUserTodayLog(member, log["activityType"])
        # TODO: if TodayLog is None, create a new log entry for the user
        if TodayLog is None:
            TodayLog = {
                "user": member.id,
                "activityType": log["activityType"],
                "minutes": log["minutes"],
            }
        else:
            TodayLog["minutes"] += log["minutes"]
        # TODO: update the log entry in the database

    async def create_user(self, user):
        user_data = {
            "id": user["id"],
            "name": user["username"],
            "bot": user["bot"],
            "nick": user["nick"],
        }
        created_user = await self.db.user.create(user_data)
        return created_user


user = {
    "id": 123456782022905678,
    "username": "TestUser",
    "discriminator": "1234",
    "nick": "Testy",
    "avatar": "a_bcd1234efgh5678ijkl9012mnop3456",
    "bot": False,
    "locale": "en-US",
    "verified": "true",
    "email": "testuser@example.com",
    "flags": 64,
    "premium_type": 1,
    "public_flags": 64,
}
