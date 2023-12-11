
from utils.error_handler import class_error_handler


class base_event_emitter():
    def __init__(self, bot):
        self.bot = bot

    # TODO: test if this works
    async def pass_event(self, channel):
        pass
