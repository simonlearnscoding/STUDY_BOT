import discord
from discord import channel
from discord.ext import commands
from vc import server


# RENAME MYCOG TO NAME OF THE MODULE
class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

        # YOUR CODE GOES HERE
        # on message event if message channel is generalText reply with hi
        @client.event
        async def on_message(message):
            # ignore messages from the bot
            if message.author == client.user:
                return

            #  print yo if the message was written in generalText
            if message.channel == server.getChannel("generalText"):
                print("yo")


async def setup(client):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await client.add_cog(MyCog(client))


async def teardown(client):
    return
