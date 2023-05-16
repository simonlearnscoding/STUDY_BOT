from collections import defaultdict, namedtuple
from datetime import datetime, time, timedelta, timezone

import pytz
import requests
from Database import queries as db
from Settings.main_settings import bot
from utils.time import get_start_end, time_difference

import cogs.TimeTracking.activities as act
import discord
from cogs.leaderboard.formatting import *
from cogs.leaderboard.interface import *
from discord import Embed
from discord.ext import commands, tasks


class leaderboard_update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_leaderboard_image_regularly.start()
        # create self.filter = instantiate the filter

    @tasks.loop(seconds=50.0)
    async def update_leaderboard_image_regularly(self):
        # TODO THIS IS THE MAIN FUNCTION
        # IT NEEDS TO BE DECOUPLED FROM THE UPDATE REGULARLY TASK
        # BECAUSE I HAVE TO CALL THIS FUNCTION FROM THE VC EVENTS TOO
        # IT BELONGS INTO THE LEADERBOARD CLASS

        print("passing the update function for now")
        # try:
        #     filter = next(filter_cycle)
        #     arr = await get_data(filter)
        #     img = create_leaderboard_image(arr)
        #     await update_image(self, img)
        # except Exception as e:
        #     print(e)
        #     print("Task failed")

    @update_leaderboard_image_regularly.before_loop
    async def before_my_background_task(self):
        await self.bot.wait_until_ready()


async def get_data(filter):
    arr = await db.get_entries_within_range(filter)
    arr = sum_durations(arr)
    return arr


async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(leaderboard_update(bot))


# the filter holds the state
def cog_unload(self):
    self.my_background_task.cancel()
