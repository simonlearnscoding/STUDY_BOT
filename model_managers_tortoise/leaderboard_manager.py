from tortoise.transactions import in_transaction
from tortoise_models import Server, User
from setup.bot_instance import bot

import discord


class server_manager_class():
    def __init__(self, bot):
        self.bot = bot

    async def create_leaderboard_channel(self, server_id):
        """
        Creates a new leaderboard channel for the given server ID.

        Parameters:
        server_id (str): The ID of the server
        to create a leaderboard channel for.
        """

        channel_id = await self.create_the_leaderboard_channel(server_id)
        await self.create_leaderboard_db_entry(server_id, channel_id)

    async def create_leaderboard_db_entry(self, server_id, channel_id):
        server = await Server.get_or_none(id=server_id)
        server.leaderboard_channel_id = channel_id
        await server.save()

    async def create_the_leaderboard_channel(self, server_id):
        guild = self.bot.get_guild(server_id)
        if not guild:
            return 'guild does not exist'

        overwrites = {guild.default_role: discord.PermissionOverwrite(
            read_messages=False), }
        channel = await guild.create_text_channel('leaderboard', overwrites=overwrites)

        return channel.id


server_manager = server_manager_class(bot)
