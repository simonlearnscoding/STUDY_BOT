
from utils.error_handler import class_error_handler
"""
ALL OF THE THINGS THAT HAPPEN AS A RESULT OF CHANNEL EVENTS WILL HAPPEN HERE!
"""


class channel_event_emitter():
    def __init__(self, bot):
        self.bot = bot
