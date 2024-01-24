from discord.ext import commands
# from event_emitters.vc_event_emitter import vc_event_manager
from model_managers_tortoise.vc_events import VCEvent
# from event_handlers.vc_event_handler import vc_event_handler
# from event_emitters import vc_event_emitter
from utils.error_handler import class_error_handler

from event_emitters.vc_event_manager import VCEventConditionState


async def setup(bot):
    # event_manager = event_manager_baseclass(vc_event_handler, vc_event_emitter(bot), bot=bot)
    await bot.add_cog(vc_events_cog(bot))

@class_error_handler
class vc_events_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        vc_event = VCEvent(self.bot, member, before, after)
        vc_event_manager = VCEventConditionState(bot=self.bot, event=vc_event)
        await vc_event_manager.evaluate_all()
