from abc import ABC, abstractmethod
from tortoise_models import Server
from typing import List, Set, Any

class database_base_class:
    def __init__(self, table, bot, id, filter_key):
        self.table = table
        self.bot = bot
        self.entity = None
        self.id = id
        self.data = self.get_data()
        self.filter_key = filter_key

    def get_entity(self):
        if self.entity is None:
            self.entity = self.fetch_entity()
        return self.entity

    @abstractmethod
    def fetch_entity(self):
        """
        Abstract method to fetch the entity. Must be implemented in subclass.
        """
        pass

    @abstractmethod
    def get_data(self):
        """
        Abstract method to return the data in a db_friendly format
        """

    async def get_or_create(self, data, custom_create=None):
        filter_condition = {self.filter_key: data[self.filter_key]}
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


class table_manager(ABC):
    def __init__(self, table, child_class, bot):
        self.table = table
        self.child_class = child_class
        self.bot = bot

    @abstractmethod
    async def get_child_data(self) -> List[Any]:
        """
        Abstract method to get child data. Must be implemented in subclass.
        """
        pass

    async def sync_table_with_data(self):
        data_list = await self.get_child_data()
        existing_ids = await self.process_and_collect_ids(data_list)
        await self.remove_redundant_from_db(existing_ids)

    async def process_and_collect_ids(self) -> Set[Any]:
        """
        Process each data item: update/create table entries and collect their IDs.
        """
        existing_ids: Set[Any] = set()
        for id in data_list:
            child_instance = self.child_class(bot=self.bot, id=id)  # Create an instance for each data item
            db_entry, _ = await child_instance.get_or_create(id)
            existing_ids.add(getattr(db_entry, self.child_class.filter_key))

        return existing_ids

    async def remove_redundant_from_db(self, valid_ids):
        all_db_entries = await self.table.all()
        for db_entry in all_db_entries:
            if getattr(db_entry, filter_key) not in valid_ids:
                await db_entry.delete()

    async def get_child_data(self) -> Set[Any]:
        
    async def fetch_table_data(self):
        return await self.table.all()
