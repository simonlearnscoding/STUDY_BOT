import datetime

from Backend.activities.activities import VC_to_Activity
from settings_switch import db


async def makeMemberIfNotExists(member):
    pass
    # TODO: Test
    # print("checking if user in db")
    # return
    # if not await db.isUserInDatabase(member):
    #     print("user not in database")
    #     await db.create_user(member)


def getActivity(id):
    activity = VC_to_Activity[id]
    return activity


class log:
    def __init__(self, db):
        self.db = db

    async def createMomentLogs(self, member, after):
        data = {}
        print(f"db is{self.db}")
        print("creating moment log")
        data["type"] = await getActivityType(after)
        data["activity"] = getActivity(after.channel.id)
        data["timestamp"] = datetime.datetime.now().isoformat()
        data["userId"] = member.id
        await db.logsnow.create(data)
        data["type"] = "total"
        await db.logsnow.create(data)

        print(await db.logsnow.find_many(where={"type": "total"}))
        return


async def updateDailyLogActivityType(member, after):
    # TODO: Test
    return
    activityType = await self.getActivityType(after)
    Log = db.GetUserMomentLog(member, after, activityType)
    Now = None  # TODO: replace with timestamp of now
    Log["minutes"] = self.countMinutesPassed(Log["whenJoined"], Now)
    db.updateUserDailyLog(Log, member)
    db.deleteMomentLog(Log)


async def getActivityType(voicestate):
    # TODO:depending on whether they have cam on etc
    return "activity"
