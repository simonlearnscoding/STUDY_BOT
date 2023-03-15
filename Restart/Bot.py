# THE BASIC BOT SETUP
import asyncio

from settings_switch import client, token

# Load the cogs
extensions = ["cogs.test", "cogs.feature_idea1"]


async def main():
    async with client:
        for ext in extensions:
            await client.load_extension(ext)
        loop = asyncio.get_event_loop()

        await loop.run_until_complete(await client.start(token))

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

asyncio.run(main())
