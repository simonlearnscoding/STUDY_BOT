import discord

class Conditionals:
    def userChangedActivityType(self, before, after):
        if (
            before.self_video != after.self_video
            or before.self_stream != after.self_stream
        ):
            return True
        return False

    def userLeftChannel(self, after):
        # TODO: TEST
        if after.channel is None:
            return True
        return False

    def userJoinedChannel(self, before, after):
        # A function that returns true if the user just joined a channel
        if before.channel is None and after.channel is not None:
            # TODO: Test
            return True

    def userChangedChannel(self, before, after):
        if (
            before.channel.id != after.channel.id
            and after.channel is not None
            and before.channel is not None
        ):
            return True

    def is_mute_or_deafen_update(self, before, after):
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
