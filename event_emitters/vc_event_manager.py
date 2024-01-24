from abc import ABC, abstractmethod
from event_emitters.base_event_manager_21_01 import EventEmitter, EventManager, EventConditionNode
from tortoise_models import Session, SessionPartial
import datetime
from model_managers_tortoise.vc_events import calculate_time_difference


class user_joined_activity(EventConditionNode):
    async def handle(self):
        if await self.evaluate_condition('user_has_active_session'):
            return False
        if not await self.evaluate_condition('from_untracked_to_tracked'):
            return False
        if not await self.evaluate_condition('user_last_session_less_than_15_minutes'):
            return True
        return False


class user_rejoins_activity(EventConditionNode):
    async def handle(self):
        if await self.evaluate_condition('user_has_active_session'):
            return False
        if not await self.evaluate_condition('from_untracked_to_tracked'):
            return False
        if await self.evaluate_condition('user_has_active_session'):
            return False
        if await self.evaluate_condition('user_last_session_less_than_15_minutes'):
            return True
        return False


class event_is_from_another_server(EventConditionNode):
    async def handle(self):
        if not await self.evaluate_condition('user_has_active_session'):
            return False
        session_partial = await SessionPartial.filter(user=self.event.user_db).first()
        session = await session_partial.session
        server_old = await session.server

        if self.event.server_db != server_old:
            return True
        return False


class user_has_active_session(EventConditionNode):
    async def handle(self):
        session = await Session.filter(user=self.event.user_db, is_active=True).first()
        if session:
            return True
        return False


class user_last_session_less_than_15_minutes(EventConditionNode):
    # Check if last session was less than 15 minutes ago
    async def get_last_session(self):
        return await Session.filter(user=self.event.user_db, server=self.event.server_db ).order_by('-left_at').first()

    async def handle(self):
        session = await self.get_last_session()
        if not session:
            return False
        activity = await session.activity
        new_activity = self.event.activity_after
        if activity != new_activity:
            return False
        if session and session.left_at:
            time_passed = calculate_time_difference(session.left_at)
            return time_passed < 100 # TODO: replace with 15 minutes
        return False


class user_left_activity(EventConditionNode):
    async def handle(self):
        if not await self.evaluate_condition('user_has_active_session'):
            return False
        if self.event.activity_before is None:
            return False
        if self.event.activity_after is None:
            return True
        return False


class user_changed_activity(EventConditionNode):
    async def handle(self):

        if not await self.evaluate_condition('user_has_active_session'):
            return False
        if self.event.activity_before is None or self.event.activity_after is None:
            return False
        if self.event.activity_before != self.event.activity_after:
            return True
        return False


class is_mute_or_deafen_update(EventConditionNode):
    async def handle(self):
        # Check if the user joined or left a voice channel
        if self.event.before.channel != self.event.after.channel:
            return False

        # Check if the user started or stopped streaming
        if self.event.before.self_stream != self.event.after.self_stream:
            return False

        # Check if the user started or stopped video
        if self.event.before.self_video != self.event.after.self_video:
            return False

        # Check if the user muted or unmuted themselves
        if self.event.before.self_mute != self.event.after.self_mute:
            return True

        # Check if the user deafened or undeafened themselves
        if self.event.before.self_deaf != self.event.after.self_deaf:
            return True

        if self.event.before.deaf != self.event.after.deaf:
            return True

        if self.event.before.mute != self.event.after.mute:
            return True
        return False


class from_untracked_to_tracked(EventConditionNode):
    async def handle(self):
        if self.event.activity_after is not None and self.event.activity_before is None:
            return True
        return False


class excluding_condition_met(EventConditionNode):
    async def handle(self):
        if self.event.member.bot:
            return True
        if await self.evaluate_condition('event_is_from_another_server'):
            return True
        if await self.evaluate_condition('is_mute_or_deafen_update'):
            return True
        if self.event.activity_before is None and self.event.activity_after is None:
            return True

        return False


class user_changed_activity_recording_type(EventConditionNode):
    async def handle(self):
        if (self.event.activity_before or self.event.activity_after) is None:
            return False
        if self.event.activity_type_before != self.event.activity_type_after:
            return True
        return False


class user_has_active_session(EventConditionNode):
    async def handle(self):
        session = await Session.filter(user=self.event.user_db, is_active=True).first()
        if session:
            return True
        return False


class user_changed_recording_type(EventConditionNode):
    async def handle(self):
        if not await self.evaluate_condition('user_has_active_session'):
            return False
        if self.event.activity_before is None or self.event.activity_after is None:
            return False
        if await self.evaluate_condition('user_changed_activity_recording_type'):
            return True
        return False


class VCEventEmitter(EventEmitter):
    async def user_joined_activity(self):
        pass


class VCEventConditionState(EventManager):
    conditionals = [
        # is_user_in_activity,
        user_joined_activity,
        user_changed_activity,
        user_left_activity,
        excluding_condition_met,
        event_is_from_another_server,
        user_rejoins_activity,
        user_changed_recording_type,
        user_changed_activity_recording_type,
        from_untracked_to_tracked,
        user_has_active_session,
        user_last_session_less_than_15_minutes,
        is_mute_or_deafen_update
    ]
    conditions_with_actions = [
        "excluding_condition_met",
        "user_changed_recording_type",
        "user_left_activity",
        "user_changed_activity",
        "user_rejoins_activity",
        "user_joined_activity",
    ]

    def __init__(self,
                 event,
                 bot,
                 ):
        super().__init__(
            bot=bot,
            event=event,
            conditionals=self.conditionals,  # type: ignore
            conditions_with_actions=self.conditions_with_actions,
        )
        # an event condition state gets instantiated by the cog


# an event condition state gets instantiated by the cog
