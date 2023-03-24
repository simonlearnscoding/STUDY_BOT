import discord
from discord.ext import commands
from settings_switch import db
from vc import server


#TODO: Use snake_case for function and variable names instead of camelCase
# as per Python's PEP 8 style guide.
# For example, change GetUserMomentLog to get_user_moment_log

# RENAME MYCOG TO NAME OF THE MODULE
class TimeTracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO:
    # ON A VOICESTATE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if(is_mute_or_deafen_update(before, after)):
            print("mute, deafen or something like that")
            return
        if member.bot:
            return

        # TODO: We have to test it muting/unmuting counts as a voicestate update
        if not await self.isUserInDatabase(member):
            print("user not in database")
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

def is_mute_or_deafen_update(before, after):
    # Check if the user joined or left a voice channel
    if before.channel != after.channel:
        return False

    # Check if the user started or stopped streaming
    if before.self_stream != after.self_stream:
        return False

    # Check if the user started or stopped video
    if before.self_video != after.self_video:
        return False

    # Check if the user muted or unmuted themselves
    if before.self_mute != after.self_mute:
        return True

    # Check if the user deafened or undeafened themselves
    if before.self_deaf != after.self_deaf:
        return True

    return False

async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(TimeTracking(bot))


async def teardown(bot):
    return
