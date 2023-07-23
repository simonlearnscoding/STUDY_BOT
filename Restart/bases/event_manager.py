import datetime

""" 
This is a Pub Sub / Eventmanager design pattern.
many objects subscribe themselves to this eventmanager and trigger 
specific functions when 
"""
class EventManager:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    # LATER: if I will scale this I should
    # consider publishing only to selected subscribers in the future
    async def publish(self, event_name, data):
        timestamp = datetime.datetime.now().strftime(" %H:%M:%S")
        # print(f"[{timestamp}] - {event_name}")
        # print(f"event: {event_name}")
        try:

            # Get a list of subscribers that have the event_name attribute
            filtered_subscribers = [subscriber for subscriber in self.subscribers if hasattr(subscriber, event_name)]

            # Call the method on each subscriber
            for subscriber in filtered_subscribers:
                method = getattr(subscriber, event_name)
                # print(f"[{timestamp}] - {type(subscriber).__name__} reacted to {event_name}")
                await method(data)

        except Exception as e:
            print(e)
        return

"""
I create one instance of this 
to store all of the subscribers
"""
event_manager = EventManager()
