
from model_managers_tortoise.table_manager import *
from tortoise_models import Activity, ActivityRewards, Pillar
from model_managers_tortoise.database_managers import FilterStrategy, UpdateStrategy, GetDataStrategy, database_base_class, CreateStrategy
rewards_presets = {
    "studying": {
        "done_reward": 10,
        "reward_treshold_minutes": 240,
        "reward_total_treshold": 400,
        "reward_per_minute": 8,
        "reward_while_cam_on": 10,
        "reward_after_treshold": 5,
    },
    "workout": {
        "done_reward": 30,
        "reward_treshold_minutes": 60,
        "reward_total_treshold": 130,
        "reward_per_minute": 10,
        "reward_while_cam_on": 10,
        "reward_after_treshold": 7,
    }
}


activity_list = [
    {"id": "1", "name": 'Study', "description": 'studying', "activity_rewards": rewards_presets['studying'], "Pillar": '1'},
    {"id": "2", "name": 'Workout', "description": 'working out', "activity_rewards": rewards_presets['workout'], "Pillar": '2'},
    {"id": "3", "name": 'Reading', "description": 'Readingg', "activity_rewards": rewards_presets['workout'], "Pillar": '1'},
    {"id": "4", "name": 'Meditation', "description": 'Meditation', "activity_rewards": rewards_presets['studying'], "Pillar": '1'},
]


class ActivityCreateStrategy(CreateStrategy):
    # TODO: adapt it
    async def create(self):
        pass


class ActivityUpdateStrategy(UpdateStrategy):
    async def update(self):
        # TODO: adapt it

        await ActivityUpdateStrategy.update_attributes_if_changed(self.db_entry, self.entity, exceptions=['id', 'activity_rewards', 'Pillar'])
        activity_rewards = await self.db_entry.activity_rewards
        class_activity_rewards = DictToClass(self.entity.activity_rewards)
        await ActivityUpdateStrategy.update_attributes_if_changed(activity_rewards, class_activity_rewards, exceptions=['id'])

        class_pillar = await Pillar.filter(id=self.entity.Pillar).first()
        db_pillar = await self.db_entry.pillar
        if db_pillar != class_pillar:
            self.db_entry.pillar = class_pillar
            await self.db_entry.save()

    @staticmethod
    async def update_attributes_if_changed(db_entry, entity, exceptions):
        # Get all attributes of the class instance
        class_attributes = vars(entity)

        # Compare each attribute with the corresponding attribute in the db entry
        for key, class_value in class_attributes.items():
            if key in exceptions:
                continue
            # Assuming db_entry is the database entry and is accessible
            db_value = getattr(db_entry, key, None)
            # Check if the attribute has changed
            if class_value != db_value:
                # Update the database entry
                setattr(db_entry, key, class_value)
                print(f'Updating {key}: {class_value}')
                # Save the changes to the database entry
                await db_entry.save()


class ActivityFilterStrategy(FilterStrategy):
    # TODO: adapt it
    async def filter(self):
        return await self.table.filter(id=str(self.id)).first()


class activity_class(database_base_class):
    def __init__(
        self,
        bot,
        entity,
    ):
        database_base_class.__init__(
            self,
            entity=entity,
            bot=bot,
            table=Activity,
            filter_strategy=ActivityFilterStrategy,
            get_data_strategy=ActivityGetDataStrategy,
            update_strategy=ActivityUpdateStrategy,
            create_strategy=ActivityCreateStrategy
        )


class DictToClass:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class ActivityGetDataStrategy(GetDataStrategy):
    async def get_data(self):

        activity_rewards = await ActivityRewards.create(**self.entity.activity_rewards)
        pillar = await Pillar.filter(id=self.entity.Pillar).first()
        return {
            'id': self.entity.id,
            'name': self.entity.name,
            'description': self.entity.description,
            'pillar': pillar,
            'activity_rewards': activity_rewards
        }


class GetActivityEntitiesStrategy(GetChildEntitiesStrategy):
    def get_child_entities(self, activity_listlist=activity_list):
        # Instantiate PillarEntity objects
        activity_entities = [DictToClass(data) for data in activity_listlist]
        return activity_entities


class activity_manager(table_manager):
    def __init__(self, bot):
        super().__init__(
            table=Activity,
            bot=bot,
            child_entities_strategy=GetActivityEntitiesStrategy,
            child_class=activity_class
        )
