from settings_switch import bot, db

import discord
from discord.ext import commands


# RENAME MYCOG TO NAME OF THE MODULE
class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # YOUR CODE GOES HERE


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(MyCog(bot))


async def teardown(bot):
    return
