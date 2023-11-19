import utils.Conditionals as cnd
from bases.event_manager import event_manager
from spqrapp.models import User
from discord.ext import commands
from decision_tree import decision_tree

# from Settings.main_settings import bot

async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(user_vc_events(bot, event_manager=event_manager))



class user_vc_events(commands.Cog):
    def __init__(self, bot, event_manager):
        self.bot = bot
        self.event_manager = event_manager

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        print('called on voice state update')
        decision_tree.check_which_vc_event_to_trigger(before, after, member)

