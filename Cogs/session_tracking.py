# from bases.event_manager import event_manager
# from spqrapp.models import User
# from Settings.main_settings import bot
from discord.ext import commands
from Cogs.VC_events import VCEvent

from Cogs.decision_tree import decision_tree
from Cogs.vc_event_manager import vc_event_manager


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(user_vc_events(bot))


class user_vc_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,  member, before, after):
        vc_event = VCEvent(member, before, after)
        event_name = decision_tree.check_event_type(
            vc_event)

        # Create an instance of VCEvent
        vc_event_manager.handle_vc_event(event_name, vc_event)
