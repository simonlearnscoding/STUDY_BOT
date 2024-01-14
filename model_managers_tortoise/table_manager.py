from abc import ABC, abstractmethod
from typing import Any, Set
from model_managers_tortoise.functional_methods import async_apply_to_each
from model_managers_tortoise.database_managers import StrategyBase


# Strategy Interface for get_child_entities
class GetChildEntitiesStrategy(StrategyBase):

    @abstractmethod
    def get_child_entities(self) -> Set[Any]:
        """ all kids should have this
        function that will fetch all of
        their kids ids as array"""
        pass


# TODO: Refactor! delete method should be in instance class itself
class DeleteStrategy(StrategyBase):
    @abstractmethod
    async def delete(self, db_entry):
        """
        Will take a DB entry and probably delete it
        or do something special if required
        """
        pass


class DefaultDeleteStrategy(DeleteStrategy):
    async def delete(self, db_entry):
        print(f'deleting ${db_entry.name}')
        await db_entry.delete()


class table_manager(ABC):
    def __init__(self,
                 table,
                 child_class,
                 bot,
                 child_entities_strategy,
                 delete_strategy=DefaultDeleteStrategy,
                 ):
        self.table = table
        self.child_class = child_class
        self.bot = bot
        self.children_instances = []
        self.delete_strategy = delete_strategy
        self.get_child_entities = child_entities_strategy.get_child_entities

    async def sync_table_with_data(self):
        await self.create_new_db_entries()
        await self.remove_redundant_db_entries()

    async def remove_redundant_db_entries(self):
        db_entries = await self.get_all_db_entries()
        valid_ids = self.create_id_array_from_children()
        await async_apply_to_each(self.check_and_delete_if_redundant, db_entries, valid_ids)

    async def get_all_db_entries(self):
        return await self.table.filter()

    async def create_new_db_entries(self):
        children_entities = self.get_child_entities(self)
        self.create_child_instances_from_array(children_entities)
        await self.create_or_update_all()

    async def create_or_update_all(self):
        for child_instance in self.children_instances:
            await child_instance.create_or_update()

    def create_child_instances_from_array(self, entities):
        for child in entities:
            self.children_instances.append(self.child_class(bot=self.bot, entity=child))

    async def run_update_function(self, obj):
        await obj.update_strategy.update(obj)

    async def create_db_instances_from_discord_data(self):
        """
        takes an array of entities and returns an array of child class objects
        """
        for child in self.children_instances:
            await child.create_db_entry_if_not_exist()

    def create_id_array_from_children(self):
        array = []
        for child in self.children_instances:
            array.append(int(child.id))
        return array

    async def check_and_delete_if_redundant(self, db_entry, valid_ids):

        """
        checks and deletes the db_entry if it's not in valid_ids.
        """
        db_entry_id = self.get_db_entry_id(db_entry)
        if db_entry_id not in valid_ids:
            await self.delete_strategy.delete(self, db_entry)

    def get_db_entry_id(self, db_entry):
        db_fields = db_entry._meta.fields
        discord_id_exists = 'discord_id' in db_fields

        if discord_id_exists:
            return int(getattr(db_entry, 'discord_id'))
        return int(getattr(db_entry, 'id'))
