import discord
from discord import app_commands
from discord.ext import commands
from vc import bot, server


class GreetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="associate a VC with an activity")  # "**_server rules_**" ** = bold, _=italicized
    async def associate(self, interaction: discord.Interaction) -> None:
        ...  # Here can be the same code that the slash command outside cog
        rules = (
            "1. Don't say bad words",
            "2. Respect other people",
            "3. You mustn't speak loud in voice channels",
        )
        rules_str = "\n".join(rules)  # Combine the rules into a single string with a new line character separating them
        await interaction.response.send_message(f"**Here are the rules:**\n{rules_str}")



async def setup(bot):
    await bot.add_cog(GreetCog(bot))
