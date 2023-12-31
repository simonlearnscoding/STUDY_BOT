from abc import ABC, abstractmethod
from tortoise_models import Server
from typing import List, Set, Any


class database_base_class():
    def __init__(self, bot, table):
        self.bot = bot
        self.table = table

    """
    ALL CHILDREN OF DATABASE_BASE_CLASS MUST
    HAVE THE FOLLOWING TWO METHODS IMPLEMENTED:
    """
    """
    Abstract method to fetch the entity.
    """

    """
    Return the data in a db_friendly format
    """

    async def create_db_entry_if_not_exist(self, custom_create=None):
        db_entry = await self.filter()
        if not db_entry:
            await self.create_table_entry()
            return self.db_entry, True
        return db_entry, False

    async def create_table_entry(self):
        data = self.get_data()
        if self.has_method("custom_create"):
            await custom_create(data)
        return await self.table.create(**data)

    async def check_if_entry_needs_update(self, data, db_entry):
        if self.db_entry_needs_update(db_entry, data):
            await db_entry.update_from_dict(data)
            await db_entry.save()

    def has_method(self, method_name):
        return hasattr(self, method_name)

    def db_entry_needs_update(self, db_entry, data):
        return any(getattr(db_entry, key) != value for key, value in data.items())


class table_manager(ABC):
    def __init__(self, table, child_class, bot):
        self.table = table
        self.child_class = child_class
        self.bot = bot
        self.children_instances = []

    @abstractmethod
    def get_child_entities(self) -> List[Any]:
        """ all kids should have this
        function that will fetch all of
        their kids ids as array"""
        pass

    async def create_db_instances_from_discord_data(self):
        """
        takes an array of ids and returns an array of child class objects
        """
        for child in self.children_instances:
            await child.create_db_entry_if_not_exist()

    def create_child_instances_from_array(self, entities):
        for child in entities:
            self.children_instances.append(self.child_class(bot=self.bot, entity=child))

    async def run_custom_update_if_exists(self, obj):
        if hasattr(obj, "custom_update") and callable(getattr(obj, "custom_update")):
            await obj.custom_update()

    async def sync_table_with_data(self):
        children_entities = self.get_child_entities()
        self.create_child_instances_from_array(children_entities)
        await self.create_db_instances_from_discord_data()
        await self.remove_redundant_from_db(children_entities)
        await async_apply_to_each(self.run_custom_update_if_exists, self.children_instances)

    async def remove_redundant_from_db(self, valid_ids):
        all_db_entries = await self.table.all()
        results = await async_apply_to_each(self.check_and_delete_if_redundant, all_db_entries, valid_ids)
        return results

    async def check_and_delete_if_redundant(self, db_entry, valid_ids):
        """
        Checks and deletes the db_entry if it's not in valid_ids.
        """
        db_fields = db_entry._meta.fields

        # Check if 'discord_id' is in the list of database fields
        discord_id_exists = 'discord_id' in db_fields

        if discord_id_exists:
            if hasattr(db_entry, 'discord_id'):
                db_entry_id = int(getattr(db_entry, 'discord_id'))
            else:
                db_entry_id = getattr(db_entry, 'id')
                if db_entry_id not in valid_ids:
                    await db_entry.delete()
            return True  # Indicates that deletion occurred
        return False  # Indicates no deletion

    async def fetch_table_data(self):
        return await self.table.all()


async def async_apply_to_each(func, array, *args, **kwargs):
    """
    Applies a given async function to each element in the array.
    Additional arguments and keyword arguments are passed to the function.
    """
    results = []
    for element in array:
        result = await func(element, *args, **kwargs)
        results.append(result)
    return results
