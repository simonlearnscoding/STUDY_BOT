from discord import VoiceState
from tortoise_models import Server, User, Channel, TextChannelEnum
import modules.session_tracking.activities as act
from model_managers_tortoise.vc_events import VCEvent

from abc import ABC, abstractmethod


class EmitEventNode(ABC):
    def __init__(self, bot=None, event=None):
        self.bot = bot
        self.event = event

    @abstractmethod
    async def handle_case(self):
        pass


class EmitUserChangedActivityRecordType(EmitEventNode):
    async def handle_case(self):
        pass


class HandleTreeNode(ABC):
    validated_conditions = {}  # Shared across all instances

    def __init__(self, bot=None, event=None, handle_if=None, handle_else=None):
        self.bot = bot
        self.event = event
        self.handle_if = handle_if
        self.handle_else = handle_else

    @abstractmethod
    async def handle(self):
        pass

    async def get_or_validate(self, condition_name):
        if condition_name in HandleTreeNode.validated_conditions:
            return HandleTreeNode.validated_conditions[condition_name]
        
        result = await self.handle()
        HandleTreeNode.validated_conditions[condition_name] = result
        return result

    async def handle_case(self):
        condition_result = await self.get_or_validate(self.__class__.__name__)
        if condition_result:
            if self.handle_if:
                await self.handle_if.set_context(self.bot, self.event)
                await self.handle_if.handle_case()
        else:
            if self.handle_else:
                await self.handle_else.set_context(self.bot, self.event)
                await self.handle_else.handle_case()

    def set_context(self, bot, event):
        self.bot = bot
        self.event = event


class did_user_change_activity_record_type(HandleTreeNode):
    async def handle(self, event):
        return self.did_user_change_activity_record_type_met()

    def did_user_change_activity_record_type_met(self):
        pass


class is_user_after_activity_none(HandleTreeNode):
    async def handle(self, event):
        return self.is_user_after_activity_none_met()

    def is_user_after_activity_none_met(self):
        pass


class is_user_after_activity_same_as_user_current_activity(HandleTreeNode):
    async def handle(self, event):
        return self.is_user_after_activity_same_as_user_current_activity_met()

    def is_user_after_activity_same_as_user_current_activity_met(self):
        pass


class is_after_channel_activity(HandleTreeNode):
    async def handle(self, event):
        return self.is_after_channel_activity_met()

    def is_after_channel_activity_met(self):
        pass


class is_user_activity_same_server_as_event(HandleTreeNode):
    async def handle(self, event):
        return self.is_user_activity_same_server_as_event_met()

    def is_user_activity_same_server_as_event_met(self):
        pass


class has_user_active_session(HandleTreeNode):
    async def handle(self, event):
        return self.has_user_active_session_met()

    def has_user_active_session_met(self):
        pass


class is_ignore_case_met(HandleTreeNode):
    async def handle(self, event):
        return self.is_ignore_case_met()

    def is_ignore_case_met(self):
        pass


def user_changed_type_of_tracking(VCEvent):
    if act.getActivity(VCEvent.before) != act.getActivity(VCEvent.after):
        return False
    if act.getActivityType(VCEvent.before) != act.getActivityType(VCEvent.after):
        return True


def user_left_channel(VCEvent: VCEvent):
    if VCEvent.after.channel is None:
        return True
    if not is_tracked_channel(VCEvent.after):
        return True
    return False


def user_joins_tracking_channel(VCEvent: VCEvent):
    if user_joined_channel(VCEvent):
        return True
    if user_comes_from_untracked_channel(VCEvent):
        return True
    return False


def user_joined_channel(VCEvent: VCEvent):
    # A function that returns true if the user just joined a channel

    if VCEvent.before.channel is not None:
        return False
    if act.getActivity(VCEvent.after):
        return True
    return False


def user_comes_from_untracked_channel(VCEvent: VCEvent):
    if is_tracked_channel(VCEvent.before):
        return False
    if is_tracked_channel(VCEvent.after):
        return True
    return False


def is_tracked_channel(voicestate: VoiceState):
    if voicestate.channel is None:
        return False
    if act.getActivity(voicestate):
        return True
    return False


def from_no_channel_to_untracked_channel(VCEvent: VCEvent):
    if VCEvent.before.channel:
        return False
    if not is_tracked_channel(VCEvent.after):
        return True


def from_untracked_to_untracked(VCEvent: VCEvent):
    if is_tracked_channel(VCEvent.after):
        return False
    if is_tracked_channel(VCEvent.before):
        return False
    return True


def excluding_condition_is_met(VCEvent):
    if VCEvent.member.bot:
        return True
    if is_mute_or_deafen_update(VCEvent):
        return True
    if from_untracked_to_untracked(VCEvent):
        return True
    if VCEvent.before:
        return False
    pass


def user_changed_channel(VCEvent):
    if (
        act.getActivity(VCEvent.before) != act.getActivity(VCEvent.after)
        and is_tracked_channel(VCEvent.after)
        and is_tracked_channel(VCEvent.before)
    ):
        return True


def is_mute_or_deafen_update(VCEvent):
    # Check if the user joined or left a voice channel
    if VCEvent.before.channel != VCEvent.after.channel:
        return False

    # Check if the user started or stopped streaming
    if VCEvent.before.self_stream != VCEvent.after.self_stream:
        return False

    # Check if the user started or stopped video
    if VCEvent.before.self_video != VCEvent.after.self_video:
        return False

    # Check if the user muted or unmuted themselves
    if VCEvent.before.self_mute != VCEvent.after.self_mute:
        return True

    # Check if the user deafened or undeafened themselves
    if VCEvent.before.self_deaf != VCEvent.after.self_deaf:
        return True

    return False
