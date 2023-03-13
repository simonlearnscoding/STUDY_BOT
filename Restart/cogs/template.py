from discord.ext import commands
import discord


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
