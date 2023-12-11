from utils.error_handler import class_error_handler
"""
Example use

# Example usage
vc_handler = EventHandler()
vc_emitter = EventEmitter()
vc_event_manager = event_handler_baseclass(handler, emitter)

client.on(vcevent):
    vc_event_manager(vcevent)
"""


@class_error_handler
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

    async def handle(self, event=None, event_triggered_str=None):

        if event_triggered_str:
            await self.emit(event_triggered_str, event)

        if self.handler is None:
            return RuntimeError('No handler defined')

        event_triggered_str = await self.handler.handle(event)
        if event_triggered_str == 'pass_event':
            return
        await self.emit(event_triggered_str, event)

    """
    Loop through the methods of event.emitter
    if any of them has the same name as event_triggered_str
    call that function with event as input value
    if none of the methods have the same name as event_triggered_str
    throw an Error
    """

    async def emit(self, event_triggered_str, event):
        method = self.lookup_method(event_triggered_str)
        if method:
            return await self.invoke_method(method, event)
        else:
            raise AttributeError(f"Method '{event_triggered_str}' not found in emitter")

    def lookup_method(self, method_name):
        return getattr(self.emitter, method_name, None)

    async def invoke_method(self, method, event):
        if event is None:
            return await method()
        else:
            return await method(event)
