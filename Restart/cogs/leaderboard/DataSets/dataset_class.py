from Settings.main_settings import bot

from cogs.SingletonFactoryManager import SingletonFactoryManager


class DatasetManager(SingletonFactoryManager):
    async def create_dataset(self, name, lb):
        dataset = await self.create(key=name, instance_class=Dataset)
        dataset.lb.append(lb)
        return dataset

    # This needs to be called when there is no more lb in this array left
    async def destroy_dataset(self, name):
        await self.destroy(name)


class Dataset:
    def __init__(self, filter):
        # TODO: 3. Test filter creation
        # I have to get the data
        # TODO: instead of filter data and image I should have just a lbContent Class
        # self.filter = FilterInstance("today_study_exclude_no_cam")
        self.bot = bot
        self.lb = []
        self.filter = filter

    async def initialize(self):
        print("Dataset initialized")
        # Filter
        # Data
        # Image
