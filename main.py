# THE BASIC BOT SETUP
import os
import sys
from setup.bot_instance import bot, token
from bases.event_manager import event_manager
import asyncio
import django
# from Cogs.time_passed import TimeEvents
# Load the cogs
# from modules.session_tracking.sessioneventhandler import session_to_database
# from spqrapp.models import *
# from modules.session_tracking.database_queries import queriess as db
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

django.setup()
print(sys.executable)
extensions = [
    "Cogs.session_tracking",
    "Cogs.time_events",
    "Cogs.menu"
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
    bot.ready = True
    # await ActivityLog.object.delete_all()
    # await Session.object.delete_all()
    await event_manager.publish("_bot_ready", bot)
    # channel = bot.get_channel(int(834144065133740102))


asyncio.run(main())
