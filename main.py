import asyncio

import discord
from cogs.goals import goals
from cogs.trackingsessions import timeTrack, trackings
from cogs.updateNew import updateNew
from cogs.User import userfunction
from cogs.vc import vc
from discord import app_commands
from discord.ext import commands, tasks

extensions = [
    "cogs.boot",
    "cogs.vcroles",
    "cogs.slashcommands",
    "cogs.goals",
    "cogs.timer",
    "cogs.User",
    "cogs.levels",
    "cogs.heatmap",
    "cogs.challenge",
    "cogs.trackingsessions",
    "cogs.vc",
    "cogs.updateNew",
    "cogs.tasks",
    "cogs.questions",
]

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="~", intents=intents)
application_id = 839089655189864508


async def main():
    async with client:
        for ext in extensions:
            await client.load_extension(ext)
        loop = asyncio.get_event_loop()

        await loop.run_until_complete(
            await client.start(
                "ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk"
            )
        )


@client.event
async def on_ready():
    print("bot ready")

    vc.start(client, False)  # set to true if you are testing
    await client.tree.sync(guild=discord.Object(id=vc.guild_id))
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


@tasks.loop(seconds=20)
async def checkem(client):
    await goals.check_goals(client)


@tasks.loop(seconds=20)  # change the intervall here
async def checkrank(client):
    RankList = await goals.ranking(client)
    await goals.displayranking(client, RankList[0], RankList[1])


asyncio.run(main())
