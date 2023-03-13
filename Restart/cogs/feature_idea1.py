import discord
from discord.ext import commands
from vc import server


# RENAME MYCOG TO NAME OF THE MODULE
class TestFeature(commands.Cog):
    def __init__(self, client):
        self.client = client

        # on message event if message channel is generalText reply with hi
        @client.event
        async def on_message(message):
            # ignore messages from the bot
            if message.author == client.user:
                return

            #  print yo if the message was written in generalText
            if message.channel == server.getChannel("generalText"):
                # reply with hi
                await message.channel.send("hi from derks new feature")


async def setup(client):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await client.add_cog(TestFeature(client))


async def teardown(client):
    return
