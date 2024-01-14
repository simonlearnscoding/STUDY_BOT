from tortoise.expressions import Q
from model_managers_tortoise.database_managers import FilterStrategy, UpdateStrategy, GetDataStrategy, database_base_class
from tortoise_models import Pillar, Role
from model_managers_tortoise.table_manager import *

data_list = [
            {"id": "1", "name": 'VITALITAS', "description": 'workout lll mental health', "color": '#000000'},
            {"id": "2","name": 'STUDY', "description": 'workout and mental health', "color": '#000000'},
            {"id": "3","name": 'DISCIPLINE', "description": 'workout and mental health', "color": '#000000'}
        ]

class PillarUpdateStrategy(UpdateStrategy):
    async def update(self):
        await UpdateStrategy.update_attributes_if_changed(self)


class PillarFilterStrategy(FilterStrategy):
    async def filter(self):
        return await self.table.filter(id=str(self.id)).first()


class PillarGetDataStrategy(GetDataStrategy):
    async def get_data(self):
        return {
            'id': self.entity.id,
            'name' : self.entity.name,
            'description' : self.entity.description,
            'color' : self.entity.color
        }


class pillar_class(database_base_class):
    def __init__(
        self,
        bot,
        entity,
    ):
        database_base_class.__init__(
            self,
            entity=entity,
            bot=bot,
            table=Pillar,
            filter_strategy=PillarFilterStrategy,
            get_data_strategy=PillarGetDataStrategy,
            update_strategy=PillarUpdateStrategy
        )


class DictToClass:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
            
class GetPillarEntitiesStrategy(GetChildEntitiesStrategy):
    def get_child_entities(self, data_list=data_list):


        # Instantiate PillarEntity objects
        pillar_entities = [DictToClass(data) for data in data_list]
        return pillar_entities

class pillar_manager(table_manager):
    def __init__(self, bot):
        super().__init__(
            table=Pillar,
            bot=bot,
            child_entities_strategy=GetPillarEntitiesStrategy,
            child_class=pillar_class
        )
