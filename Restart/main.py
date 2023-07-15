# THE BASIC BOT SETUP
import asyncio
import sys
import os
# import modules.leaderboard_interface
print(os.getcwd())
# from modules.session_tracking.session_to_database import session_to_database
# from modules.session_tracking.database_queries import queriess as db
print(sys.executable)
from setup.bot_instance import bot, token
from bases.event_manager import event_manager
from Cogs.time_passed import TimeEvents
# Load the cogs
extensions = [
    "Cogs.session_tracking",
    "Cogs.time_events",
    "Cogs.menu"
]


async def main():
    async with bot:
        for ext in extensions:
            await bot.load_extension(ext)
        #await db.delete_all_activities()
        #await db.delete_all_sessions()
        loop = asyncio.get_event_loop()
        await loop.run_until_complete(await bot.start(token))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    bot.ready = True

    await event_manager.publish("_bot_ready", bot)
    channel = bot.get_channel(int(834144065133740102))






asyncio.run(main())
