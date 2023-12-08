"""
ALL OF THE THINGS THAT HAPPEN AS A RESULT OF VC EVENTS WILL HAPPEN HERE!
"""

from tortoise_connection import init_db_connection
from model_managers_tortoise.server_connector import server_manager

from utils.error_handler import error_handler
# from pydispatch import dispatcher
# from spqrapp.models import Server


class connect_emitter():
    def __init__(self, bot):
        self.bot = bot

    @error_handler
    async def on_ready(self):
        # self.sync_servers_with_database()
        await init_db_connection()

        # Find servers that are in the database but not on Discord
        # await server_manager.remove_servers_not_on_discord
        print('bot ready')
        await server_manager.sync_all_servers()
        # await server_manager.print_all_channels()
