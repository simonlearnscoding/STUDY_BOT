from modules.session_tracking.database_queries import queries as db
from bases.event_manager import event_manager

event_manager = event_manager


class session_to_database():
    async def create_new_session(self, data):
        member = data["member"]
        after = data["state"]
        session = await db.create_session_log(member, after)
        activity = await db.create_activity_log(member, after, session.id)
        print(f"created a new session for {member.name}")

    async def end_session(self, member):
        await db.complete_activity(member, "activitylog")
        await db.complete_activity(member, "session")  # TODO TEST
        print(f"ended a session for {member.name}")
        await db.get_all("session")
        # LATER: send Message

    #TODO: listen to
    # user_joins_tracking_channel =>
    #    await self.create_new_session(data)

    #TODO: listen to
    async def user_changed_type_of_tracking(self, member, state):
      await db.complete_activity(member, "activitylog")
      session = await db.get_ongoing_session(member)
      await db.create_activity_log(member, state, session.id)


    #TODO: listen to
    # user_changed_tracking_channel =>
    #   await self.end_session(member)

    #TODO: listen to
    # any_voice_state_update =>
    #   await self.create_user_if_not_in_database(member)
    async def create_user_if_not_in_database(self, member):
        user = await db.get_user(member)
        if user is None:
            await db.create_user(member)
