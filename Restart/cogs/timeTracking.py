# TODO: Here I will create the functions that track every time a user joins a voice channel and leaves a voice channel
# AND LOG ONE OF THE FOLLOWING FOR STATES: 1. no cam and no ss, 2. no cam and ss, 3. cam and no ss, 4. cam and ss
from settings_switch import db

import discord
from discord.ext import commands
from vc import server


# RENAME MYCOG TO NAME OF THE MODULE
class TimeTracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO:
    # ON A VOICESTATE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # TODO: We have to test it muting/unmuting counts as a voicestate update
        print("Voice state update just happened")

        if not self.isUserInDatabase(member):
            # TODO: create user in database
            # the function for this is in Backend/database.py)
            pass

        # IF USER JUST JOINED A CHANNEL
        if self.userJoinedChannel(before, after):
            print("User joined a channel")
            # CREATE A LOG ENTRY WITH LOG THE TIME THEY JOINED
            await self.createLogEntry(member, after)

        # IF HE DIDNT JUST JOIN A CHANNEL IT MEANS
        # HE EITHER JUST LEFT A CHANNEL OR
        # HIS STATE CHANGED (TURNED ON CAM ETC)
        # SO WE HAVE TO LOG THIS IN THE DAILY LOGS
        # AND DELETE THE OLD LOG ENTRY

        Log = self.GetUserMomentLog(member, after)
        Now = None  # TODO: replace with timestamp of now
        Log["minutes"] = self.countMinutesPassed(Log["whenJoined"], Now)

        self.updateDailyLog(Log, member)
        self.deleteMomentLog(Log)
        self.CountSumOfToday(member)

    def updateDailyLog(self, log, member):
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

    def CountSumOfToday(self, member):
        # TODO:
        # after we update the daily log, we have to count the sum
        # of all the minutes of different activity types for the leaderboard
        pass

    def deleteMomentLog(self, log):
        pass

    def userJoinedChannel(self, before, after):
        # A function that returns true if the user just joined a channel
        if before.channel is None and after.channel is not None:
            return True

    def GetUserMomentLog(self, member, after):
        # TODO GET FROM DB
        return {}

    def getUserTodayLog(self, member, ActivityType):
        # TODO: Find user object in Daily logs of Today where ActivityType == the activity he just did
        pass

    async def isUserInDatabase(self, member):
        # TODO: Check if the user is in the database
        pass

    async def createLogEntry(self, member, after):
        # TODO: Create a log entry for the user in the database
        pass

    async def countMinutesPassed(self, whenJoined, whenLeft):
        # TODO: This function will take two dateTimes and return the number of minutes that have passed between them
        pass

    async def getActivityType(self, after):
        # TODO: Depending on the VC channel they are in, return the activity type
        pass


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(TimeTracking(bot))


async def teardown(bot):
    return
