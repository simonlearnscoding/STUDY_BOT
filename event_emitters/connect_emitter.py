"""
ALL OF THE THINGS THAT HAPPEN AS A RESULT OF VC EVENTS WILL HAPPEN HERE!
"""

from tortoise_models import Role, Server, Pillar, User, Channel, RolePillar, TextChannelEnum
from event_emitters.base_event_emitter import base_event_emitter
from tortoise_connection import init_db_connection
# from model_managers_tortoise.server_connector import server_manager
from model_managers_tortoise.pillars import pillar_manager 
from model_managers_tortoise.roles import role_manager 
from utils.error_handler import error_handler
# from pydispatch import dispatcher
# from spqrapp.models import Server
from model_managers_tortoise.server_db_manager import server_manager


class connect_emitter(base_event_emitter):
    def __init__(self, bot):
        super().__init__(bot)

    @error_handler
    async def on_ready(self):
        print('bot ready')
        await init_db_connection()
        # await Server.all().delete()
        # await Channel.all().delete()
        # await Pillar.all().delete()
        # await Role.all().delete()
        # await RolePillar.all().delete()
        print(len(await Channel.all()))
        print(len(await Server.all()))
        servers = server_manager(self.bot)
        await servers.sync_table_with_data()
        pillars = pillar_manager(self.bot)
        await pillars.sync_table_with_data()
        roles = role_manager(self.bot)
        await roles.sync_table_with_data()
        # await role_manager.sync_table()
