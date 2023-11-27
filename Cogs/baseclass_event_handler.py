class event_handler_baseclass():
    def __init__(self, event_handler, event_emitter):
        self.handler = event_handler
        self.emitter = event_emitter

    def handle_event(self, event):
        """
         Loop through the methods of self.handler
         and if any of them returns true run self.emit(event_triggered_str, event)
         """
        return event

    def emit_event(self, event_triggered_str, event):
        """
        Loop through the methods of event.emitter
        if any of them has the same name as event_triggered_str
        call that function with event as input value
        if none of the methods have the same name as event_triggered_str
        throw an Error
        """
        return [event_triggered_str, event]

"""
Example use

# Example usage
vc_handler = EventHandler()
vc_emitter = EventEmitter()
vc_event_manager = EventHandlerBaseClass(handler, emitter)

client.on(vcevent):
    vc_event_manager(vcevent)
"""
