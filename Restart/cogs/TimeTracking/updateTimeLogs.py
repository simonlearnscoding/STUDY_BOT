from settings_switch import db

from cogs.activities.activities import VC_to_Activity


class UpdateTimeLogs:
    async def makeMemberIfNotExists(self, member):
        pass
        # TODO: Test
        # print("checking if user in db")
        # return
        # if not await db.isUserInDatabase(member):
        #     print("user not in database")
        #     await db.create_user(member)

    def getActivity(self, id):
        activity = VC_to_Activity[id]
        return activity

    async def createMomentLogs(self, member, after):
        # TODO: Test
        return
        activityType = await self.getActivityType(after)
        await db.createMomentLogEntry(self, member, after, activityType)
        await db.createMomentLogEntry(self, member, after, "total")
        return

    async def updateDailyLogActivityType(self, member, after):
        # TODO: Test
        return
        activityType = await self.getActivityType(after)
        Log = db.GetUserMomentLog(member, after, activityType)
        Now = None  # TODO: replace with timestamp of now
        Log["minutes"] = self.countMinutesPassed(Log["whenJoined"], Now)
        db.updateUserDailyLog(Log, member)
        db.deleteMomentLog(Log)

    async def getActivityType(self, voicestate):
        # TODO: Depending on the VC channel they are in, return the activity type
        pass
