from Cogs.time_passed import TimeEvents
from discord.ext import commands


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(time_events(bot))


class time_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_events = TimeEvents()
        self.bot.loop.create_task(
            self.run_time_events()
        )  # Use the bot's event loop to run your task

    async def run_time_events(self):
        while True:
            await self.time_events.functions_to_run()
