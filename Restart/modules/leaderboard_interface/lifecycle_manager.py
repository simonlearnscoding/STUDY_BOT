from abc import ABC, abstractmethod

from bases.event_manager import event_manager


class EventSubscriber:
    def __init__(self):
        self.event_manager = event_manager
        event_manager.subscribe(self)
        self.event_manager = event_manager
        self.publish = self.event_manager.publish
        self.unsubscribe = self.event_manager.unsubscribe
class LastInstanceHandler:
    def __init__(self):
        pass
    async def handle_last_instance_with_filter(self, instance):
        if instance.name == "leaderboard":
            filter_instances = self.filter_count(instance)
            if filter_instances(instance) == 0:
                await self.event_manager.publish(
                    f"_last_instance_with_filter_{instance.name}", instance
                )

    async def handle_first_instance_with_filter(self, instance):
        if instance.name == "leaderboard":
            filter_instances = self.filter_count(instance)
            if filter_instances == 1:
                await self.event_manager.publish(
                    f"_first_instance_with_filter_{instance.name}", instance
                )

    def filter_count(self, object):
        count = 0
        if len(self.instances) == 0:
            return count
        for instance in self.instances:
            if self.instances[instance].filter == object.filter:
                count += 1
        return count

class LifeCycleManager(EventSubscriber, LastInstanceHandler):
    def __init__(self):
        self.instances = {}
        super().__init__()
        # event_manager.subscribe(self)

    async def create(self, data, key):
        """
        create if it does not exist yed
        """
        if key in self.instances:
            return self.instances[key]
        instance = self.instance_class(data, self)
        self.event_manager.subscribe(instance)

        """
        perform instance specific spawn operation
        """

        if hasattr(instance, "create"):
            await instance.create(data)
        self.instances[key] = instance

        """
        subscribe to the event manager
        """

        """
        publish info to trigger events
        """
        await self.event_manager.publish(f"_created_instance_{instance.name}", instance)
        await self.handle_first_instance_with_filter(instance)
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
        self.event_manager.unsubscribe(to_delete)
        del self.instances[instance.key]
        """
        unsubscribe from events
        """
        self.event_manager.unsubscribe(instance)
        """
        publish event to event manager for other objects 
        to react to this
        """
        await self.event_manager.publish(
            f"_destroyed_instance_{instance.name}", instance
        )

        """
        counts the amount of instance with this specific filter
        """

        await self.handle_last_instance_with_filter(instance)





