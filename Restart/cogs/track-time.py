from settings_switch import bot

import discord
from discord.ext import commands


# RENAME MYCOG TO NAME OF THE MODULE
class trackTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # YOUR CODE GOES HERE


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(trackTime(bot))


async def teardown(bot):
    return
