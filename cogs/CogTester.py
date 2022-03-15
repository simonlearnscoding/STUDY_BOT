import discord

from discord.ext import commands, tasks
from cogs.trackingsessions import trackings, timeTrack

from cogs.vc import vc
from cogs.updateNew import updateNew
from cogs.goals import goals
import cogs.timer
from User import user, userfunction
from cogs.heatmap import heatmap

extensions = ["cogs.boot", "cogs.goals", "cogs.timer", "User", "cogs.levels", "cogs.heatmap", "cogs.challenge", "cogs.trackingsessions", "cogs.vc", "cogs.updateNew", "cogs.tasks"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "*", intents = intents)

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

@client.event
async def on_ready():
    vc.start(client, True)
    await timeTrack.totalReboot(client)
    checkupdate.start(client)
    checkrank.start(client)
    checkem.start(client)
    await goals.ranking(client)

@tasks.loop(seconds=40)
async def checkupdate(client):
    await updateNew.update(client)

@tasks.loop(seconds=30) #TODO: change the intervall here
async def checkem(client):
    await goals.check_goals(client)

@tasks.loop(seconds=30) #change the intervall here
async def checkrank(client):
    RankList = await goals.ranking(client)
    await goals.displayranking(client, RankList[0], RankList[1])
client.run("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk")