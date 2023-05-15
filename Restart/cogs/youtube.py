# LATER: here I will probably write (steal lol) a function that takes a youtube URL and plays that sound in the vc
import discord
from discord.ext import commands


# RENAME MYCOG TO NAME OF THE MODULE
class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

        # YOUR CODE GOES HERE


async def setup(client):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await client.add_cog(MyCog(client))


async def teardown(client):
    return
