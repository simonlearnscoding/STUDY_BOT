
from tortoise_models import Channel, TextChannelEnum
from utils.error_handler import class_error_handler
# from model_managers_tortoise.server_manager import server_class

from event_emitters.base_event_emitter import base_event_emitter
"""
ALL OF THE THINGS THAT HAPPEN AS A RESULT OF CHANNEL EVENTS WILL HAPPEN HERE!
"""

# @class_error_handler


class channel_event_emitter(base_event_emitter):
    def __init__(self, bot):
        super().__init__(bot)
        self.wrapper = wrapper_functions(bot)

    async def channel_created_by_me(self, channel):
        print('channel created by my bot')
        pass

    async def text_channel_created(self, channel_event):
        await self.wrapper.handle_channel_created(channel_event)

    async def voice_channel_created(self, channel_event):
        await self.wrapper.handle_channel_created(channel_event)

    async def category_channel_created(self, channel_event):
        await self.wrapper.handle_channel_created(channel_event)

    async def leaderboard_channel_deleted(self, channel_event):
        await self.wrapper.handle_delete_bot_channel(channel_event, TextChannelEnum.LEADERBOARD)

    async def tasks_channel_deleted(self, channel_event):
        await self.wrapper.handle_delete_bot_channel(channel_event, TextChannelEnum.TASKS)

    async def voice_channel_deleted(self, channel_event):
        await self.wrapper.handle_channel_deleted(channel_event)

    async def category_channel_deleted(self, channel_event):
        await self.wrapper.handle_channel_deleted(channel_event)

    async def text_channel_deleted(self, channel_event):
        await self.wrapper.handle_channel_deleted(channel_event)

    async def channel_renamed(self, channel_event):
        server = server_class(self.bot, channel_event.after.guild.id)
        await server.rename_channel(channel_event.after)
        pass


class wrapper_functions():
    def __init__(self, bot):
        self.bot = bot

    async def handle_delete_bot_channel(self, channel_event, channel_type):
        server = await self.handle_channel_deleted(channel_event)
        await server.create_or_return_channel(channel_type)

    async def handle_channel_created(self, channel_event):
        server = server_class(self.bot, channel_event.after.guild.id)
        await server.get_or_create_channel(channel_event.after)
        return server

    async def handle_channel_deleted(self, channel_event):
        server = server_class(self.bot, channel_event.before.guild.id)
        await server.delete_channel(channel_event.before)
        return server
