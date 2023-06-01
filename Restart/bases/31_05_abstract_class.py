from abc import ABC, abstractmethod


class data_object(ABC):
    @abstractmethod
    def create(self):
        pass
    @abstractmethod
    def destroy(self):
        pass
    @abstractmethod 
    def events(self):
        pass

class leaderboard_manager_factory:
    def __init__(self, events):
        self.state = {}
        self.classes = {
            "lb_object": lb_object,
            
        }
        self.events = events
        self.create_listeners()
        
    async def get_member_filter(self, member):
        pass
    def create_listeners(self):
        self.events.subscribe("user_joins_vc", self)
        self.events.subscribe("created_lb", self)
        pass
        
    async def handle_event(self, event_name, data):
        if event_name == "user_joins_tracking_channel":
            await self.user_joins_tracking_channel(data)
            return
        if event_name == "created_lb":
            pass
            await self.created_lb(data)

            
    async def created_lb(self, data):
        pass

    
    async def user_joins_tracking_channel(self, data):
        member = data.member
        filter_name = await self.get_member_filter(member)
        return await self.create(classname="lb_object", key=filter_name, data=data)
        
    async def create(self, classname, key, data):
        if (classname, key) in self.state:
            return self.state[(classname, key)]
        else:
            instance = await self.classes[classname].create(key, data)
            self.state[(classname, key)] = instance
            self.events.subscribe(instance.events, self)
            self.events.publish("created_lb", instance)
    
    
        
class lb_object(data_object):

    @staticmethod
    async def create_private_channel(member):
        #TODO: create private channel here
        return await member.create_dm()
    @staticmethod  
    async def write_and_get_message(member, channel):
        #TODO: write message here
        pass

        
    async def create(self, key, data):
        self.key = key
        self.channel = await lb.create_private_channel(self.member)
        self.message = await self.write_and_get_message(self.member, self.channel)
        self.state = state
        self.events = event
        self.add_instance_events()
        return self
        


    def add_instance_events():
        #TODO: when user leaves vc, destroy lb_object

        pass

    async def destroy(self):
        #TODO: if this is the last lb_object, send an event (no more lb instance for $filter)
        await self.channel.delete()
        if self.state.lb_object[self.filter] == 0:
            
            await self.state.destroy(self.filter)









class filter_object:
    filter: string
    where: dict  # or is it a tuple?


class dataset_object:
    data: dict
    # TODO: add methods to get data from the dataset


class image_object(data_object):
    image_url: string
    def __init__(self, state_manager, event_manager):
        super().__init__(state_manager, event_manager)

    async def initialize(self, key, data=None):
        #TODO: replace with get from user
        self.member = data.member
        filter_name = data.filter
        self.channel = await self.create_private_channel(self.member)
        self.message = await self.write_and_get_message(self.member, self.channel)
        self.add_instance_events()
        
        # this.image_url = ...
    
    async def create():
        pass
        #await super().create()
        #await super().create()

    def add_instance_events():
        pass

class state_manager:
    def __init__(self):
        self.instances = {}

#TODO: import all possible class_objects
class_objects = {
    "lb_object": lb_object,
}




class data_parent():
    def __init__(self, state_manager, event_manage):
        self.state = state_manager
        self.events = event_manager

    async def create(self, classname, key, data=None):
        self.member  = data.member
        if (classname, key) in self.state.instances:
            return self.state.instances[(classname, key)]
         
        instance = await classname.initialize(key, data)
        if hasattr(classname, "initialize"):
            if data is not None:
            else:
                return await classname.initialize(key)
        self.state.instances[(classname, key)] = instance
        #TODO: send event (instance ${name} created)
        return instance

    async def destroy(self, classname, key):
        if (classname, key) not in self.state.instances:
            return
        instance = self.state.instances[(classname, key)]
        if hasattr(instance, "destroy"):
            await instance.destroy()
        del self.state.instances[(classname, key)]
        #TODO: send event (instance ${name} created)
        # send event to the event creator
        return

class data_manager(class_objects):
    def __init__(self, state_manager, event_manager):
        self.state = state_manager
        self.events = event_manager
        self.classes = class_objects
    
    async def get_filter_name(self, member):
        pass

    async def user_joins_vc(self, member):
        data = { }
        data['member'] = member
        data['filter'] = self.get_filter_name(member)
        class_objects['lb_object'].create(data)

    async def create(self, classname, key, data=None):
        if (classname, key) in self.state.instances:
            return self.state.instances[(classname, key)]
    
        instance = self.classes[classname](self.state, self.events)

        # this needs to change inputs
        if hasattr(instance, "initialize"):
            if data is not None:
                await instance.initialize(key, data)
            else:
                await instance.initialize(key)
        self.state.instances[(classname, key)] = instance    




class filter(data_parent):
    @staticmethod
    def initialize(self, key, data=None):
        pass

    @staticmethod
    def create_events(self):
        pass
