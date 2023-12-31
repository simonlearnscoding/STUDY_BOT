
from tortoise_models import Pillar, Role
from dataclasses import dataclass
from typing import Optional, Callable, Any
from bases.update_table import UpdateContext, update_table
from tortoise_models import User, UserServer, Pillar


from enum import Enum
from tortoise.transactions import in_transaction
from tortoise_models import Server, User, Channel, TextChannelEnum
from setup.bot_instance import bot
import discord
from bases.update_table import UpdateContext, update_table


class server_state():
    def __init__(self, bot, id):
        self.guild = None
        self.server_db = None
        self.id = id
        self.channels = {}

    async def sync_with_database(self):
        await self.create_or_return_channel(TextChannelEnum.LEADERBOARD)
        await self.create_or_return_channel(TextChannelEnum.TASKS)
        await self.sync_all_channels()
        await self.sync_all_users()
        # TODO: sync users

    async def get_guild(self):
        '''caching the guild to reduce api calls'''
        if not self.guild:
            self.guild = self.bot.get_guild(self.id)
        return self.guild

    # TODO: I could probably use the other method I made here
    # what was I trying to say??
    async def get_or_create_server(self):
        if self.server_db:
            return self.server_db
        # Try to get the server from the database
        server, created = await Server.get_or_none(id=self.id), False

        # If the server does not exist, create a new one
        if server is None:
            await create_server()

        # Return the server and a boolean indicating whether it was created or not
            self.server_db = server

        async def create_server():
            guild = await self.get_guild()
            servers = await Server.all()
            server = await Server.create(id=self.id, name=self.guild.name)
            created = True
            await server.save()

        return server, created


class server_sync(server_state):
    def __init__(self, bot, id):
        super().__init__(bot, id)
        self.bot = bot

    async def get_or_create_channel(self, textChannel, channel_type=None):
        if channel_type is None:
            channel_type = self.get_channel_type(textChannel)
        server, created = await self.get_or_create_server()
        channel = await Channel.get_or_none(discord_id=textChannel.id, server=server)
        if channel is None:
            channel = await Channel.create(discord_id=textChannel.id, server=server, name=textChannel.name, channel_type=channel_type)
            created = True
            await channel.save()
        return channel, created

    async def sync_all_channels(self):
        discord_channels = await self.get_discord_channels()
        await self.sync_database_channels_with_discord(discord_channels)
        await self.remove_stale_channels_from_database(discord_channels)

    async def sync_database_channels_with_discord(self, discord_channels):
        for channel_id, channel in discord_channels.items():
            await self.get_or_create_channel(channel)

    def get_channel_type(self, channel):
        if channel.type.name == 'text':
            return TextChannelEnum.TEXT
        if channel.type.name == 'voice':
            return TextChannelEnum.VOICE
        if channel.type.name == 'category':
            return TextChannelEnum.CATEGORY
        else:
            print('whats going on here')

    async def get_discord_channels(self):
        guild = await self.get_guild()
        return {str(channel.id): channel for channel in guild.channels}

    # TODO: this funciton is not being implemented right now
    async def update_channel_if_needed(self, channel_entry, discord_channel):
        if channel_entry.name != discord_channel.name:
            channel_entry.name = discord_channel.name
            await channel_entry.save()

    async def remove_stale_channels_from_database(self, discord_channels):
        db_channels = await Channel.filter(server_id=self.id)
        for channel_entry in db_channels:
            if channel_entry.discord_id not in discord_channels:
                await channel_entry.delete()

    async def delete_channel(self, channel):
        server = await Server.get_or_none(id=self.id)
        channel_db = await Channel.get_or_none(discord_id=channel.id, server=server)
        if channel_db:
            await channel_db.delete()

    async def rename_channel(self, discord_channel):
        channel, created = await self.get_or_create_channel(discord_channel)
        channel.name = discord_channel.name
        await channel.save()


class bot_owned_channels(server_state):
    def __init__(self, bot, id):
        super().__init__(bot, id)

    async def create_channel_on_discord(self, channel_type):
        guild = await self.get_guild()
        channel_name = channel_type.value
        channel = await guild.create_text_channel(channel_name)
        await self.get_or_create_channel(channel, channel_type)
        return channel

    async def create_or_return_channel(self, channel_type: TextChannelEnum):
        """this is a special wrapper around channel creation,
        creates a channel if no lb | task channel is present"""
        channel = await self.has_channel_of_type(channel_type)
        if not channel:
            return await self.create_channel_on_discord(channel_type)
        return channel

    async def has_channel_of_type(self, channel_type: TextChannelEnum):
        """this one tests if the server already has a channel of type leaderboard or task"""
        channel_entry = await Channel.filter(server_id=self.id, channel_type=channel_type).first()
        if channel_entry:
            guild = await self.get_guild()
            discord_channel = guild.get_channel(int(channel_entry.discord_id))
            if discord_channel:
                return discord_channel
            else:
                await channel_entry.delete()
        return None

# UserServerManager class


class user_class(update_table):
    def __init__(self):
        # super().__init__()
        self.update_methods = update_table()

    async def create_user(self, user_data):
        # Custom create function for User
        pillars = await Pillar.all()
        user = await user_class.create(**user_data)
        await user.save()
        for pillar in pillars:
            await UserPillar.create(user=user, pillar=pillar)
        return user

    async def get_or_create(self, discord_user):
        context = UpdateContext(
            table=User,
            filter_key='discord_id',
            data=self.create_user_object(discord_user),
            custom_create=self.create_user
        )
        await self.update_methods.get_or_create(context)

    def create_user_object(self, discord_user):
        # Convert a Discord user object to a dictionary suitable for User model
        return {'discord_id': discord_user.id, 'display_name': discord_user.display_name}


# Usage example


class user_server_manager(update_table, server_state):
    def __init__(self, bot, id):
        server_state.__init__(self, bot, id)
        update_table.__init__(self)
        self.user_class = user_class()

    async def create(self, member):
        user = await self.user_class.get_or_create(discord_user=member)
        server = await self.get_or_create_server()
        await self.user_class.get_or_create(user=user, server=server)

    async def sync_all_users(self):
        guild = await self.get_guild()
        for discord_user in guild.members:
            await self.create(discord_user)


class server_class(server_sync, bot_owned_channels, user_server_manager):
    def __init__(self, bot, id):
        server_sync.__init__(self, bot, id)
        bot_owned_channels.__init__(self, bot, id)
        user_server_manager.__init__(self, bot, id)

# server_manager = server_class(bot)
