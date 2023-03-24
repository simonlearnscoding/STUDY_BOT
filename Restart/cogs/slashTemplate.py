import discord
from discord import app_commands
from discord.ext import commands
from vc import client, server


class GreetCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(description="Shows the server rules")
    async def rules(self, interaction: discord.Interaction) -> None:
        ...  # Here can be the same code that the slash command outside cog
        rules = (
            "1. Don't say bad words",
            "2. Respect other people",
            "3. You mustn't speak loud in voice channels",
        )

        await interaction.response.send_message(f"{rules}")


#     @slash.slash#


async def setup(client):
    await client.add_cog(GreetCog(client))
