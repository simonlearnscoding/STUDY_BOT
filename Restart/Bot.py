
token = "ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk"

import discord
import asyncio
from discord.ext import commands



intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="~", intents=intents)
application_id = 839089655189864508

# Load the cogs
extensions = [
    'cogs.test'
    ]

async def main():
    async with client:
        for ext in extensions:
            await client.load_extension(ext)
        loop = asyncio.get_event_loop()

        await loop.run_until_complete(
            await client.start(
token            )
        )


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")


asyncio.run(main())
