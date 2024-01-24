"""
This is the main file for python
"""
import asyncio

from setup.bot_instance import bot, token
# TODO: reactivate that cod
extensions = [
    "Cogs.on_ready_cog",
    "Cogs.channel_cog",
    "Cogs.on_minute_passed_cog",
    "Cogs.vc_events_cog",
    "event_emitters.server_event_emitter",
    "slash_commands.associate_activity"
]


async def main():
    if token is None:
        print("Token is not set. Exiting.")
        return  # Exit the function or raise an error
    async with bot:
        for ext in extensions:
            await bot.load_extension(ext)
        # Directly await the bot.start coroutine
        await bot.start(token)


# To run the main coroutine in a synchronous context
if __name__ == "__main__":
    asyncio.run(main())
