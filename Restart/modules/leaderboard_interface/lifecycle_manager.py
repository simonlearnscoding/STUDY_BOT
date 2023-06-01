from abc import ABC, abstractmethod

from bases.event_manager import event_manager

class LifeCycleManager:
    def __init__(self, event_manager=event_manager):
        self.instances = {}
        event_manager.subscribe(self)

    async def create(self, data, key):
        """
        create if it does not exist yed
        """
        if key in self.instances:
            return self.instances[key]
        instance = self.instance_class(data, self)
        self.event_manager=event_manager

        """
        perform instance specific spawn operation
        """

        if hasattr(instance, "create"):
            await instance.create(data)
        self.instances[key] = instance

        """
        subscribe to the event manager
        """
        event_manager.subscribe(instance)
        filter_instances = self.filter_count(instance)

        """
        publish info to trigger events
        """
        await event_manager.publish(f"created_instance_{instance.name}", instance)
        if instance.name != "leaderboard":
            return

        if filter_instances == 1:
            await event_manager.publish(
                f"first_instance_with_filter_{instance.name}", instance
            )
        return instance

    async def destroy(self, instance):
        """
        perform instance specific destroy operations
        """
        if hasattr(instance, "destroy"):
            await instance.destroy()
        """
        remove instance from instance manager
        """
        to_delete = self.instances[instance.key]
        del self.instances[instance.key]
        """
        unsubscribe from events
        """
        event_manager.unsubscribe(instance)
        """
        publish event to event manager for other objects 
        to react to this
        """
        await event_manager.publish(f"destroyed_instance_{instance.name}", instance)

        """
        counts the amount of instance with this specific filter
        """

        if instance.name != "leaderboard":
            return
        if self.filter_count(instance) == 0:
            await event_manager.publish(
                f"last_instance_with_filter_{instance.name}", instance
            )

    def filter_count(self, object):
        count = 0
        if len(self.instances) == 0:
            return count
        for instance in self.instances:
            if self.instances[instance].filter == object.filter:
                count += 1
        return count

class destroyWhenNoLb(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def last_instance_with_filter_leaderboard(self, instance):
        if instance.filter == self.filter:
            await self.manager.destroy(self)
