from tortoise.expressions import Q
from bases.update_table import update_table, UpdateContext
from tortoise_models import Pillar, Role


class base_manager(update_table):
    def __init__(self, table, filter_key, data):
        self.table_methods = update_table()
        self.table = table
        self.filter_key = filter_key
        self.data = data

    async def sync_table(self):
        context = UpdateContext(
            table=self.table,
            filter_key=self.filter_key,
            data=self.data
        )
        await self.table_methods.update(context)


pillar_manager = base_manager(
    table=Pillar,
    filter_key='name',
    data=[
        {"name": 'VITALITAS', "description": 'workout and mental health', "color": '#000000'},
        {"name": 'STUDY', "description": 'workout and mental health', "color": '#000000'},
        {"name": 'DISCIPLINE', "description": 'workout and mental health', "color": '#000000'}
    ]
)


# Assuming base_manager is already defined as previously discussed

# Create an instance for role manager with specific data
role_manager = base_manager(
    table=Role,
    filter_key='name',
    data=[
        {"name": 'VITALITAS', "description": 'workout and mental health', "color": '#000000'},
        {"name": 'STUDY', "description": 'workout and mental health', "color": '#000000'},
        {"name": 'DISCIPLINE', "description": 'workout and mental health', "color": '#000000'}
    ]
)


class role_manager_class(base_manager):
    def __init__(self):
        super().__init__()
        self.filter = Q(name=data[name])
        self.table = Role
        self.data = [
            {"name": 'VITALITAS',
             "description": 'workout and mental health',
             "color": '#000000'},
            {"name": 'STUDY',
             "description": 'workout and mental health',
             "color": '#000000'},
            {"name": 'DISCIPLINE',
             "description": 'workout and mental health',
             "color": '#000000'}, ]
