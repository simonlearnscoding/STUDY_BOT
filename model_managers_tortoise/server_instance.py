from model_managers_tortoise.database_managers import *

from tortoise_models import Server
from pydispatch import dispatcher



class ServerFilterStrategy(FilterStrategy):
    async def filter(self):
        return await self.table.filter(id=str(self.id)).first()


class ServerGetDataStrategy(GetDataStrategy):
    async def get_data(self):
        return {"id": self.id, "name": self.name}


class ServerCreateStrategy(CreateStrategy):
    async def create(self):
        await self.sync_channels()
        await self.sync_user_server()


class ServerUpdateStrategy(UpdateStrategy):
    async def update(self):
        await UpdateStrategy.update_name_if_changed(self)
        print(f'updating server {self.entity.name}')
        await self.sync_channels()


class ServerDeleteStrategy(DeleteStrategy):
    async def delete(self):
        channel_db = await self.table.get_or_none(
            id=str(self.id)
        )

        if channel_db:
            print(f'deleting {self.entity.name}')
            await channel_db.delete()


class server(database_base_class):
    def __init__(self, bot, entity):
        super().__init__(
            entity=entity,
            bot=bot,
            table=Server,
            get_data_strategy=ServerGetDataStrategy,
            filter_strategy=ServerFilterStrategy,
            create_strategy=ServerCreateStrategy,
            update_strategy=ServerUpdateStrategy,
            # ignore this error its just due to typing I
        )
        self.delete_strategy = ServerDeleteStrategy

    async def sync_channels(self):
        # dispatcher.connect(async_event_handler, signal="async_custom_event")
        from model_managers_tortoise.channel_db_manager import channel_manager
        self.channel_manager = channel_manager(bot=self.bot, entity=self.entity)
        await self.channel_manager.sync_channels()

    async def sync_user_server(self):
        from model_managers_tortoise.user_server import user_server_manager
        user_server_man = user_server_manager(self.bot, entity=self.entity)
        await user_server_man.sync_table_with_data()
