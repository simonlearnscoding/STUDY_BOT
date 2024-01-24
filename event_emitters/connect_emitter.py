"""
ALL OF THE THINGS THAT HAPPEN AS A RESULT OF VC EVENTS WILL HAPPEN HERE!
"""

from tortoise_models import *
from event_emitters.base_event_emitter import base_event_emitter
from tortoise_connection import init_db_connection
from model_managers_tortoise.user import user_manager
from model_managers_tortoise.pillars import pillar_manager
from model_managers_tortoise.roles import role_manager
from utils.error_handler import class_error_handler, error_handler
from model_managers_tortoise.activities import activity_manager
from model_managers_tortoise.server_db_manager import server_manager


@class_error_handler
class connect_emitter(base_event_emitter):
    def __init__(self, bot):
        super().__init__(bot)

    @error_handler
    async def on_ready(self):

        print('bot ready')
        await self.sync_slash_commands()
        await init_db_connection()
        await self.delete_tables()
        await self.sync_global_tables()

    async def delete_tables(self):
        # await Server.all().delete()
        await Session.all().delete()
        await SessionData.all().delete()
        await SessionPartial.all().delete()
        # await Channel.all().delete()
        # await Pillar.all().delete()
        # await Role.all().delete()
        # await RolePillar.all().delete()
        # await User.all().delete()
        # await UserServer.all().delete()
        pass

    async def sync_slash_commands(self):
        synced = await self.bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")

    async def sync_global_tables(self):
        managers = [
            pillar_manager(self.bot),
            role_manager(self.bot),
            server_manager(self.bot),
            user_manager(self.bot),
            activity_manager(self.bot),
            # Add more managers as needed
            # Maybe user manager if someone changed name?
        ]

        for manager in managers:
            print(manager.table)
            await manager.sync_table_with_data()
