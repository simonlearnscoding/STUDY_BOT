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
        channel_type = await cnd.get_channel_type_from_discord(ChannelEvent.after)
        string = f'{channel_type}_channel_created'
        return string

class VoiceChannelDeleted:
    # TODO: Test
    @staticmethod
    async def handle(ChannelEvent):
        # logic for when a voice channel is renamed
        channel_type = await cnd.get_channel_type_from_db(ChannelEvent.before)
        string = f'{channel_type}_channel_deleted'
        return string

class VoiceChannelRenamed:
    @staticmethod
    async def handle(ChannelEvent):
        if cnd.channel_renamed(ChannelEvent):
        # TODO: Test if the handler points to the correct emitter
            return 'channel_renamed'
        # if cnd.excluding_condition_is_met(ChannelEvent):
        # TODO: Test this
        return 'pass_event'
        #     pass




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
