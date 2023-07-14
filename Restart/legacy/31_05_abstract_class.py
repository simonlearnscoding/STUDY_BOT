from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Union

from bases.event_manager import event_manager


class data_object(ABC):
    def __init__(self, state_manager):
        self.state_manager = state_manager

    @abstractmethod
    async def async_init(self, data, state):
        # TODO: check if instance already exists
        event_manager.subscribe(self)
        event_manager.publish(f"created_{data['name']}", data)
        pass
    """
    this is to ensure that all data objects follow
    the same structure.

    it also makes sure that all data objects are subscribed
    to the event manager on instantiation
    and that they will publish anything that they do

    """

    @abstractmethod
    def destroy(self) -> None:
        """Abstract method to destroy an object."""
        pass


class lb(data_object):
    def __init__(self, state_manager):
        super().__init__(state_manager)

    async def async_init(self, data, state):
        data['name'] = "lb"
        data['filter_name'] = await self.get_member_filter(data['member'])
        super().async_init(data, state)

    @classmethod
    async def create(self, data, state):
        self = self(state_manager)
        await self.async_init(data, state)
        return self


    async def get_member_filter(self, member) -> None:
        """
        Get the filter for a member.

        Args:
            member: The member to get the filter for.
        """
        pass
        
class leaderboard_event_manager():
    """
    this class will subscribe itself to the event manager
    and it will listen to when a user joins a voice channel
    """
    def __init__(self, event_manager, lb, state) -> None:
        self.event_manager = event_manager()
        event_manager.subscribe(self)
        self.lb = lb
        self.state = state
    
    async def user_joins_tracking_channel(self, data) -> None:
        lb_instance = await self.lb.create(self.state, data)
        """
        this method will be called when a user joins a tracking channel
        """
        pass

class state_manager:
    def __init__(self) -> None:
        """
        Initialize the state_manager.
        this class is used to store the instances of the active leader boards
        and the corresponding data objects.
        """
        leaderboard_event_manager(event_manager, lb, self)


   
class leaderboard_manager_factory:
    def __init__(self, event_manager ) -> None:
        """
        Initialize the leaderboard_manager_factory.

        Args:
            event_manager: An instance of event_manager.
            events: An instance of events.
            lb_object: An instance of lb_object.
        """
        self.state = {}
        event_manager.subscribe(self)
        self.classes = {
            "lb_object": lb_object,
        }
        self.event_manager = event_manager
        self.events = events()

    async def user_joins_tracking_channel(self, data: Dict) -> None:    
        """
        Handle the event when a user joins the tracking channel.

        Args:
            data: A dictionary containing the event data.
        """
        self.create_listeners()
        data['filter_name'] = await self.get_member_filter(data['member'])
        classname = "lb_object"
        await self.create(classname="lb_object", data=data)

    def object_exists(self, classname: str, key: str) -> bool:
        """
        Check if an object exists.

        Args:
            classname: The name of the class.
            key: The key of the object.

        Returns:
            True if the object exists, False otherwise.
        """
        return (classname, key) in self.state

    async def create(self, classname: str, key: str, data: Dict) -> None:
        """
        Create an object.

        Args:
            classname: The name of the class.
            key: The key of the object.
            data: A dictionary containing the data to create the object.
        """
        if self.object_exists(classname, key):
            return
        instance = await self.classes[classname].create(data)
        self.state[(classname, key)] = instance
        self.events.subscribe(instance.events, self)
        self.events.publish("created_lb", instance)

    async def created_lb(self, data: Dict) -> None:
        """
        Handle the event when a leaderboard is created.

        Args:
            data: A dictionary containing the event data.
        """
        await self.created_lb(data)


    def create_listeners(self) -> None:
        """
        Create event listeners.
        """
        self.events.subscribe("user_joins_vc", self)
        self.events.subscribe("created_lb", self)


class lb_object(data_object):
    @staticmethod
    async def create_private_channel(member: Any) -> Any:
        """
        Create a private channel for a member.

        Args:
            member: The member to create a private channel for.

        Returns:
            The created private channel.
        """
        return await member.create_dm()

    @staticmethod  
    async def write_and_get_message(member: Any, channel: Any) -> None:
        """
        Write a message and get it.

        Args:
            member: The member to write a message to.
            channel: The channelI apologize for the abrupt cut-off in the previous message. Here's the continuation of the code:

```python
            channel: The channel to write the message in.
        """
        pass

    async def create(self, key: str, data: Dict) -> 'lb_object':
        """
        Create an lb_object.

        Args:
            key: The key of the lb_object.
            data: A dictionary containing the data to create the lb_object.

        Returns:
            The created lb_object.
        """
        self.key = key
        self.channel = await self.create_private_channel(self.member)
        self.message = await self.write_and_get_message(self.member, self.channel)
        self.state = state
        self.events = event
        self.add_instance_events()
        return self

    def add_instance_events(self) -> None:
        """
        Add instance events.
        """
        pass

    async def destroy(self) -> None:
        """
        Destroy the lb_object.
        """
        await self.channel.delete()
        if self.state.lb_object[self.filter] == 0:
            await self.state.destroy(self.filter)


class filter_object:
    filter: str
    where: Dict  # or is it a tuple?


class dataset_object:
    data: Dict
    # TODO: add methods to get data from the dataset


class image_object(data_object):
    image_url: str

    def __init__(self, state_manager: Any, event_manager: event_manager) -> None:
        """
        Initialize the image_object.

        Args:
            state_manager: An instance of state_manager.
            event_manager: An instance of event_manager.
        """
        super().__init__(state_manager, event_manager)

    async def initialize(self, key: str, data: Optional[Dict] = None) -> None:
        """
        Initialize the image_object.

        Args:
            key: The key of the image_object.
            data: A dictionary containing the data to initialize the image_object.
        """
        self.member = data.member
        filter_name = data.filter
        self.channel = await self.create_private_channel(self.member)
        self.message = await self.write_and_get_message(self.member, self.channel)
        self.add_instance_events()

    async def create(self) -> None:
        """
        Create the image_object.
        """
        pass

    def add_instance_events(self) -> None:
        """
        Add instance events.
        """
        pass



class data_parent():
    def __init__(self, state_manager: state_manager, event_manager: event_manager) -> None:
        """
        Initialize the data_parent.

        Args:
            state_manager: An instance of state_manager.
            event_manager: An instance of event_manager.
        """
        self.state = state_manager
        self.events = event_manager

    async def create(self, classname: str, key: str, data: Optional[Dict] = None) -> Any:
        """
        Create an object.

        Args:
            classname: The name of the class.
            key: The key of the object.
            data: A dictionary containing the data to create the object.

        Returns:
            The created object.
        """
        self.member  = data.member
        if (classname, key) in self.state.instances:
            return self.state.instances[(classname, key)]
         
        instance = await classname.initialize(key, data)
        if hasattr(classname, "initialize"):
            if data is not None:
                return await classname.initialize(key)
        self.state.instances[(classname, key)] = instance
        return instance

    async def destroy(self, classname: strI apologize for the abrupt cut-off again. Here's the continuation and completion of the code:

```python
    async def destroy(self, classname: str, key: str) -> None:
        """
        Destroy an object.

        Args:
            classname: The name of the class.
            key: The key of the object.
        """
        if (classname, key) not in self.state.instances:
            return
        instance = self.state.instances[(classname, key)]
        if hasattr(instance, "destroy"):
            await instance.destroy()
        del self.state.instances[(classname, key)]


class data_manager:
    def __init__(self, state_manager: state_manager, event_manager: event_manager) -> None:
        """
        Initialize the data_manager.

        Args:
            state_manager: An instance of state_manager.
            event_manager: An instance of event_manager.
        """
        self.state = state_manager
        self.events = event_manager
        self.classes = class_objects
    
    async def get_filter_name(self, member: Any) -> None:
        """
        Get the filter name for a member.

        Args:
            member: The member to get the filter name for.
        """
        pass

    async def user_joins_vc(self, member: Any) -> None:
        """
        Handle the event when a user joins the voice channel.

        Args:
            member: The member who joined the voice channel.
        """
        data = { }
        data['member'] = member
        data['filter'] = self.get_filter_name(member)
        class_objects['lb_object'].create(data)

    async def create(self, classname: str, key: str, data: Optional[Dict] = None) -> Any:
        """
        Create an object.

        Args:
            classname: The name of the class.
            key: The key of the object.
            data: A dictionary containing the data to create the object.

        Returns:
            The created object.
        """
        if (classname, key) in self.state.instances:
            return self.state.instances[(classname, key)]
    
        instance = self.classes[classname](self.state, self.events)
        if hasattr(instance, "initialize"):
            if data is not None:
                await instance.initialize(key, data)
            else:
                await instance.initialize(key)
        self.state.instances[(classname, key)] = instance    


class filter(data_parent):
    @staticmethod
    def initialize(self, key: str, data: Optional[Dict] = None) -> None:
        """
        Initialize the filter.

        Args:
            key: The key of the filter.
            data: A dictionary containing the data to initialize the filter.
        """
        pass

    @staticmethod
    def create_events(self) -> None:
        """
        Create events for the filter.
        """
        pass
