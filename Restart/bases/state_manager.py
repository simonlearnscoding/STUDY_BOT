class SingletonFactoryManager:
    def __init__(self):
        self.instances = {}

    async def create(self, key, data=None):
        if key in self.instances:
            return self.instances[key]
        instance = self.instance_class(key)

        if hasattr(instance, "initialize"):
            if data is not None:
                await instance.initialize(key, data)
            else:
                await instance.initialize(key)
        self.instances[key] = instance
        return instance

    async def destroy(self, key):
        if key not in self.instances:
            return
        instance = self.instances[key]
        if hasattr(instance, 'destroy'):
            await instance.destroy()
        del self.instances[key]
        return

    def get_all(self):
        return self.instances
