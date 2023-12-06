from utils.error_handler import error_handler
"""
Example use

# Example usage
vc_handler = EventHandler()
vc_emitter = EventEmitter()
vc_event_manager = event_handler_baseclass(handler, emitter)

client.on(vcevent):
    vc_event_manager(vcevent)
"""


class event_manager_baseclass():
    def __init__(self, event_handler=None, event_emitter=None, bot=None):
        if bot is None:
            raise RuntimeError('No bot defined')
        self.handler = event_handler
        self.emitter = event_emitter
        self.bot = bot  # Add a reference to the bot

    """
     Loop through the methods of self.handler
     and if any of them returns true
     it will run self.emit(event_triggered_str, event)
     """

    @error_handler
    async def handle(self, event=None, event_triggered_str=None):

        if event_triggered_str:
            await self.emit(event_triggered_str, event)

        if self.handler is None:
            return RuntimeError('No handler defined')

        event_triggered_str = await self.handler.handle(event)
        await self.emit(event_triggered_str, event)

    """
    Loop through the methods of event.emitter
    if any of them has the same name as event_triggered_str
    call that function with event as input value
    if none of the methods have the same name as event_triggered_str
    throw an Error
    """

    @error_handler
    async def emit(self, event_triggered_str, event):
        if self.emitter is None:
            raise RuntimeError('No emitter defined')

        # Check if the emitter has a method with the name event_triggered_str
        #TODO: refactor!
        method = getattr(self.emitter, event_triggered_str, None)
        if method is not None and callable(method):
            # Call the method
            return await method() if event is None else method(event)

            # Dispatch a custom event to the bot

        else:
            # No method found with the name event_triggered_str
            raise AttributeError(
                f"Method '{event_triggered_str}' not found in emitter")
