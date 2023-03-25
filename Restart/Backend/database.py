import asyncio
from contextlib import asynccontextmanager

from prisma import Prisma
from datetime import datetime, timezone

# THIS IS AN EXAMPLE SCRIPT FOR INTERACTING WITH THE DB
# https://prisma-client-py.re
# adthedocs.io/en/stable/getting_started/quickstart/


class db:
    def __init__(self, Database):
        self.db = Database

    async def createMomentLogEntry(self, member, time, type, activity):
        data = {
            "activity": activity,
            "timestamp": time,
            "type": type,
            "userId": member["id"],
        }
        created_user = await self.db.logsnow.create(data)
        return created_user

    async def createMomentLogs(self, member, after):
        db = await Database.create()
        data = {}
        data["type"] = "CAM" #await getActivityType(after)
        data["activity"] = "hi" # getActivity(after.channel.id)
        timestamp = datetime.now(timezone.utc)
        data["timestamp"] = timestamp.isoformat()

        data["userId"] = {
            "connect": {
                "id": member["id"]
            }
        }
        print(data)
        try:
            await db.db.logsnow.create(data)
            print("it worked")
        except Exception as e:
            print(e)
        data["type"] = "total"
        await self.db.logsnow.create(data)

        print(await self.db.logsnow.find_many(where={"type": "total"}))
        await db.disconnect()
        return

    def getUserMomentLog(self, member, after):
        # TODO: GET FROM DB
        return {}

    def deleteMomentLog(self, log):
        # TODO: delete user log
        pass

    async def isUserInDatabase(self, member):
        #TODO: Move this to conditionals probably
        db = await Database.create()
        db = db.db
        try:
            user = await db.user.find_unique(
                where={'id' : member.id},)
        except Exception as e:
            print(e)
        if not user:
            return False
        return True
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
        db = await Database.create()
        db = db.db
        #TODO: YOU ARE HERE
        user_data = {
            "id": user["id"],
            "name": user["username"],
            "bot": user["bot"],
            "nick": user["nick"],
        }
        try:
            created_user = await db.user.create(user_data)
            print(f"created user{created_user}")
            return created_user
        except Exception as e:
            print(e)





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
