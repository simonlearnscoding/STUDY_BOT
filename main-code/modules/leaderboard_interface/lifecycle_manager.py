from abc import ABC, abstractmethod

from bases.event_manager import event_manager

class EventSubscriber:
    """
    the only purpose of this class is to
    subscribe classes to the Event manager
    """

    def __init__(self):
        self.event_manager = event_manager
        event_manager.subscribe(self)
        self.event_manager = event_manager
        self.publish = self.event_manager.publish
        self.unsubscribe = self.event_manager.unsubscribe
        self.subscribe = self.event_manager.subscribe
class LifeCycleManager(EventSubscriber):
    def __init__(self):
        self.instances = {}
        super().__init__()
    async def create(self, data, key):
        """
        create if it does not exist yed
        """
        if key in self.instances:
            return self.instances[key]
        instance = self.instance_class(data, self)

        """
        perform instance specific spawn operation
        """

        if hasattr(instance, "create"):
            await instance.create(data)
        self.instances[key] = instance

        """
        subscribe to the event manager
        """
        self.event_manager.subscribe(instance)
        # filter_instances = self.filter_count(instance)

        """
        publish info to trigger events
        """
        await self.event_manager.publish(f"_created_instance_{instance.name}", instance)
        # await self.handle_first_instance_with_filter(instance)
        return instance

    async def destroy(self, instance):
        """
        the standard set of actions to run when an instance of
        an object gets destroyed.

        delete the object from the manager dict and so on
        """
        if hasattr(instance, "destroy"):
            await instance.destroy()
        """
        remove instance from instance manager
        """
        del self.instances[instance.key]
        """ unsubscribe from events """
        self.event_manager.unsubscribe(instance)
        """
        publish destruction to the event manager for other objects 
        to react to this
        """
        await self.event_manager.publish(
            f"_destroyed_instance_{instance.name}", instance
        )

        """
        counts the amount of instance with this specific filter
        """

