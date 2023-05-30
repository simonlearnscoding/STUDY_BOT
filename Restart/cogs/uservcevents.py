import modules.TimeTracking.utils.Conditionals as cnd
from discord.ext import commands


# from Settings.main_settings import bot

async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(user_vc_events(bot))

class user_vc_events(commands.Cog):
    def __init__(self, bot, event_manager):
        super().__init__()
        self.bot = bot
        self.event_manager = event_manager

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.excluding_condition_is_met(before, after, member):
            return
        await self.event_manager.publish('any_voice_state_update', {"member": member, "before": before, "after": after})

        if cnd.user_joins_tracking_channel(before, after):
            print(f"{member.name} joined channel")
            self.event_manager.publish('user_joins_tracking_channel', {"member": member, "state": after})
            return

        if cnd.user_changed_type_of_tracking(before, after):
            print(f"{member.name} changed activity type")
            self.event_manager.publish('user_changed_type_of_tracking', {"member": member, "state": after})
            return

        if cnd.userLeftChannel(after):
            # LATER: make the message function
            print(f"{member.name} left channel")
            self.event_manager.publish('user_left_tracking_channel', member)
            return

        if cnd.userChangedChannel(before, after):
            # LATER: make the message function
            print("user changed channel")
            self.event_manager.publish('user_changed_tracking_channel', {"member": member, "state": after})

    def excluding_condition_is_met(self, before, after, member):
        if cnd.is_mute_or_deafen_update(before, after):
            return True
        if member.bot:
            return True
        return False



async def teardown(bot):
    return
