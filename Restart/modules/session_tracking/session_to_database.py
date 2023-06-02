from modules.session_tracking.database_queries import queriess as db
from bases.event_manager import event_manager
from modules.session_tracking.activities import getActivity
class session_to_database():
    def __init__(self, event_manager=event_manager):
        self.event = event_manager
        self.event.subscribe(self)
        pass
    async def _user_changed_type_of_tracking(self, data):
        await self.changed_type_of_tracking(data)
    async def _user_joins_tracking_channel(self, data):
        await self.create_new_session(data)
    async def _user_left_tracking_channel(self, data):
        member = data['member']
        await self.end_session(member)
    async def changed_type_of_tracking(self, data):
        member = data["member"]
        state = data["state"]
        await db.complete_activity(member, "activitylog")
        session = await db.get_ongoing_session(member)
        await db.create_activity_log(member, state, session.id)
    async def _user_changed_tracking_channel(self, data):
        member = data['member']
        after = data['state']

        await self.end_session(member)
        await db.get_all("session")
        if not getActivity( after.channel.id ):
            return
        await self.create_new_session(data)

    #TODO: listen to
    async def _any_voice_state_update(self, data):
        member = data['member']
        await self.create_user_if_not_in_database(member)
    async def create_new_session(self, data):
        member = data["member"]
        after = data["state"]
        session = await db.create_session_log(member, after)
        activity = await db.create_activity_log(member, after, session.id)


    async def end_session(self, member):
        await db.complete_activity(member, "activitylog")
        await db.complete_activity(member, "session")  # TODO TEST
        await db.get_all("session")
        # LATER: send Message




    async def create_user_if_not_in_database(self, member):
        user = await db.get_user(member)
        if user is None:
            await db.create_user(member)

session_to_database = session_to_database()