
from model_managers_tortoise.database_managers import database_base_class
from model_managers_tortoise.table_manager import UserSetterMixin, ServerSetterMixin
from tortoise_models import *

class session_class(database_base_class, ServerSetterMixin, UserSetterMixin):
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
