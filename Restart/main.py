# THE BASIC BOT SETUP
import asyncio
import sys
import modules.leaderboard_interface
from modules.session_tracking.session_to_database import session_to_database

from modules.session_tracking.database_queries import queriess as db
print(sys.executable)
from setup.bot_instance import bot, token

# Load the cogs
extensions = [
    "cogs.session_tracking",
    # "cogs.leaderboard.update_every_x_seconds",
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
    channel = bot.get_channel(int(834144065133740102))
    # REMOVE THIS WHEN Im DONE TESTING
    await db.delete_all_sessions()
    await db.delete_all_activities()





asyncio.run(main())
