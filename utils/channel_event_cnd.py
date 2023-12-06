
# from types.VC_events import VCEvent

def channel_renamed(ChannelEvent):
    if ChannelEvent.event_str != 'on_guild_channel_update':
        return False
    if ChannelEvent.before.name != ChannelEvent.after.name:
        return True
    return False


def excluding_condition_is_met(ChannelEvent):
    if ChannelEvent.event_str != 'on_guild_channel_update':
        return False
    if ChannelEvent.before.name == ChannelEvent.after.name:
        return True
    return False

# TODO


def is_task_channel_deleted(ChannelEvent):
    if ChannelEvent.event_str != 'on_guild_channel_delete':
        return False
    # leaderboard_id =
    return True

# TODO


def is_leaderboard_deleted(ChannelEvent):
    if ChannelEvent.event_str != 'on_guild_channel_delete':
        return False
    # leaderboard_id =
    return True


def is_relevant_channel(ChannelEvent):
    # TODO
    return True


def task_channel_deleted(ChannelEvent):
    return True


def voice_channel_created(ChannelEvent):
    return True


def changed_privacy_settings(ChannelEvent):
    return True
