import discord
from discord.ext import commands, tasks
from discord.channel import VoiceChannel
from discord.client import Client
from giphy_client.rest import ApiException



from mydb import db
from cogs.goals import goals
import cogs.timer
from User import user, userfunction
from User import User
from cogs.update import update

intents = discord.Intents.default()
intents.members = True
client = discord.Client()
client = commands.Bot(command_prefix = "*", intents=intents)
channel = None

extensions = ["cogs.boot", "cogs.goals", "cogs.tracking", "cogs.timer", "User", "cogs.update"]
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
    db.drop_tables()
    checkem.start()
    await userfunction.ResetUsers(client)
    checkupdate.start(client)

@tasks.loop(seconds=1)
async def checkupdate(client):
    await update.update(client)

@tasks.loop(seconds=60) #change the intervall here
async def checkem():
    await goals.check_goals()




client.run("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.bxsDVuswWQeZqzuS0cNYgcHDqV0")