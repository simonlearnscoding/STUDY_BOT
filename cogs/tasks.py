import discord
from mydb import db
from discord.ext import commands
# THE OTHER PY FILES
import User
from vc import vc
from cogs.boot import boot

import re
import discord
import asyncio
from cogs.levels import levels

    # From now, `custom_emojis` is `list` of `discord.Emoji` that `msg` contains.
# client.load_extension("cogs.boot")

class tasks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.channel.id == vc.tasks_id:
            beforeDone = before.content.count("✅")
            beforeUndone = before.content.count("🔳")
            afterDone = after.content.count("✅")
            afterUndone = after.content.count("🔳")
            if ((beforeDone < afterDone) and (afterUndone == 0) and (beforeUndone > 0)):
                Embed = discord.Embed()
                xp = 50
                Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
                Embed.add_field(name=f"{after.author.name},Completed everything today!!",
                                value=f"+ {xp}xp",
                                inline=False)
                message = await after.channel.send(embed=Embed)

                await asyncio.sleep(1)
                await message.delete()
                # add xp
                await levels.addXP(self.client, after.author, xp)


            elif beforeDone < afterDone:
                print("New Tast Completed!")
                Embed = discord.Embed()
                xp = 10
                Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
                Embed.add_field(name=f"{after.author.name},Completed a Task!",
                                value=f"+ {xp}xp",
                                inline=False)
                message = await after.channel.send(embed=Embed)

                await asyncio.sleep(1)
                await message.delete()
                # add xp
                await levels.addXP(self.client, after.author, xp)









def setup(client):
    client.add_cog(tasks(client))