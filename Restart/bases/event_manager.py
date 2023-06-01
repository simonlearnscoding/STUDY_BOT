class EventManager:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def publish(self, event_name, data):
        print(f'triggered {event_name}')

        try:
            for subscriber in self.subscribers:
                if hasattr(subscriber, event_name):
                    method = getattr(subscriber, event_name)
                    await method(data)
        except Exception as e:
            print(e)
        return


event_manager = EventManager()
