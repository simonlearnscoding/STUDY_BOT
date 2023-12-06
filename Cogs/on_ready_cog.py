from event_emitters.connect_emitter import connect_emitter
from discord.ext import commands
from bases.event_manager_base import event_manager_baseclass
from utils.error_handler import error_handler


async def setup(bot):

    event_manager = event_manager_baseclass(
        event_emitter=connect_emitter(bot),
        bot=bot
    )
    await bot.add_cog(connect_events_cog(bot, event_manager))


class connect_events_cog(commands.Cog):
    def __init__(self, bot, event_manager):
        self.bot = bot
        self.event_manager = event_manager

    @commands.Cog.listener()
    @error_handler
    async def on_ready(self):
        await self.event_manager.handle(event_triggered_str="on_ready")
