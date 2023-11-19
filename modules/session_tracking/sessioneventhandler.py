from bases.event_manager import event_manager
from setup.bot_instance import bot
from modules.session_tracking.activities import getActivity
from spqrapp.models import *


class SessionActions:
    def __init__(self, event_manager=event_manager):
        self.event = event_manager
        self.event.subscribe(self)

    """
    this function returns all members
    that are currently in a voice channel
    that is being tracked
    """

    async def changed_type_of_tracking(self, data):
        member = data["member"]
        state = data["state"]
        log = await ActivityLog.object.complete_log(member)
        # TODO: I should be able to just get the session from the activity log actually
        session = await Session.object.get_member_ongoing_log(member)
        await ActivityLog.object.create_activity_log(member, state, session)

    async def get_all_voice(self):
        # LATER: change if I want to expand on multiple servers
        guild = bot.get_guild(789814373434654731)
        members_in_voice = []

        for channel in guild.voice_channels:
            if getActivity(channel.id):
                for member in channel.members:
                    members_in_voice.append(member)
        return members_in_voice

    async def create_new_session(self, data):
        member = data["member"]
        after = data["state"]
        try:
            session = await Session.object.create_session_log(member, after)
            activity = await ActivityLog.object.create_activity_log(member, after, session)
        except Exception as e:
            print(e)

    async def end_session(self, member):
        # TODO: Test
        await ActivityLog.object.complete_log(member)
        await Session.object.complete_log(member)

        # LATER: send Message

    # TODO: call this when bot boots
    async def update_sessions_on_bot_restart(self):
        """
        this function is called when the bot boots it will
        close all sessions that were
        ongoing then start a new session for all members that are
        crently in a voice channel that is being tracked
        """
        # TODO: Test

        await ActivityLog.object.complete_all()
        await Session.object.complete_all()
        # await db.complete_all() # this is from the prisma orm times
        members_in_voice = await self.get_all_voice()
        for member in members_in_voice:
            data = {}
            data["member"] = await User.object.get_or_create_user(member)
            data["state"] = member.voice
            await self.create_new_session(data)


class SessionEventHandler(SessionActions):
    def __init__(self, event_manager=event_manager):
        self.event = event_manager
        self.event.subscribe(self)

    async def _bot_ready(self, bot):
        # TODO: comment this out when you are done
        # await User.object.delete_all()
        await self.update_sessions_on_bot_restart()

    async def _user_changed_type_of_tracking(self, data):
        await self.changed_type_of_tracking(data)

    async def _user_joins_tracking_channel(self, data):
        await self.create_new_session(data)

    async def _user_left_tracking_channel(self, data):
        member = data["member"]
        await self.end_session(member)

    async def _user_changed_tracking_channel(self, data):
        member = data["member"]
        after = data["state"]
        await self.end_session(member)
        if not getActivity(after.channel.id):
            return
        await self.create_new_session(data)

    async def _any_voice_state_update(self, data):
        member = data["member"]
        # await self.create_user_if_not_in_database(member)
        await User.object.get_or_create_user(member)


session_to_database = SessionEventHandler()
