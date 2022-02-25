import discord

from discord.ext import commands, tasks
from discord.channel import VoiceChannel
from discord.client import Client
from giphy_client.rest import ApiException

from cogs import tracking
from mydb import db
from cogs.goals import goals
import cogs.timer
from User import user, userfunction
from cogs.challenge import challenge
from cogs.update import update
from vc import vc

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "*", intents = intents)

extensions = ["cogs.boot", "cogs.goals", "cogs.tracking", "cogs.timer", "User", "cogs.update", "cogs.tasks", "cogs.levels", "cogs.challenge"]
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
    #db.drop_tables()
    await userfunction.ResetUsers(client)
    guild = client.get_guild(vc.guild_id)
    await tracking.tracking.reboot2(client, guild)
    checkem.start(client)
    checkupdate.start(client)
    checkchallenge.start(client)
    checkrank.start(client)
    await goals.ranking(client)


@tasks.loop(seconds=40)
async def checkupdate(client):
    await update.update(client)

@tasks.loop(seconds=40)
async def checkchallenge(client):
    await challenge.checktimes(client)

@tasks.loop(seconds=10) #change the intervall here
async def checkem(client):
    await goals.check_goals(client)

@tasks.loop(seconds=30) #change the intervall here
async def checkrank(client):
    RankList = await goals.ranking(client)
    await goals.displayranking(client, RankList[0], RankList[1])
    print(RankList)







client.run("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk")