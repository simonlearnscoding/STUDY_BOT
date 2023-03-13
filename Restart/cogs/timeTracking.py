# TODO: Here I will create the functions that track every time a user joins a voice channel and leaves a voice channel
# AND LOG ONE OF THE FOLLOWING FOR STATES: 1. no cam and no ss, 2. no cam and ss, 3. cam and no ss, 4. cam and ss

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
