class event_handler():
  pass

class event_manager():
    def __init__(self, event_handler=None, event_emitter=None, bot=None):
        if bot is None:
            raise RuntimeError('No bot defined')
        self.handler = event_handler
        self.emitter = event_emitter
        self.bot = bot  # Add a reference to the bot
