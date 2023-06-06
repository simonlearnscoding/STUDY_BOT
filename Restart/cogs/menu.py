from cogs.time_passed import TimeEvents
from discord.ext import commands
import discord
async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(menu(bot))

class menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#     @commands.command()
#     async def Menu(self):
#         view = menu()
#         await self.reply(view=view)
#
# await button().send_message()