from discord.ext import commands, tasks
from tortoise_models import Channel
from utils.error_handler import class_error_handler
from bases.event_manager_base import event_manager_baseclass
from event_handlers.channel_event_handler import channel_event_handler
from event_emitters.channel_event_emitter import channel_event_emitter



async def setup(bot):
    await bot.add_cog(on_minute_passed_cog(bot))

@class_error_handler
class on_minute_passed_cog(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
        self.minute_task.start()  # Start the minute task when the cog is loaded


    @tasks.loop(seconds=1)
    async def minute_task(self):
        leaderboard_channels = await Channel.filter(channel_type='Leaderboard').all()
        for channel in leaderboard_channels:
            channel = self.bot.get_channel(channel.discord_id)
            if channel:
                print(channel)

    @minute_task.before_loop
    async def before_minute_task(self):
        await self.bot.wait_until_ready()  # Wait until the bot is ready before starting the task

    # ... (rest of your existing event listeners)

# Example usage in your bot setup
# bot = commands.Bot(command_prefix="!")
# bot.run('YOUR_BOT_TOKEN')
