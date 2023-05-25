from cogs.leaderboard.filter import filter_singleton as Filter
# TODO: Uncomment this
from cogs.leaderboard.queries import DatasetManagerSingleton as data
from cogs.SingletonFactoryManager import SingletonFactoryManager
from Settings.main_settings import bot

#TODO: Instead of member nick I should go with member name
class ContentManager(SingletonFactoryManager):
    async def create_dataset(self, name, lb):
        dataset = await self.create(key=name, instance_class=Content_Instance)
        dataset.lb.append(lb)
        return dataset

    # This needs to be called when there is no more lb in this array left
    async def destroy_dataset(self, name):
        await self.destroy(name)


Content_Manager = ContentManager()


class Content_Instance:
    def __init__(self, name):
        self.bot = bot
        self.lb = []

    async def initialize(self, name):
        self.filter = Filter.get_filter(name)
        self.data = await data.create_dataset(key=name)
        print("Dataset initialized")
        # Data
        # Image
