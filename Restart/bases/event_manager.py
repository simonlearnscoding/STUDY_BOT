class EventManager:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    # LATER: if I will scale this I can
    # consider publishing only to selected subscribers in the future
    async def publish(self, event_name, data):
        print(f"event: {event_name}")

        try:
            for subscriber in self.subscribers:
                if hasattr(subscriber, event_name):
                    method = getattr(subscriber, event_name)
                    await method(data)
        except Exception as e:
            print(e)
        return


event_manager = EventManager()
