

import discord
from discord.ext import commands
from vc import server


# RENAME MYCOG TO NAME OF THE MODULE
class DataBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # on message event if message channel is generalText reply with hi


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(DataBase(bot))


async def teardown(bot):
    return
