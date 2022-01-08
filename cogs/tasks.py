import discord
from mydb import db
from discord.ext import commands
# THE OTHER PY FILES
import User
from vc import vc
from cogs.boot import boot


# client.load_extension("cogs.boot")

class tasks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == vc.tasks_id:
            channel = self.client.get_channel(vc.tasks_id)
            print(f"{message.author.id} wrote in tasks channel")
            for x in User.Users:
                print(f"{x.id}")
                if x.id == message.author.id:
                    x.Tasks = message.content
                    print(f"{x.name} {x.Tasks}")


def setup(client):
    client.add_cog(tasks(client))