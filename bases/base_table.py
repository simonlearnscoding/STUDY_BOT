from dataclasses import dataclass
from typing import Optional, Callable, Any


@dataclass
class UpdateContext:
    table: Any
    filter_key: str
    custom_create: Optional[Callable[[Any], Any]] = None


class table_manager():
    def __init__(self, table, child_class):
        self.table = table
        self.child_class = child_class
        self.children = []


class server_manager(table_manager):
    def __init__(self, bot):
        super().__init__(table=Server, child_class=server_class)
        self.bot = bot


class channel_manager(table_manager):
    def __init__(self, bot, guild):
        super().__init__(table=Channel, child_class=channel_class)
        self.bot = bot
        self.guild = guild
    # TODO: refactor this one

    def get_channel_type(self, channel):
        if channel.type.name == 'text':
            return TextChannelEnum.TEXT
        elif channel.type.name == 'voice':
            return TextChannelEnum.VOICE
        elif channel.type.name == 'category':
            return TextChannelEnum.CATEGORY
        else:
            print('Unknown channel type:', channel.type.name)
            return None

    async def get_discord_channels(self):
        return {channel.id: channel for channel in guild.channels}


class database_base_class:
    def __init__(self, table):
        self.table = table

    async def get_or_create(self, filter_key, data, custom_create=None):
        filter_condition = {filter_key: data[filter_key]}
        db_entry = await self.table.filter(**filter_condition).first()

        if not db_entry:
            if custom_create:
                db_entry = await custom_create(data)
            else:
                db_entry = await self.table.create(**data)
        else:
            if self.db_entry_needs_update(db_entry, data):
                await db_entry.update_from_dict(data)
                await db_entry.save()

        return db_entry

    def db_entry_needs_update(self, db_entry, data):
        return any(getattr(db_entry, key) != value for key, value in data.items())


class database_update_methods:
    def __init__(self, table):
        self.db_base = database_base_class(table)

    async def update_table_with_data(self, data_list, filter_key, custom_create=None):
        existing_ids = set()
        for data in data_list:
            db_entry, _ = await self.db_base.get_or_create(filter_key, data, custom_create)
            existing_ids.add(getattr(db_entry, filter_key))

        await self.remove_redundant_from_db(existing_ids, filter_key)

    async def remove_redundant_from_db(self, valid_ids, filter_key):
        all_db_entries = await self.db_base.table.all()
        for db_entry in all_db_entries:
            if getattr(db_entry, filter_key) not in valid_ids:
                await db_entry.delete()
