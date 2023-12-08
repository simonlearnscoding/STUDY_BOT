# import utils.channel_event_cnd as cnd
import utils.channel_event_cnd as cnd
from typing import Type, Protocol, Dict


class ChannelEventHandlerProtocol(Protocol):
    @staticmethod
    async def handle(ChannelEvent) -> str:
        pass


class VoiceChannelCreated:
    @staticmethod
    async def handle(ChannelEvent):
        if await cnd.was_channel_created_by_my_bot(ChannelEvent):
            return ('channel_created_by_me')
        # return 'voice_channel_created'


class VoiceChannelRenamed:
    # TODO: Test
    @staticmethod
    async def handle(ChannelEvent):
        if cnd.channel_renamed(ChannelEvent):
            return 'channel_renamed'
        # if cnd.excluding_condition_is_met(ChannelEvent):
        #     pass


class VoiceChannelDeleted:
    # TODO: Test
    @staticmethod
    async def handle(ChannelEvent):
        # logic for when a voice channel is renamed
        if cnd.is_leaderboard_deleted(ChannelEvent):
            return 'leaderboard_deleted'

        if cnd.is_task_channel_deleted(ChannelEvent):
            return 'task_channel_deleted'

        return 'channel_deleted'


class channel_event_handler:
    event_handlers: Dict[str, Type[ChannelEventHandlerProtocol] | None] = {
        'on_guild_channel_create': VoiceChannelCreated,
        'on_guild_channel_update': VoiceChannelRenamed,
        'on_guild_channel_delete': VoiceChannelDeleted,
        # Add other mappings
    }

    @staticmethod
    async def handle(ChannelEvent) -> str:
        handler_class: Type[ChannelEventHandlerProtocol] | None = channel_event_handler.event_handlers.get(
            ChannelEvent.event_str)

        # Ensure that a handler class is found
        if handler_class is not None:
            # Instantiate the handler class and perform the handling
            handler = handler_class()
            return await handler.handle(ChannelEvent)
        raise RuntimeError("No handler for the given ChannelEvent.")
