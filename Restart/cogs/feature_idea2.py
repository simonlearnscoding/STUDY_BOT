import discord
from discord.ext import commands
from vc import server

# RENAME MYCOG TO NAME OF THE MODULE
class TestFeature2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # on message event if message channel is generalText reply with hi
    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore messages from the bot
        if message.author == self.client.user:
            return

        #  print yo if the message was written in generalText
        #if message.channel == server.getChannel("botspamText"):
        if message.channel == server.getChannel("vc_chat") and message.content == "!hello":
            # reply with hi
            await message.channel.send("Hello from feature two")


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(TestFeature2(bot))


async def teardown(bot):
    return
