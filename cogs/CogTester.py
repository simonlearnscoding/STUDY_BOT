import asyncio

import discord

from discord.ext import commands, tasks
from cogs.trackingsessions import trackings, timeTrack
from cogs.User import userfunction
from cogs.vc import vc
from cogs.updateNew import updateNew
from cogs.goals import goals

extensions = ["cogs.boot", "cogs.goals", "cogs.timer", "cogs.User", "cogs.levels", "cogs.heatmap", "cogs.challenge", "cogs.trackingsessions", "cogs.vc", "cogs.updateNew", "cogs.tasks", "cogs.questions"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "~", intents = intents)

async def main():

    async with client:
        for ext in extensions:
            await client.load_extension(ext)
        loop = asyncio.get_event_loop()
        await loop.run_until_complete(await client.start("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk"))



@client.event
async def on_ready():
    print("bot ready")
    vc.start(client, False)
    for member in vc.guild.members:
        await userfunction.GetUser(client, member)
    await timeTrack.totalReboot(client)
    checkupdate.start(client)
    checkrank.start(client)
    checkem.start(client)
    await goals.ranking(client)


@tasks.loop(seconds=40)
async def checkupdate(client):
    await updateNew.update(client)

@tasks.loop(seconds=20) #TODO: change the intervall here
async def checkem(client):
    await goals.check_goals(client)

@tasks.loop(seconds=20) #change the intervall here
async def checkrank(client):
    RankList = await goals.ranking(client)
    await goals.displayranking(client, RankList[0], RankList[1])

asyncio.run(main())