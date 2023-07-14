

# class session_tracking(commands.Cog):
#     def __init__(self, bot):
#         super().__init__()
#         self.bot = bot
#
#     # ON A VOICESTATE EVENT
#     @commands.Cog.listener()
#     async def on_voice_state_update(self, member, before, after):
#         # await timelogs.makeMemberIfNotExists(member)
#         if self.excluding_condition_is_met(before, after, member):
#             return
#         await self.create_user_if_not_in_database(member)
#
#         if cnd.user_joins_tracking_channel(before, after):
#             print(f"{member.name} joined channel")
#             await self.create_new_session(member, after)
#             await Leaderboard_Manager.create(key=member)
#             return
#
#         if cnd.user_changed_type_of_tracking(before, after):
#             print(f"{member.name} changed activity type")
#             await db.complete_activity(member, "activitylog")
#             session = await db.get_ongoing_session(member)
#             await db.create_activity_log(member, after, session.id)
#             print(e)
#             # return
#
#         if cnd.userLeftChannel(after):
#             # LATER: make the message function
#             print("user left")
#             await self.end_session(member)
#             await Leaderboard_Manager.destroy(member)
#             # return
#
#         if cnd.userChangedChannel(before, after):
#             # LATER: make the message function
#             print("user changed channel")
#             await self.end_session(member)
#             await db.get_all("session")
#             if not act.getActivity( after.channel.id ):
#                 return
#             await self.create_new_session(member, after)
#
#     async def create_new_session(self, member, after):
#         session = await db.create_session_log(member, after)
#         activity = await db.create_activity_log(member, after, session.id)
#         print(f"created a new session for {member.name}")
#
#     async def end_session(self, member):
#         await db.complete_activity(member, "activitylog")
#         await db.complete_activity(member, "session")  # TODO TEST
#         print(f"ended a session for {member.name}")
#         await db.get_all("session")
#         # LATER: send Message
#
#     def excluding_condition_is_met(self, before, after, member):
#         # EXCLUDING CONDITIONS
#
#         if cnd.is_mute_or_deafen_update(before, after):
#             return True
#         if member.bot:
#             return True
#         return False
#
#     async def create_user_if_not_in_database(self, member):
#         user = await db.get_user(member)
#         if user is None:
#             await db.create_user(member)
#
