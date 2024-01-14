from model_managers_tortoise.database_managers import *
from model_managers_tortoise.table_manager import table_manager, GetChildEntitiesStrategy
from tortoise_models import Server
from model_managers_tortoise.server_db_manager import *

from model_managers_tortoise.server_instance import *


class ServerEntitiesStrategy(GetChildEntitiesStrategy):

    def get_child_entities(self):
        discord_servers = {guild for guild in self.bot.guilds}
        return discord_servers

# Define a function that will be triggered by the event


def event_handler(sender):
    print(f"Event received from {sender}")


class server_manager(table_manager):
    def __init__(self, bot):
        super().__init__(
            table=Server,
            bot=bot,
            child_entities_strategy=ServerEntitiesStrategy,
            child_class=server)

    async def get_all_db_entries(self):
        entries = await self.table.filter()
        return entries
