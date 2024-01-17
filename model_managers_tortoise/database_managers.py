from abc import ABC, abstractmethod
from typing import Any
from discord import Guild

from utils.error_handler import class_error_handler


# from model_managers_tortoise.functional_methods import async_apply_to_each
# from tortoise_models import Server
# from bases.event_manager_base import event_manager_baseclass
# from event_emitters.base_event_emitter import base_event_emitter


class StrategyBase(ABC):
    pass

    def __init__(self, instance):
        self.instance = instance


class CreateStrategy(StrategyBase):
    async def create(self) -> Any:
        """ No operation, do nothing """
        pass


class DefaultCreateStrategy(CreateStrategy):
    async def create(self):
        pass


class UpdateStrategy(StrategyBase):
    @abstractmethod
    async def update(self) -> Any:
        """ No operation, do nothing """
        pass

    @staticmethod
    async def update_name_if_changed(self):
        if UpdateStrategy._name_changed(self):
            self.db_entry.name = self.entity.name
            print(f'updating {self.entity.name}')
            await self.db_entry.save()

    @staticmethod
    async def update_attributes_if_changed(self):
        # Get all attributes of the class instance
        class_attributes = vars(self.entity)

        # Compare each attribute with the corresponding attribute in the db entry
        for key, class_value in class_attributes.items():
            if key == 'id':
                continue
            if key == 'role_requirements':
                continue
            # Assuming db_entry is the database entry and is accessible
            db_value = getattr(self.db_entry, key, None)
            # Check if the attribute has changed
            if class_value != db_value:
                # Update the database entry
                setattr(self.db_entry, key, class_value)
                print(f'Updating {key}: {class_value}')

        # Save the changes to the database entry
        await self.db_entry.save()

    @staticmethod
    def _name_changed(self):
        if ((not self.db_entry.name) or (not self.entity.name)):
            print('here we are')
        discord_name = self.entity.name
        db_name = self.db_entry.name
        return self.entity.name != self.db_entry.name


class DefaultUpdateStrategy(UpdateStrategy):
    async def update(self):
        await UpdateStrategy.update_name_if_changed(self)


class FilterStrategy(StrategyBase):
    @abstractmethod
    async def filter(self) -> Any:
        """ Implement the filter strategy """
        pass


class GetDataStrategy(StrategyBase):
    def __init__(self, instance):
        super().__init__(instance)

    @abstractmethod
    def get_data(self) -> Any:
        """ Implement the filter strategy """
        pass


class DeleteStrategy(StrategyBase):
    @abstractmethod
    async def delete(self):
        """
        Will take a DB entry and probably delete it
        or do something special if required
        """
        pass


class DefaultDeleteStrategy(DeleteStrategy):
    async def delete(self):
        await self.create_or_nothing()
        print(f'deleting ${self.db_entry}')
        await self.db_entry.delete()

@class_error_handler
class database_base_class():
    def __init__(self, bot, table, filter_strategy, get_data_strategy,
                 entity,
                 create_strategy=DefaultCreateStrategy,
                 update_strategy=DefaultUpdateStrategy,
                 delete_strategy=DefaultDeleteStrategy,
                 ):
        self.bot = bot
        self.entity = entity
        self.name = entity.name
        self.id = entity.id
        self.table = table
        self.update_strategy = update_strategy
        self.get_data_strategy = get_data_strategy
        self.create_strategy = create_strategy
        self.filter_strategy = filter_strategy
        self.delete_strategy = delete_strategy,
        self.db_entry = None

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

    async def create_or_update(self):
        self.db_entry, created = await self.get_or_create()

        if created:
            await self.create_strategy.create(self)
        else:
            await self.update_strategy.update(self)

    async def create_or_nothing(self):
        self.db_entry, created = await self.get_or_create()
        if created:
            await self.create_strategy.create(self)
        return self.db_entry, created

    async def get_or_create(self):
        if self.db_entry:
            return self.db_entry, False
        self.db_entry = await self.filter_strategy.filter(self)
        if self.db_entry:
            return self.db_entry, False

        self.db_entry = await self.create_new_db_entry()
        return self.db_entry, True

    async def create_new_db_entry(self):
        data = await self.get_data_strategy.get_data(self)
        db_entry = await self.table.create(**data)
        print(f'created {db_entry}')
        return db_entry

    def has_method(self, method_name):
        return hasattr(self, method_name)
