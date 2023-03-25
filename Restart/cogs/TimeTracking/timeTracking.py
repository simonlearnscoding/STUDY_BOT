from settings_switch import db

import discord
from cogs.activities.activities import VC_to_Activity
from cogs.TimeTracking.Conditionals import Conditionals
from cogs.TimeTracking.updateTimeLogs import UpdateTimeLogs
from discord.ext import commands
from vc import server

# TODO: Use snake_case for function and variable names instead of camelCase
# as per Python's PEP 8 style guide.
# For example, change GetUserMomentLog to get_user_moment_log


# RENAME MYCOG TO NAME OF THE MODULE
class TimeTracking(commands.Cog, Conditionals, UpdateTimeLogs):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    # ON A VOICESTATE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.is_mute_or_deafen_update(before, after):
            print("user mute/unmute")
            return

        if member.bot:
            return

        await self.makeMemberIfNotExists(member)

        if self.userJoinedChannel(before, after):
            print("user joined channel")
            await self.createMomentLogs(member, after)
            return

        if self.userChangedActivityType(before, after):
            print("user changed activity")
            await self.updateDailyLogActivity(member, after)
            return

        if self.userLeftChannel(after):
            print("user left channel")
            return

        if self.userChangedChannel:
            print("user changed channel")
            return

    async def countMinutesPassed(self, whenJoined, whenLeft):
        # TODO: This function will take two dateTimes and return the number of minutes that have passed between them
        pass


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(TimeTracking(bot))


async def teardown(bot):
    return
