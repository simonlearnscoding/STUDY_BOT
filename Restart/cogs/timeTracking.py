from activities import VC_to_Activity
from settings_switch import db

import discord
from discord.ext import commands
from vc import server

# TODO: Use snake_case for function and variable names instead of camelCase
# as per Python's PEP 8 style guide.
# For example, change GetUserMomentLog to get_user_moment_log


# RENAME MYCOG TO NAME OF THE MODULE
class TimeTracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ON A VOICESTATE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # TODO: remove this after it's been tested
        print(self.getActivity(after.channel.id))
        if is_mute_or_deafen_update(before, after):
            return
        if member.bot:
            return

        if not await db.isUserInDatabase(member):
            print("user not in database")
            # TODO: Test
            await db.create_user(member)

        # IF USER JUST JOINED A CHANNEL
        if self.userJoinedChannel(before, after):
            print("User joined a channel")
            # CREATE A LOG ENTRY WITH LOG THE TIME THEY JOINED
            await db.createMomentLogEntry(member, after)
            return

        # IF HE DIDNT JUST JOIN A CHANNEL IT MEANS
        # HE EITHER JUST LEFT A CHANNEL OR
        # HIS STATE CHANGED (TURNED ON CAM ETC)
        # SO WE HAVE TO LOG THIS IN THE DAILY LOGS
        # AND DELETE THE OLD LOG ENTRY

        Log = db.getUserMomentLog(member, after)
        Now = None  # TODO: replace with timestamp of now
        Log["minutes"] = self.countMinutesPassed(Log["whenJoined"], Now)

        db.updateUserDailyLog(Log, member)
        db.deleteMomentLog(Log)
        db.countSumOfToday(member)

        if userLeftChannel:
            return

        db.createMomentLogEntry(member, after)

    def userLeftChannel(after):
        # TODO: TEST
        if after.channel == None:
            return True

    def userJoinedChannel(self, before, after):
        # A function that returns true if the user just joined a channel
        if before.channel is None and after.channel is not None:
            print("user joined a channel")
            # TODO: Test
            return True

    # TODO: test
    def getActivity(self, id):
        activity = VC_to_Activity[id]
        print(activity)
        return activity

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
