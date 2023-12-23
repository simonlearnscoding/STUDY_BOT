from dataclasses import dataclass
from tortoise_models import Server, User, Channel
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from model_managers_tortoise.database_managers import database_base_class, table_manager


class server_class(database_base_class):
    def __init__(self, bot, id):
        super().__init__(Server, bot, id)

    def fetch_entity(self):
        return self.bot.get_guild(self.id)

    def get_data(self):
        return {'id': self.id, 'name': self.entity.name}

    async def custom_create(self, data):
        await super().get_or_create(data=data)
        await self.sync()


class user_class(database_base_class):
    def __init__(self, bot, id):
        super().__init__(User, bot, id, filter_key="discord_id")

    def fetch_entity(self):
        return self.bot.get_member(self.id)

    async def get_data(self):
        return {'discord_id': self.channel.id, 'display_name': self.channel.name}


class channel_methods(ABC):
    def __init__(self, bot):
        self.bot = bot
        self.guild_class = server_class

    @abstractmethod
    def get_data(self):
        return {'discord_id': self.channel.id, 'name': self.channel.name}

    @abstractmethod
    def fetch_entity(self):
        return self.bot.get_channel(self.id)


class channel_class(database_base_class):
    def __init__(self, bot, entity, server_id):
        database_base_class.__init__(Channel, bot, entity)
        channel_methods.__init__(self)
        self.channel_type = None


class bot_owned_channel_class(database_base_class):
    def __init__(self, bot, entity, channel_type):
        database_base_class.__init__(Channel, bot, entity)
        channel_methods.__init__(self)
        self.guild_class = server_class
        self.channel_type = channel_type

    async def custom_create(self):
        await self.create_channel_on_discord(channel_type)
        await super().get_or_create()

    async def create_channel_on_discord(self):
        guild = await self.get_guild()
        channel_name = channel_type.value
        channel = await guild.create_text_channel(self.channel_name)
        await self.get_or_create_channel(channel, channel_type)
        return channel


class server_manager(table_manager):
    def __init__(self, bot):
        super().__init__(table=Server, bot=bot, child_class=server_class)

    def get_child_data(self):
        discord_servers = {int(guild.id) for guild in self.bot.guilds}
        return discord_servers


class channel_manager(table_manager):
    def __init__(self, bot):
        super().__init__(table=Channel, bot=bot, child_class=channel_class)

    async def get_child_data(self):
        channels_id = {channel.id for guild in self.bot.guilds}
        channels = await self.get_entities_by_id(channels_id)
        return channels


class user_manager(table_manager):
    def __init__(self, bot):
        super().__init__(table=User, bot=bot, child_class=user_class)
