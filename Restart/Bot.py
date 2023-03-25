# THE BASIC BOT SETUP
import asyncio

from settings_switch import bot, token

import discord

# Load the cogs
extensions = [
    "cogs.feature_idea1",
    "cogs.feature_idea2",
    "cogs.slashTemplate",
    "cogs.database_connect",
    "cogs.TimeTracking.timeTracking",
]


async def main():
    async with bot:
        for ext in extensions:
            await bot.load_extension(ext)
        loop = asyncio.get_event_loop()
        await loop.run_until_complete(await bot.start(token))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    # UNCOMMENT THIS WHEN YOU CREATED A NEW SLASH COMMAND
    # THEN ONCE YOU'VE SYNCED THE NEW SLASH COMMAND YOU CAN RECOMMENT THIS LINE
    # await client.tree.sync()


asyncio.run(main())
