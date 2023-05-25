class SingletonFactoryManager:
    def __init__(self):
        self.instances = {}

    async def create(self, key, instance_class, data=None):
        if key in self.instances:
            return self.instances[key]
        instance = instance_class(key)

        if hasattr(instance, "initialize"):
            if data is not None:
                await instance.initialize(key, data)
            else:
                await instance.initialize(key)
        self.instances[key] = instance
        return instance

    async def destroy(self, key):
        if key in self.instances:
            instance = self.instances[key]
            del self.instances[key]
        return instance

    def get_all(self):
        return self.instances
