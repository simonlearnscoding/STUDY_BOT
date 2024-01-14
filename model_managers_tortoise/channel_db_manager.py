from dataclasses import dataclass
from model_managers_tortoise.database_managers import *
from tortoise_models import Server, User, Channel, TextChannelEnum
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from model_managers_tortoise.database_managers import database_base_class
from model_managers_tortoise.table_manager import *

class GetChannelEntitiesStrategy(GetChildEntitiesStrategy):
    def get_child_entities(self):
        # TODO: I need to extract the leaderboard and task channel maybe?

        array = []
        for child in self.children_instances:
            array.append(child.entity.id)
        channel_ids_to_remove = array
        channels = {
            channel
            for channel in self.entity.channels
            if channel.id not in channel_ids_to_remove
        }
        return channels


class ServerSetterMixin:
    async def set_server(self):
        if hasattr(self, "server") and hasattr(self, "server_db"):
            return
        from model_managers_tortoise.server_instance import server

        
        self.server = server(bot=self.bot, entity=self.guild)
        self.server_db, created = await self.server.create_or_nothing()

        

class channel_manager(table_manager, ServerSetterMixin):
    def __init__(self, bot, entity):
        super().__init__(
            table=Channel,
            bot=bot,
            child_entities_strategy=GetChannelEntitiesStrategy,
            child_class=channel_class,
        )
        self.entity = entity
        self.guild = entity
        self.bot_owned_channel_creator = bot_owned_channel_creator(
            bot=self.bot, entity=self.guild
        )

    async def get_all_db_entries(self):
        await self.set_server()
        entries = await self.table.filter(server=self.server_db)
        return entries

    async def sync_channels(self):
        await self.create_bot_owned_instances()
        await self.sync_table_with_data()

    async def create_bot_owned_instances(self):
        leaderboard_channel = await self.bot_owned_channel_creator.create_if_not_exist(
            channel_type=TextChannelEnum.LEADERBOARD
        )
        task_channel = await self.bot_owned_channel_creator.create_if_not_exist(
            channel_type=TextChannelEnum.TASKS
        )
        self.children_instances.append(
            channel_class(
                bot=self.bot,
                entity=leaderboard_channel,
                channel_type=TextChannelEnum.LEADERBOARD,
            )
        )
        self.children_instances.append(
            channel_class(
                bot=self.bot, entity=task_channel, channel_type=TextChannelEnum.TASKS
            )
        )


class bot_owned_channel_creator(ServerSetterMixin):
    def __init__(self, bot, entity):
        self.bot = bot
        self.table = Channel
        self.guild = entity

    async def create_if_not_exist(self, channel_type):
        self.channel_type = channel_type
        textChannel = await self._filter()
        if not textChannel:
            textChannel = await self._custom_create()
        return textChannel

    async def _custom_create(self):
        await self.set_server()
        channel_name = self.channel_type.value
        channel = await self.guild.create_text_channel(channel_name)
        self.channel = channel
        await self.table.create(
            server=self.server_db,
            discord_id=channel.id,
            channel_type=self.channel_type.value,
            name=self.channel_type.value,
        )
        # await self.table.create(server=self.server_db, discord_id=channel.id)
        return channel

    async def _filter(self):
        """this one tests if the server already has a channel of type leaderboard or task"""
        await self.set_server()
        channel_entry = await self.table.filter(
            server=self.server_db, channel_type=self.channel_type.value
        ).first()
        if channel_entry:
            discord_channel = self.guild.get_channel(int(channel_entry.discord_id))
            if discord_channel:
                return discord_channel
            else:
                await channel_entry.delete()
        return None


class ChannelFilterStrategy(FilterStrategy):
    async def filter(self):
        await self.set_server()
        # get the server from the database
        entry = await self.table.filter(discord_id=str(self.entity.id), server=self.server_db).first()
        return entry

    @staticmethod
    def get_guild_channel_array(self):
        array = []
        for channel in self.bot.guilds[2].channels:
            array.append(channel.id)
        return array


class ChannelGetDataStrategy(GetDataStrategy):
    async def get_data(self):
        await self.set_server()
        if not self.channel_type:
            self.channel_type = self.entity.type.name.capitalize()
        return {
            "discord_id": self.entity.id,
            "channel_type": self.channel_type,
            "server": self.server_db,
            "name": self.entity.name,
        }


class ChannelCreateStrategy(CreateStrategy):
    async def create(self):
        pass


class ChannelUpdateStrategy(UpdateStrategy):
    async def update(self):
        await UpdateStrategy.update_name_if_changed(self)


class channel_class(database_base_class, ServerSetterMixin):
    def __init__(
        self,
        bot,
        entity,
        channel_type=None,
    ):
        self.channel_type = channel_type
        database_base_class.__init__(
            self,
            entity=entity,
            bot=bot,
            table=Channel,
            filter_strategy=ChannelFilterStrategy,
            get_data_strategy=ChannelGetDataStrategy,
            create_strategy=ChannelCreateStrategy,
            update_strategy=ChannelUpdateStrategy
        )
        self.guild = entity.guild

    async def delete_channel(self ):
        await self.set_server()
        channel_db = await Channel.get_or_none(
            discord_id=str(self.id), server=self.server_db)

        if channel_db:
            print(f'deleting {self.entity.name}')
            await channel_db.delete()


class user_manager(table_manager):
    def __init__(self, bot):
        super().__init__(table=User, bot=bot, child_class=user_class)


class user_class(database_base_class):
    def __init__(self, bot, id):
        super().__init__(
            User,
            bot,
            id,
        )

    def fetch_entity(self):
        return self.bot.get_member(self.id)

    async def get_data(self):
        self.entity = self.fetch_entity()
        return {"discord_id": self.entity.id, "display_name": self.entity.name}
