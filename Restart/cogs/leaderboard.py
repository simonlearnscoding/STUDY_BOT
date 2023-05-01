from datetime import datetime, timezone, time, timedelta
from collections import namedtuple
from utils.time import time_difference
from Database import queries as db
import pytz
import cogs.TimeTracking.activities as act
import discord
from discord.ext import commands
from collections import defaultdict


import discord
from discord.ext import commands, tasks


# RENAME MYCOG TO NAME OF THE MODULE
class leaderboard(commands.Cog):
    def __init__(self, bot):
        self.my_background_task.start()
        self.bot = bot
        
    # YOUR CODE GOES HERE

    def cog_unload(self):
        self.my_background_task.cancel()

    @tasks.loop(seconds=5.0)
    async def my_background_task(self):
        pass
        # RUN THE TASK HERE
        # print("Task running every 10 seconds")
        arr = await get_today()
        formatted = sum_durations(arr)
        print(formatted)


    @my_background_task.before_loop
    async def before_my_background_task(self):
        await self.bot.wait_until_ready()



async def setup(bot):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await bot.add_cog(leaderboard(bot))
    


async def get_today():
    # GET COMPLETED
    date_range = get_start_end_today()
    entries = await get_entries_within_range(date_range, "MEDITATION", "SS")
    UserArr = []
    for entry in entries:
        UserArr.append(entry)
    return UserArr
    # YOU ARE HERE, CREATE THE DATA



def sum_durations(input_array):
    user_durations = defaultdict(int)
    user_status = defaultdict(bool) # dictionary to track user status
    for log in input_array:
        user_id = log.userId
        duration = log.duration
        if log.nick is not None:
            user_nick = log.nick
        else:
            user_nick = f"User {user_id}"
        user_durations[user_id] += duration
        if log.status == "ONGOING":
            user_status[user_id] = True
    output_array = []
    for user_id, duration in user_durations.items():
        online = user_status[user_id]
        output_array.append({"nick": user_nick, "duration": duration, "online": online})
    return output_array


# nick = next((log.nick for log in input_array if log.userId == user_id and log.nick is not None), f"User {user_id}")




def get_start_end_today():
    gmt_plus_one = pytz.timezone("Etc/GMT-1")
    now = datetime.now(gmt_plus_one)

    start_of_today = datetime.combine(now.date(), time(0, 0, tzinfo=gmt_plus_one))
    end_of_today = start_of_today + timedelta(days=1)

    return {
        "start": start_of_today,
        "end": end_of_today
    }


async def get_sum_duration_by_user():
    results = await create_query(
        "find_many",
        "ActivityLog",
    )
    return results

async def get_entries_within_range(date_range, activity, typeOfActivity):
    where = {
        'AND' : [
            {"status": "COMPLETED"},
            {
                "joinedAt": {
                    "gte": date_range["start"],
                    "lt": date_range["end"]
                },
            },
            {"activity": activity},
            {"activityType": typeOfActivity}
        ]

    } #SEEMS TO WORK
    completed = await db.create_query(
        "activitylog",
        "find_many",
        where=where,
    )
    
    where = {
            'AND' : [
                {"status": "ONGOING"},
                {"activity": activity},
                {"activityType": typeOfActivity}
                ]}
            
    ongoing = await db.create_query(
        "activitylog",
        "find_many",
        where=where,
    )

    ongoingArr = []
    for entry in ongoing:
        ongoingArr.append(calculate_duration(entry))

    entries = completed + ongoingArr
    return entries

def calculate_duration(entry):
    new_duration = time_difference(entry.joinedAt)
    print(new_duration)
    print(entry)
    setattr(entry, 'duration', new_duration)
    print(entry)
    return entry
# get all user id's in an array
# for every id in the array:
## call that function (limit it to id
# get discord nick to user name (from another table)
# 
#
#
