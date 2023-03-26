import datetime

# from vc import server
from Database import queries as db


import utils.Conditionals as cnd
import discord
from discord.ext import commands

# TODO: Use snake_case for function and variable names instead of camelCase
# as per Python's PEP 8 style guide.
# For example, change GetUserMomentLog to get_user_moment_log


# RENAME MYCOG TO NAME OF THE MODULE
class TimeTracking(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    # ON A VOICESTATE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # await db.delete_all()
        if cnd.is_mute_or_deafen_update(before, after):
            return

        if member.bot:
            return

        # await timelogs.makeMemberIfNotExists(member)

        if cnd.userJoinedChannel(before, after):
            user = await db.get_user(member)
            print(user)
            if user is None:
                await db.create_user(member)
            await db.createMomentLogs(db, member, after)
            return

        if cnd.userChangedActivityType(before, after):
            if not await db.isUserInDatabase(member):
                await db.create_user(member)
            # await timelogs.updateDailyLogActivity(member, after)
            return

        if cnd.userLeftChannel(after):
            if not await db.isUserInDatabase(member):
                await db.create_user(member)
            return

        if cnd.userChangedChannel:
            if not await db.isUserInDatabase(member):
                await db.create_user(member)
            return

    async def countMinutesPassed(self, whenJoined, whenLeft):
        # TODO: This function will take two dateTimes and return the number of minutes that have passed between them
        pass


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(TimeTracking(bot))


async def teardown(bot):
    return
