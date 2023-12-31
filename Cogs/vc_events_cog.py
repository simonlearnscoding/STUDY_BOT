from discord.ext import commands
from my_types import VCEvent
from event_handlers import vc_event_handler
from event_emitters import vc_event_emitter
from bases.event_manager_base import event_manager_baseclass
from utils.error_handler import error_handler


async def setup(bot):
    event_manager = event_manager_baseclass(
        vc_event_handler, vc_event_emitter(bot),

        bot=bot
    )
    await bot.add_cog(vc_events_cog(bot, event_manager))


class vc_events_cog(commands.Cog):
    def __init__(self, bot, event_manager):
        self.bot = bot
        self.event_manager = event_manager

    @commands.Cog.listener()
    @error_handler
    async def on_voice_state_update(self, member, before, after):
        vc_event = VCEvent(member, before, after)
        await self.event_manager.handle(vc_event)
