from discord import VoiceState
import modules.session_tracking.activities as act
from Cogs.VC_events import VCEvent


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
    if is_mute_or_deafen_update(VCEvent):
        return True
    if VCEvent.member.bot:
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
