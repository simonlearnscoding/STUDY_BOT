from settings_switch import db

import discord
from cogs.activities.activities import VC_to_Activity
from discord.ext import commands
from vc import server

# TODO: Use snake_case for function and variable names instead of camelCase
# as per Python's PEP 8 style guide.
# For example, change GetUserMomentLog to get_user_moment_log


# RENAME MYCOG TO NAME OF THE MODULE
class TimeTracking(commands.Cog, Conditionals, UpdateTimeLogs):
    def __init__(self, bot):
        self.bot = bot

    # ON A VOICESTATE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if is_mute_or_deafen_update(before, after):
            print("user mute/unmute")
            return
        
        if member.bot:
            return
        self.makeMemberIfNotExists(member)
        
        if self.userJoinedChannel(before, after):
            print("User joined a channel")
            self.createMomentLogs(member, after)
            
        if self.userChangedActivityType(before, after):
            print("user changed activity type (cam/ss)")
            self.updateDailyLogActivity(member, after)
            return
        
        if self.userLeftChannel:
           return


    async def countMinutesPassed(self, whenJoined, whenLeft):
        # TODO: This function will take two dateTimes and return the number of minutes that have passed between them
        pass


class UpdateTimeLogs():

    def makeMemberIfNotExists(member):
        if not await db.isUserInDatabase(member):
            print("user not in database")
            await db.create_user(member)
    
    
    # TODO: test
    def getActivity(self, id):
        activity = VC_to_Activity[id]
        return activity
    
   async def createMomentLogs(member, after):
        activityType = await self.getActivityType(after)
        await db.createMomentLogEntry(member, after, activityType)
        await db.createMomentLogEntry(member, after, "total")
        return
   async def updateDailyLogActivityType(member, after): 
        activityType = await self.getActivityType(after)
        Log = db.GetUserMomentLog(member, after, activityType)
        Now = None  # TODO: replace with timestamp of now
        Log["minutes"] = self.countMinutesPassed(Log["whenJoined"], Now)
        db.updateUserDailyLog(Log, member)
        db.deleteMomentLog(Log)
   async def getActivityType(self, voicestate):
        # TODO: Depending on the VC channel they are in, return the activity type
        pass
    pass

class Conditionals():

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
    
    async def userChangedChannel(self, before, after):
        if not is_mute_or_deafen_update(before, after) and before.channel.id == after.channel.id:
                return True

    
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
