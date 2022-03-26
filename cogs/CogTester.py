import asyncio

import discord

from discord.ext import commands, tasks
from cogs.trackingsessions import trackings, timeTrack

from cogs.vc import vc
from cogs.updateNew import updateNew
from cogs.goals import goals

extensions = ["cogs.boot", "cogs.goals", "cogs.timer", "User", "cogs.levels", "cogs.heatmap", "cogs.challenge", "cogs.trackingsessions", "cogs.vc", "cogs.updateNew", "cogs.tasks"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "~", intents = intents)


async def main():
    async with client:
        for ext in extensions:
            await client.load_extension(ext)
        await client.start("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk")

asyncio.run(main())


@client.event
async def on_ready():
    vc.start(client, False)
    print("bot ready")
    await timeTrack.totalReboot(client)
    checkupdate.start(client)
    checkrank.start(client)
    checkem.start(client)
    await goals.ranking(client)

@tasks.loop(seconds=40)
async def checkupdate(client):
    await updateNew.update(client)

@tasks.loop(seconds=40) #TODO: change the intervall here
async def checkem(client):
    await goals.check_goals(client)

@tasks.loop(seconds=20) #change the intervall here
async def checkrank(client):
    RankList = await goals.ranking(client)
    await goals.displayranking(client, RankList[0], RankList[1])
