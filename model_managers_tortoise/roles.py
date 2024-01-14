from tortoise.expressions import Q
from model_managers_tortoise.database_managers import FilterStrategy, UpdateStrategy, GetDataStrategy, database_base_class, CreateStrategy
from tortoise_models import Role, RolePillar, Pillar
from model_managers_tortoise.table_manager import *

data_list = [
    {"id": "1", "name": 'GLADIATOR', "description": 'a cladiator', "color": '#000000', "role_requirements": {'1': "5", "2": "5", "3": "1"}},
    {"id": "2", "name": 'GLADIATOR', "description": 'a cladiator', "color": '#000000', "role_requirements": {'1': "1", "2": "1", "3": "1"}},
    {"id": "3", "name": 'GLADIATOR', "description": 'a cladiator', "color": '#000000', "role_requirements": {'1': "1", "2": "5", "3": "1"}},
    {"id": "4", "name": 'PENNER', "description": 'ein penner', "color": '#000000', "role_requirements": {'1': "1", "2": "5", "3": "1"}},
]



class RoleUpdateStrategy(UpdateStrategy):
    async def update(self):
        await UpdateStrategy.update_attributes_if_changed(self)
        await RoleUpdateStrategy.update_role_pillars(self)

    @staticmethod
    async def update_role_pillars(self):
        for key, value in self.entity.role_requirements.items():
            pillar = await Pillar.filter(id=key).first()
            role_pillar = await RolePillar.filter(role=self.db_entry, pillar=pillar).first()
            if role_pillar is None:
                role_pillar = await RolePillar.create(role=self.db_entry, pillar=pillar, level=value)
            else:
                if str(role_pillar.level) != value:
                    role_pillar.level = value
                    await role_pillar.save()
                    print('updated pillar level requirement')


class RoleFilterStrategy(FilterStrategy):
    async def filter(self):
        return await self.table.filter(id=str(self.id)).first()


class RoleCreateStrategy(CreateStrategy):
    async def create(self):
        await RoleCreateStrategy.create_role_pillars(self)

    async def create_role_pillars(self):
        for key, value in self.entity.role_requirements.items():
            pillar = await Pillar.filter(id=key).first()
            role_pillar = await RolePillar.create(role=self.db_entry, pillar=pillar, level=value)


class role_class(database_base_class):
    def __init__(
        self,
        bot,
        entity,
    ):
        database_base_class.__init__(
            self,
            entity=entity,
            bot=bot,
            table=Role,
            filter_strategy=RoleFilterStrategy,
            get_data_strategy=RoleGetDataStrategy,
            update_strategy=RoleUpdateStrategy,
            create_strategy=RoleCreateStrategy
        )


class DictToClass:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class RoleGetDataStrategy(GetDataStrategy):
    async def get_data(self):
        return {
            'id': self.entity.id,
            'name': self.entity.name,
            'description': self.entity.description,
            'role_requirements': self.entity.color
        }


class GetRoleEntitiesStrategy(GetChildEntitiesStrategy):
    def get_child_entities(self, data_list=data_list):

        # Instantiate PillarEntity objects
        role_entities = [DictToClass(data) for data in data_list]
        return role_entities


class role_manager(table_manager):
    def __init__(self, bot):
        super().__init__(
            table=Role,
            bot=bot,
            child_entities_strategy=GetRoleEntitiesStrategy,
            child_class=role_class
        )
