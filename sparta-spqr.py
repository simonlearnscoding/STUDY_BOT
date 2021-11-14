import discord
from discord import commands
from discord.channel import VoiceChannel
from discord.client import Client
from giphy_client.rest import ApiException


import mydb
from mydb import db
import cogs.goals
import cogs.timer
import User
from User import user

intents = discord.Intents.default()
intents.members = True
client = discord.Client()
client = commands.Bot(command_prefix = "*", intents=intents)
channel = None

extensions = ["cogs.boot", "cogs.goals", "cogs.tracking", "cogs.timer", "cogs.user"]
if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)
        
# STARTING EVENT
@client.event
async def on_ready():
    #TODO Switch with timer inbreak
    cogs.timer.InBreak = False
    print("bot is ready.")#
    #await runschedule()
   #making the tables and add every member
    cogs.goals.check_goals.start()
    db.drop_tables()
    await user.ResetUsers()

client.run("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.bxsDVuswWQeZqzuS0cNYgcHDqV0")