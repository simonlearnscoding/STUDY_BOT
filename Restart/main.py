# THE BASIC BOT SETUP
import asyncio
import sys
from modules.session_tracking.session_to_database import session_to_database
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

    # REMOVE THIS WHEN Im DONE TESTING
    # await db.delete_all_sessions()
    # await db.delete_all_activities()
    # prisma = await database_queries.create()
    # db = LogOperations(prisma)  # Set the 'db' instance as an attribute of the 'bot'
    # UNCOMMENT THIS WHEN YOU CREATED A NEW SLASH COMMAND
    # THEN ONCE YOU'VE SYNCED THE NEW SLASH COMMAND YOU CAN RECOMMENT THIS LINE
    # await client.tree.sync()


asyncio.run(main())
