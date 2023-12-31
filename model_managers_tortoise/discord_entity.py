from dataclasses import dataclass
from tortoise_models import Server, User, Channel, TextChannelEnum
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from model_managers_tortoise.database_managers import database_base_class, table_manager

class server_manager(table_manager):
    def __init__(self, bot):
        super().__init__(table=Server, bot=bot, child_class=server_class)

    def get_child_entities(self):
        discord_servers = {guild for guild in self.bot.guilds}
        return discord_servers

class server_class(database_base_class):
    def __init__(self, bot, entity):
        super().__init__(bot, table=Server)
        self.entity = entity
        self.id = guild.id
        self.name = guild.name
        self.channel_manager = channel_manager(bot=self.bot, entity=self.entity)

    async def filter(self):
        return await self.table.filter(id=self.id).first()

    def get_data(self):
        return {'id': self.id, 'name': self.name}

    # async def custom_create(self, data):
    #     await self.channel_manager.sync_channels()
    #
    # async def custom_update(self):
    #     await self.channel_manager.sync_channels()




class channel_manager(table_manager):
    def __init__(self, bot, entity):
        super().__init__(table=Channel, bot=bot, child_class=channel_class)
        self.entity = entity
        self.guild = entity
        # self.leaderboard_class = bot_owned_channel_class(channel_type=TextChannelEnum.LEADERBOARD, guild=self, bot=self.bot)
        # self.task_channel_class = bot_owned_channel_class(channel_type=TextChannelEnum.TASKS, guild=self, bot=self.bot)

    async def get_child_ids(self):
        channels_id = {int(channel.id) for channel in self.guild}
        # TODO: I need to extract the leaderboard and task channel maybe?
        return channels

    async def sync_channels(self):
        # TODO: check if leaderboard channel exists - if not create it
        # TODO: check if task channel exists - if not create it
        await self.leaderboard_class.create_db_entry_if_not_exist()
        await self.task_channel_class.create_db_entry_if_not_exist()
        await self.sync_table_with_data()

class create_bot_owned_channel():
    def __init__(self, bot, channel_type, id):
        self.bot = bot
        self.guild = self.bot.get_guild(id)
        self.server_class = server_class(bot=bot, id=id)
        self.channel_type = channel_type

    async def custom_create(self):
        server_db = await self.server_class.create_if_not_exist()
        channel_name = self.channel_type.value
        channel = await self.guild.create_text_channel(channel_name)
        await self.table.create(server=self.guild.db_entry, discord_id=channel.id, channel_type=self.channel_type, name=self.channel_type)
        return channel

    async def create_if_not_exist(self):
        db_entry = await self.filter()
        if not db_entry:
            channel = await self.custom_create()
            return channel

    async def filter(self):
        """this one tests if the server already has a channel of type leaderboard or task"""
        server_db = await self.server_class.create_if_not_exist()
        channel_entry = await self.table.filter(server=server_db, channel_type=self.channel_type).first()
        if channel_entry:
            discord_channel = self.guild.get_channel(int(channel_entry.discord_id))
            if discord_channel:
                return discord_channel
            else:
                await channel_entry.delete()
        return None

class channel_methods(ABC):
    def __init__(self, bot, guild, channel_type=None):
        self.bot = bot
        self.channel_type = channel_type

    def get_data(self):
        self.entity = self.fetch_entity()
        return {'discord_id': self.channel.id, 'channel_type': self.channel_type, 'server': self.server_db, 'name': self.channel.name}

    def fetch_entity(self):
        return self.bot.get_channel(self.id)

    async def delete_channel(self, channel):
        server = await Server.get_or_none(id=self.id)
        channel_db = await Channel.get_or_none(discord_id=channel.id, server=server)
        if channel_db:
            await channel_db.delete()

class channel_class(database_base_class, channel_methods):
    def __init__(self, bot, id):
        database_base_class.__init__(self=self, table=Channel, bot=bot)
        channel_methods.__init__(self, bot, id)

    async def filter(self):
        return await self.table.filter(discord_id=self.id, server=self.guild_db).first()






class user_manager(table_manager):
    def __init__(self, bot):
        super().__init__(table=User, bot=bot, child_class=user_class)
        
class user_class(database_base_class):
    def __init__(self, bot, id):
        super().__init__(User, bot, id, )

    def fetch_entity(self):
        return self.bot.get_member(self.id)

    def get_data(self):
        self.entity = self.fetch_entity()
        return {'discord_id': self.channel.id, 'display_name': self.channel.name}

