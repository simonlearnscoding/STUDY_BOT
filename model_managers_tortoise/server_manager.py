from enum import Enum

from tortoise.transactions import in_transaction
from tortoise_models import Server, User, Channel, TextChannelEnum
from setup.bot_instance import bot
import discord


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

    async def get_guild(self):
        '''caching the guild to reduce api calls'''
        if not self.guild:
            self.guild = self.bot.get_guild(self.id)
        return self.guild

    async def get_or_create_server(self):
        if self.server_db:
            return self.server_db
        # Try to get the server from the database
        server, created = await Server.get_or_none(id=self.id), False

        # If the server does not exist, create a new one

        if server is None:
            guild = await self.get_guild()
            servers = await Server.all()
            server = await Server.create(id=self.id, name=self.guild.name)
            created = True
            await server.save()

        # Return the server and a boolean indicating whether it was created or not
            self.server_db = server
        return server, created


class server_sync(server_state):
    def __init__(self, bot, id):
        super().__init__(bot, id)
        self.bot = bot

    async def get_or_create_channel(self, textChannel, channel_type=TextChannelEnum.TEXT):
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
            channel_type = self.get_channel_type(channel)
            await self.get_or_create_channel(channel, channel_type)

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


class bot_owned_channels(server_state):
    def __init__(self, bot, id):
        super().__init__(bot, id)

    async def remove_stale_channels_from_database(self, discord_channels):
        db_channels = await Channel.filter(server_id=self.id)
        for channel_entry in db_channels:
            if channel_entry.discord_id not in discord_channels:
                await channel_entry.delete()

    async def create_or_return_channel(self, channel_type: TextChannelEnum):
        """this is a special wrapper around channel creation , 
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

    async def create_channel_on_discord(self, channel_type):
        guild = await self.get_guild()
        channel_name = channel_type.value
        channel = await guild.create_text_channel(channel_name)
        await self.get_or_create_channel(channel, channel_type)
        return channel


#TODO: TEST if refactoring worked
class server_class(server_sync, bot_owned_channels):
    def __init__(self, bot, id):
        super().__init__(bot, id)

# server_manager = server_class(bot)
