class SingletonFactoryManager:
    def __init__(self):
        self.instances = {}

    async def create(self, key, instance_class):
        if key in self.instances:
            return self.instances[key]
        instance = instance_class(key)
        if hasattr(instance, "initialize"):
            await instance.initialize()
        self.instances[key] = instance
        return instance

    async def destroy(self, key):
        if key in self.instances:
            instance = self.instances[key]
            del self.instances[key]
        return instance

    def get_all(self):
        return self.instances
