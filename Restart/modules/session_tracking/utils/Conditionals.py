import modules.TimeTracking.activities as act


def user_changed_type_of_tracking(before, after):
    if before.self_video != after.self_video or before.self_stream != after.self_stream:
        return True
    return False


def userLeftChannel(after):
    if after.channel is None:
        return True
    return False


def user_joins_tracking_channel(before, after):
    if userJoinedChannel(before, after):
        return True
    if comesFromNonActChannel(before, after):
        return True
    return False


def userJoinedChannel(before, after):
    # A function that returns true if the user just joined a channel

    if before.channel is not None:
        return False
    if act.getActivity(after.channel.id):
        return True
    return False


def comesFromNonActChannel(before, after):
    if before.channel is None:
        return False
    if act.getActivity(before.channel.id):
        return False
    if act.getActivity(after.channel.id):
        return True


def userChangedChannel(before, after):
    if (
        before.channel.id != after.channel.id
        and after.channel is not None
        and before.channel is not None
    ):
        return True


def is_mute_or_deafen_update(before, after):
    # Check if the user joined or left a voice channel
    if before.channel != after.channel:
        return False

    # Check if the user started or stopped streaming
    if before.self_stream != after.self_stream:
        return False

    # Check if the user started or stopped video
    if before.self_video != after.self_video:
        return False

    # Check if the user muted or unmuted themselves
    if before.self_mute != after.self_mute:
        return True

    # Check if the user deafened or undeafened themselves
    if before.self_deaf != after.self_deaf:
        return True

    return False
