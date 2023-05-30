from cogs.leaderboard.filter import Filter_Manager
from cogs.leaderboard.datasets import Dataset_Manager
from bases.state_manager import SingletonFactoryManager
from setup.bot_instance import bot
from cogs.leaderboard.image import Image_Manager
#TODO: Instead of member nick I should go with member name
class ContentManager(SingletonFactoryManager):
    def __init__(self):
        self.instance_class = Content_Instance
    async def create(self, name, lb):
        instance = super.create()
        instance.lb.append(lb)
        return instance

Content_Manager = ContentManager()

class Content_Instance:
    def __init__(self, name):
        self.bot = bot
        self.lb = []
        self.name = name

    async def initialize(self, name):
        self.filter = await Filter_Manager.create(name)
        self.dataset = await Dataset_Manager.create(key=name)
        self.data = self.dataset.data
        self.image = await Image_Manager.create_image(name, self.data)
        print("Dataset initialized")

    async def destroy(self):
        try:
            await Filter_Manager.destroy(self.name)
            await Dataset_Manager.destroy(self.name)
            await Image_Manager.destroy(self.name)
        except Exception as e:
            print(e)
