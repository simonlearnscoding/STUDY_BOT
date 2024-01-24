from enum import Enum
# from dataclasses import dataclass
from discord import Member, VoiceState
from event_emitters.base_event_manager_21_01 import EventEmitter
from model_managers_tortoise.database_managers import *
from model_managers_tortoise.table_manager import SetterMixin
from tortoise_models import *


def calculate_time_difference(joined_at):
    tz = pytz.timezone('Etc/GMT-2')
    now = datetime.now(tz)
    duration_in_seconds = int(round((now - joined_at).total_seconds())) + 3600
    return duration_in_seconds


class VCEvent(SetterMixin, EventEmitter):

    def __init__(self, bot, member: Member, before: VoiceState, after: VoiceState,
                 ):
        EventEmitter.__init__(self, bot)
        self.member = member
        self.guild = member.guild
        self.before = before
        self.bot = bot
        self.after = after
        self.activity_before = None
        self.activity_after = None
        self.activity_before = None
        self.activity_type_after = None
        self.activity_type_before = None

    async def excluding_condition_met(self):
        print("excluding condition met")

    async def disconnect_member_from_voice(self, member_id):
        disconnect_status = {}

        for guild in self.bot.guilds:
            member = guild.get_member(member_id)
            if member and member.voice:
                try:
                    await member.move_to(None)
                    disconnect_status[guild.name] = "Disconnected"
                except Exception as e:
                    disconnect_status[guild.name] = f"Failed to disconnect: {e}"

        return disconnect_status

    async def get_member_voice_states(self, member_id):
        voice_states = []

        for guild in self.bot.guilds:
            member = guild.get_member(member_id)
            if member and member.voice:
                voice_states.append(member.voice)
                voice_states.append(member)
        return voice_states

    async def user_changed_recording_type(self):
        print("user changed recording type")
        session_partial = await SessionPartial.filter(user=self.user_db).first()
        session = await session_partial.session
        session_data = await SessionData.filter(session=session, activity_record_type=self.activity_type_before).first()
        await self.end_session_partial(session_partial, session, session_data)
        await self.create_session_partial(session, self.activity_type_after)

    async def user_left_activity(self):
        await self.end_session()
        await self.disconnect_member_from_voice(self.member.id)
        # RESTART A Session if Im still somewhere.
        # voice_states = await self.get_member_voice_states(self.member.id)
        # if len(voice_states) > 0:
        # print('hi')
        # await self.recursively_start_another_session(voice_states)

    async def recursively_start_another_session(self, voice_states):
        # TODO: fix this
        old_vs = voice_states[0]
        member = voice_states[1]
        old_vs.channel = None
        vc_event = VCEvent(self.bot, member, old_vs, voice_states[1])
        await vc_event.get_event_db_entries()
        from event_emitters.vc_event_manager import VCEventConditionState
        vc_event_manager = VCEventConditionState(bot=self.bot, event=vc_event)
        await vc_event_manager.evaluate_all()

    async def end_session(self):
        print("ending a session")
        session_partial = await SessionPartial.filter(user=self.user_db).first()
        session = await session_partial.session
        session_data = await SessionData.filter(session=session, activity_record_type=self.activity_type_before).first()
        await self.end_session_partial(session_partial, session, session_data)
        session.left_at = datetime.now()
        session.is_active = False
        all_session_data = await SessionData.filter(session=session)
        for session_data in all_session_data:
            print(f'user was {session_data.duration_in_seconds} seconds in {session_data.activity_record_type}')
        await session.save()

    async def end_session_partial(self, session_partial, session, session_data):
        duration_in_seconds = calculate_time_difference(session_partial.joined_at)
        session_data.duration_in_seconds += duration_in_seconds
        session.duration_in_seconds += duration_in_seconds
        session_data.partials_amount += 1
        await session_data.save()
        await session.save()
        await session_partial.delete()

    async def create_session_partial(self, session, activity_type):
        session_partial = await SessionPartial.create(user=self.user_db, server=self.server_db, session=session, activity_record_type=activity_type)
        await session_partial.save()
        session_data = await SessionData.filter(session=session, activity_record_type=activity_type).first()
        if not session_data:
            session_data = await SessionData.create(session=session, activity_record_type=activity_type)
        await session_data.save()

    async def user_changed_activity(self):
        await self.end_session()
        await self.create_session(self.activity_after, self.activity_type_after)

    async def user_rejoins_activity(self):
        print("user_rejoins_activity")
        session = await Session.filter(user=self.user_db, activity=self.activity_after).order_by('-left_at').first()
        session.is_active = True
        session.left_at = None
        await session.save()
        session_data = await SessionData.filter(session=session, activity_record_type=self.activity_type_after).first()
        if not session_data:
            session_data = await SessionData.create(session=session, activity_record_type=self.activity_type_after).first()
        await self.create_session_partial(session, self.activity_type_after)

    async def user_joined_activity(self):
        await self.create_session(self.activity_after, self.activity_type_after)

    async def create_session(self, activity, activity_type):
        print("create_session")
        session = await Session.create(user=self.user_db, server=self.server_db, activity=activity)
        await session.save()
        await self.create_session_partial(session, activity_type)

    async def get_event_db_entries(self):
        await self.set_attribute('server_db', 'model_managers_tortoise.server_instance', 'server', self.guild)
        await self.set_attribute('user_db', 'model_managers_tortoise.user', 'user_class', self.member)

        self.activity_type_before = self.determine_activity_type(self.before)
        self.activity_type_after = self.determine_activity_type(self.after)
        self.channel_before, self.activity_before = await self.fetch_channel_and_activity(attribute_name='channel_before', voice_state=self.before)
        self.channel_after, self.activity_after = await self.fetch_channel_and_activity(attribute_name='channel_after', voice_state=self.after)

    async def fetch_channel_and_activity(self, attribute_name, voice_state):
        if voice_state.channel is not None:
            channel = await self.set_attribute(attribute_name, 'model_managers_tortoise.channel_db_manager', 'channel_class', voice_state.channel)
            if channel:
                activity = await channel.activity.first() if channel.activity else None
                return channel, activity
            else:
                return None, None
        return None, None

    def determine_activity_type(self, voicestate):
        if voicestate.channel is None:
            return "NONE"
        if voicestate.self_stream and voicestate.self_video:
            return "BOTH"
        if not voicestate.self_stream and not voicestate.self_video:
            return "VC"
        if voicestate.self_stream:
            return "SS"
        if voicestate.self_video:
            return "CAM"


class ChannelEvent:
    def __init__(self, event_str, before=None, after=None):
        self.event_str = event_str
        self.before = before
        self.after = after
