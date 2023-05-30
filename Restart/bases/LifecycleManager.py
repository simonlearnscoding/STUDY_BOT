from cogs.leaderboard.filter import Filter_Manager
from cogs.leaderboard.datasets import Dataset_Manager
from cogs.leaderboard.image import Image_Manager

#TODO: compare with state_manager -> keep only one of the two
class_lookup = {
    "Filter_Manager": Filter_Manager,
    "Dataset_Manager": Dataset_Manager,
    "Image_Manager": Image_Manager,
    # Add other classes here...
}


class SingletonFactoryManager:
    def __init__(self):
        self.instances = {}

    async def create(self, classname, key, data=None):
        if (classname, key) in self.instances:
            return self.instances[(classname, key)]

        class_obj = class_lookup[classname]
        instance = class_obj(key)

        if hasattr(instance, "initialize"):
            if data is not None:
                await instance.initialize(key, data)
            else:
                await instance.initialize(key)
        self.instances[(classname, key)] = instance
        return instance

    async def destroy(self, classname, key):
        if (classname, key) not in self.instances:
            return
        instance = self.instances[(classname, key)]
        if hasattr(instance, "destroy"):
            await instance.destroy()
        del self.instances[(classname, key)]
        return

    def get_all(self):
        return self.instances
