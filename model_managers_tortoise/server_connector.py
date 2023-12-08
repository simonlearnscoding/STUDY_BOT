
from tortoise.transactions import in_transaction
from tortoise_models import Server, User, TextChannelEnum
from setup.bot_instance import bot
from model_managers_tortoise.server_manager import server_class
import discord


class server_manager(server_class):
    def __init__(self, bot):
        self.bot = bot
        # self.server = server_class(bot)

    async def sync_all_servers(self):
        discord_servers = {guild.id for guild in self.bot.guilds}
        db_servers = {server.id for server in await Server.all()}
        for server_id in discord_servers:
            server = server_class(bot, server_id)
            await server.sync_with_database()

    async def remove_servers_not_on_discord(self):
        discord_servers = {guild.id for guild in self.bot.guilds}
        db_servers = {server.id for server in await Server.all()}
        await self.remove_servers_from_set(db_servers - discord_servers)

    # TODO: Test
    async def remove_servers_from_set(self, servers_to_remove):
        """
        Removes servers from the database that the bot is no longer a part of
        as a single transaction.

        Parameters:
        servers_to_remove (set): A set of server IDs that the bot has left.
        """
        async with in_transaction():
            for server_id in servers_to_remove:
                # Retrieve the server from the database by its Discord ID
                server_to_remove = await Server.get_or_none(id=server_id)

                # If the server exists in the database, delete it
                if server_to_remove:
                    await server_to_remove.delete()
                    print(
                        f"Removed server with ID {server_id} from the database.")


server_manager = server_manager(bot)
