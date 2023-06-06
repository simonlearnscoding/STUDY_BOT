from bases.event_manager import event_manager
from modules.session_tracking.activities import getActivity
from modules.session_tracking.database_queries import queriess as db
from setup.bot_instance import bot
from modules.session_tracking.activities import getActivity

class safety_checks:
    def __init__(self, event_manager=event_manager):
        self.event = event_manager
        self.event.subscribe(self)
    """
    this function returns all members that are currently in a voice channel that is being tracked
    """
    async def get_all_voice(self):
        # TODO: test this function
        guild = bot.get_guild(789814373434654731) #LATER: change if I want to expand on multiple servers
        members_in_voice = []
        
        for channel in guild.voice_channels:
            if getActivity(channel.id):
                for member in channel.members:
                    members_in_voice.append(member)
        return members_in_voice


    # TODO: call this when bot boots
    async def update_on_restart(self):
        """
        this function is called when the bot boots it will
        close all sessions that were
        ongoing then start a new session for all members that are
        crently in a voice channel that is being tracked
        """
        await db.complete_all()
        members_in_voice = await self.get_all_voice()
        for member in members_in_voice:
            data = {}
            data["member"] = member
            data["state"] = member.voice
            await self.create_user_if_not_in_database(member)
            await self.create_new_session(data)


class Session_to_database(safety_checks):
    def __init__(self, event_manager=event_manager):
        self.event = event_manager
        self.event.subscribe(self)
        pass

    async def _bot_ready(self, bot):
        await self.update_on_restart()

    async def _user_changed_type_of_tracking(self, data):
        await self.changed_type_of_tracking(data)

    async def _user_joins_tracking_channel(self, data):
        await self.create_new_session(data)

    async def _user_left_tracking_channel(self, data):
        member = data["member"]
        await self.end_session(member)

    async def changed_type_of_tracking(self, data):
        member = data["member"]
        state = data["state"]
        await db.complete_activity(member, "activitylog")
        session = await db.get_ongoing_session(member)
        await db.create_activity_log(member, state, session.id)

    async def _user_changed_tracking_channel(self, data):
        member = data["member"]
        after = data["state"]

        await self.end_session(member)
        await db.get_all("session")
        if not getActivity(after.channel.id):
            return
        await self.create_new_session(data)

    async def _any_voice_state_update(self, data):
        member = data["member"]
        await self.create_user_if_not_in_database(member)

    async def create_new_session(self, data):
        member = data["member"]
        after = data["state"]
        try:
            session = await db.create_session_log(member, after)
            activity = await db.create_activity_log(member, after, session.id)
        except Exception as e:
            print(e)
    async def end_session(self, member):
        await db.complete_activity(member, "activitylog")
        await db.complete_activity(member, "session")  # TODO TEST
        await db.get_all("session")
        # LATER: send Message

    async def create_user_if_not_in_database(self, member):
        user = await db.get_user(member)
        if user is None:
            await db.create_user(member)


session_to_database = Session_to_database()
