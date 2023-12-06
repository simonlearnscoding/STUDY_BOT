from discord.ext import commands
from utils.error_handler import error_handler
from bases.event_manager_base import event_manager_baseclass
from event_handlers.channel_event_handler import channel_event_handler
from event_emitters.channel_event_emitter import channel_event_emitter
# from types import ChannelEvent


class ChannelEvent:
    def __init__(self, event_str, before=None, after=None):
        self.event_str = event_str
        self.before = before
        self.after = after


async def setup(bot):
    event_manager = event_manager_baseclass(
        channel_event_handler, channel_event_emitter(bot),
        bot=bot
    )

    await bot.add_cog(channel_events_cog(bot, event_manager))


class channel_events_cog(commands.Cog):
    def __init__(self, bot, event_manager):
        self.bot = bot
        self.event_manager = event_manager

    @commands.Cog.listener()
    @error_handler
    async def on_guild_channel_delete(self, channel):
        # TODO: fix this!
        CHEvent = ChannelEvent(
            event_str='on_guild_channel_delete', before=channel)
        await self.event_manager.handle(CHEvent)

    @commands.Cog.listener()
    @error_handler
    async def on_guild_channel_create(self, channel):
        CHEvent = ChannelEvent(
            event_str='on_guild_channel_create', after=channel)
        await self.event_manager.handle(CHEvent)

    @commands.Cog.listener()
    @error_handler
    async def on_guild_channel_update(self, before, after):
        CHEvent = ChannelEvent(
            event_str='on_guild_channel_update', before=before, after=after)
        await self.event_manager.handle(CHEvent)
