class EventManager:
    def __init__(self):
        self.handlers = {}

    def subscribe(self, event_name, handler):
        if event_name not in self.handlers:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)

    def publish(self, event_name, data):
        if event_name in self.handlers:
            for handler in self.handlers[event_name]:
                handler(data)

event_manager = EventManager()