import datetime

# from Backend.activities.activities import VC_to_Activity
# from settings_switch import db
import cogs.TimeTracking.activities as act


async def makeMemberIfNotExists(member):
    pass
    # TODO: Test
    # print("checking if user in db")
    # return
    # if not await db.isUserInDatabase(member):
    #     print("user not in database")
    #     await db.create_user(member)


class log:
    def __init__(self, db):
        self.db = db

    async def createMomentLogs(self, member, after):
        data = {}
        data["type"] = await act.getActivityType(after)
        data["activity"] = act.getActivity(after.channel.id)
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
