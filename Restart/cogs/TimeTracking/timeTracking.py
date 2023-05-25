import datetime

import utils.Conditionals as cnd
# from vc import server
from Database import queries as db
from discord.ext import commands
from Settings.main_settings import bot

import cogs.TimeTracking.activities as act
import discord
from cogs.leaderboard.temp_leaderboard_class import leaderboard_manager

# LATER: Use snake_case for function and variable names instead of camelCase
# For example, change GetUserMomentLog to get_user_moment_log


# TODO: Separate the cogs from my modules


class TimeTracking(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.lb = leaderboard_manager

    # ON A VOICESTATE EVENT
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # await timelogs.makeMemberIfNotExists(member)
        if self.excluding_condition_is_met(before, after, member):
            return
        await self.create_user_if_not_in_database(member)

        if cnd.user_joins_tracking_channel(before, after):
            print(f"{member.name} joined channel")
            await self.create_new_session(member, after)
            await self.lb.create_leaderboard(member)
            return

        if cnd.user_changed_type_of_tracking(before, after):
            print(f"{member.name} changed activity type")
            try:  # WORKS UNTIL HERE
                await db.complete_activity(member, "activitylog")
                session = await db.get_ongoing_session(member)
                await db.create_activity_log(member, after, session.id)
            except Exception as e:
                print(e)
            return

        if cnd.userLeftChannel(after):
            # LATER: make the message function
            print("user left")
            await self.end_session(member)
            await leaderboard_manager.destroy_leaderboard(member)

            # await db.get_all("session")
            return

        if cnd.userChangedChannel(before, after):
            # LATER: make the message function
            print("user changed channel")
            await self.end_session(member)
            await db.get_all("session")
            if not act.getActivity(
                after.channel.id
            ):  # If its not not in the official list of activities
                return
            await self.create_new_session(member, after)
            return

    async def create_new_session(self, member, after):
        session = await db.create_session_log(member, after)
        activity = await db.create_activity_log(member, after, session.id)
        print(f"created a new session for {member.name}")

    async def end_session(self, member):
        await db.complete_activity(member, "activitylog")
        await db.complete_activity(member, "session")  # TODO TEST
        print(f"ended a session for {member.name}")
        await db.get_all("session")
        # LATER: send Message

    def excluding_condition_is_met(self, before, after, member):
        # EXCLUDING CONDITIONS

        if cnd.is_mute_or_deafen_update(before, after):
            return True
        if member.bot:
            return True
        return False

    async def create_user_if_not_in_database(self, member):
        user = await db.get_user(member)
        if user is None:
            await db.create_user(member)


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(TimeTracking(bot))


async def teardown(bot):
    return
