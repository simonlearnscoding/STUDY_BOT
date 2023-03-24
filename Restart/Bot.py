# THE BASIC BOT SETUP
import asyncio

from settings_switch import client, token

# Load the cogs
extensions = ["cogs.feature_idea1", "cogs.feature_idea2", "cogs.slashTemplate"]


async def main():
    async with client:
        for ext in extensions:
            await client.load_extension(ext)
        loop = asyncio.get_event_loop()

        await loop.run_until_complete(await client.start(token))


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

    # UNCOMMENT THIS WHEN YOU CREATED A NEW SLASH COMMAND
    # THEN ONCE YOU'VE SYNCED THE NEW SLASH COMMAND YOU CAN RECOMMENT THIS LINE
    #await client.tree.sync()


asyncio.run(main())
