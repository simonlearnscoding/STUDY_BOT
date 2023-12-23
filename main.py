"""
This is the main file for python
"""
import asyncio

from setup.bot_instance import bot, token
# TODO: reactivate that cog
extensions = [
    "Cogs.on_ready_cog",
    # "Cogs.channel_cog",
]


async def main():
    if token is None:
        print("Token is not set. Exiting.")
        return
    async with bot:
        for ext in extensions:
            await bot.load_extension(ext)
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
