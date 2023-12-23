from abc import ABC, abstractmethod
from tortoise_models import Server
from typing import List, Set, Any


class database_base_class:
    def __init__(self, table, bot, id, filter_key="id"):
        DatabaseHandler.__init__(table, filter_key)
        self.db_entry = None
        self.bot = bot
        self.id = id
        self.entity = self.fetch_entity()
        self.data = self.get_data()

    """
    ALL CHILDREN OF DATABASE_BASE_CLASS MUST
    HAVE THE FOLLOWING TWO METHODS IMPLEMENTED:
    """
    """
    Abstract method to fetch the entity.
    """
    @abstractmethod
    async def fetch_entity(self):
        pass

    """
    Return the data in a db_friendly format
    """
    @abstractmethod
    def get_data(self):
        pass


class DatabaseHandler:
    def __init__(self, table, filter_key="id"):
        self.table = table
        self.filter_key = filter_key
        self.db_entry = None

    async def create_db_entry_if_not_exist(self, data, custom_create=None):
        if self.db_entry:
            return self.db_entry, False

        filter_condition = {self.filter_key: data[self.filter_key]}
        db_entry = await self.table.filter(**filter_condition).first()
        if not db_entry:
            db_entry = await self.create_table_entry(data, custom_create)
            return db_entry, True
        return db_entry, False

    async def create_table_entry(self, data, custom_create):
        if custom_create:
            return await custom_create(data)
        else:
            return await self.table.create(**data)

    async def check_if_entry_needs_update(self, data, db_entry):
        if self.db_entry_needs_update(db_entry, data):
            await db_entry.update_from_dict(data)
            await db_entry.save()

    def db_entry_needs_update(self, db_entry, data):
        return any(getattr(db_entry, key) != value for key, value in data.items())


class table_manager(ABC):
    def __init__(self, table, child_class, bot):
        self.table = table
        self.child_class = child_class
        self.bot = bot

    @abstractmethod
    def get_child_data(self) -> List[Any]:
        """
        Abstract method to get child data. Must be implemented in subclass.
        """
        pass

    def get_entities_by_id(self, ids):
        dict = []
        for id in ids:
            child = self.child_class(bot=self.bot, id=id)
            data = child.get_data()
            dict.append(data)
        return dict

    # I think effectively I want to 
    # call get_or_create for every item in the list
    async def sync_table_with_data(self):
        data_list = self.get_child_data()
        # data_list = await self.get_entities_by_id(data_list)
        # existing_ids = await self.process_and_collect_ids(data_list)
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

    async def fetch_table_data(self):
        return await self.table.all()
