from event_emitters import base_event_emitter

from utils.error_handler import class_error_handler
"""
ALL OF THE THINGS THAT HAPPEN AS A RESULT OF MESSAGE EVENTS WILL HAPPEN HERE!
"""


# TODO: test if I could do without the class_error_handler
@class_error_handler
class message_event_emitter(base_event_emitter):
    def __init__(self, bot):
        self.bot = bot

    async def task_created(self, channel):
        pass

    async def task_modify(self, channel):
        pass

    async def task_done(self, channel):
        pass
