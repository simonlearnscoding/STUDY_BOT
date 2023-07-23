import utils.Conditionals as cnd
from bases.event_manager import event_manager
from djangoproject.spqrapp.models import User
from discord.ext import commands

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
        try:
            if self.excluding_condition_is_met(before, after, member):
                return
            # TODO: test
            member = await User.object.get_or_create_user(member) # fetch the user from DB
            if cnd.user_joins_tracking_channel(before, after):
                await self.event_manager.publish('_user_joins_tracking_channel', {"member": member, "state": after})
                await self.event_manager.publish('_any_voice_state_update', {"member": member})
                return

            if cnd.user_changed_type_of_tracking(before, after):
                await self.event_manager.publish('_user_changed_type_of_tracking', {"member": member, "state": after})
                await self.event_manager.publish('_any_voice_state_update', {"member": member})
                return

            if cnd.userLeftChannel(after):
                # LATER: make the message function
                await self.event_manager.publish('_user_left_tracking_channel', {"member": member})
                await self.event_manager.publish('_any_voice_state_update', {"member": member})
                return

            if cnd.userChangedChannel(before, after):
                # LATER: make the message function
                await self.event_manager.publish('_user_changed_tracking_channel', {"member": member, "state": after})
                await self.event_manager.publish('_any_voice_state_update', {"member": member})
        except Exception as e:
            print(e)

    def excluding_condition_is_met(self, before, after, member):
        if cnd.is_mute_or_deafen_update(before, after):
            return True
        if member.bot:
            return True
        return False



