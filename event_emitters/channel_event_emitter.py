
from tortoise_models import Channel, TextChannelEnum
from utils.error_handler import class_error_handler
# from model_managers_tortoise.server_manager import server_class
from model_managers_tortoise.server_instance import server
from model_managers_tortoise.channel_db_manager import channel_class, bot_owned_channel_creator

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
        channel_man = bot_owned_channel_creator(self.bot, channel_event.before.guild)
        await channel_man.create_if_not_exist(channel_type=TextChannelEnum.LEADERBOARD)

    async def tasks_channel_deleted(self, channel_event):
        channel_man = bot_owned_channel_creator(self.bot, channel_event.before.guild)
        await channel_man.create_if_not_exist(channel_type=TextChannelEnum.TASKS)

    async def voice_channel_deleted(self, channel_event):
        await self.wrapper.handle_channel_deleted(channel_event)

    async def category_channel_deleted(self, channel_event):
        await self.wrapper.handle_channel_deleted(channel_event)

    async def text_channel_deleted(self, channel_event):
        await self.wrapper.handle_channel_deleted(channel_event)

    async def channel_renamed(self, channel_event):
        await self.wrapper.handle_channel_renamed(channel_event)


class wrapper_functions():
    def __init__(self, bot):
        self.bot = bot

    async def handle_channel_renamed(self, channel_event):
        entity = channel_event.after
        channel = channel_class(self.bot, entity)
        await channel.create_or_update()

    async def handle_channel_created(self, channel_event):
        # TODO: Test
        entity = channel_event.after
        channel = channel_class(self.bot, entity)
        await channel.get_or_create()

    # TODO: you are here
    async def handle_channel_deleted(self, channel_event):
        # TODO: Test
        entity = channel_event.before
        channel = channel_class(self.bot, entity)
        await channel.delete_channel()

