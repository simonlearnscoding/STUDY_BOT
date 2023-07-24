from collections import defaultdict
from copy import deepcopy
from utils.time import time_difference
from setup.bot_instance import bot
from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager
from spqrapp.models import *
from django.db.models import Q
from modules.leaderboard_interface.filter_strategy_pattern import FilterManager
from modules.leaderboard_interface.image_refactored_20_6 import ImageCreator

class DatasetManager(LifeCycleManager):
    def __init__(self):
        self.instance_class = Dataset
        super().__init__()
        self.image = ImageCreator()
        self.filter_manager = FilterManager()

    async def _bot_ready(self, bot):
        pass
        #TODO: uncomment when Im done here
        # for pattern in self.filter_manager.filter_patterns:
        #     await super().create(key=pattern, data=pattern)




class utils:
    def initialize_user_segments(self):
        # Initialize a dictionary with 96 keys each corresponding to a 15 minute segment of the day
        user_segments = {i: 0 for i in range(96)}
        return user_segments

    def get_segment_index(self, joinedAt):
        # Get the hour and minute from the "joinedAt" attribute and convert it to the 15 minute segment index
        hour = joinedAt.hour
        minute = joinedAt.minute
        segment_index = hour * 4 + minute // 15
        return segment_index

    def add_duration_to_segments(self, user_segments, segment_index, duration):
        # Add the duration to the appropriate segments
        remaining_duration = duration

        while remaining_duration > 0:
            # Calculate how much time is left in the current segment
            time_left_in_segment = 900 - user_segments[segment_index]

            if remaining_duration <= time_left_in_segment:
                # If the remaining duration fits in the current segment, add it and break the loop
                user_segments[segment_index] += remaining_duration
                break
            else:
                # If the remaining duration does not fit in the current segment, fill up the current segment
                # and continue with the next one
                user_segments[segment_index] += time_left_in_segment
                remaining_duration -= time_left_in_segment
                segment_index = (segment_index + 1) % 96

        return user_segments

    def calculate_segment_percentage(self, user_segments):
        # Calculate how many percent of time have been filled in each segment
        segment_percentages = {i: round(value / 900 * 100, 2) for i, value in user_segments.items()}
        return segment_percentages

    async def sum_and_format(self, input_array):
        # Initialize dictionaries to store user-related data
        user_data = {}

        # First loop: process all logs in the input array
        for log in input_array:
            user_id = log.user_id
            duration = log.duration
            user_nick = log.nick if log.nick else f"User {user_id}"

            if user_id not in user_data:
                user_data[user_id] = {
                    "nick": user_nick,
                    "durations": 0,
                    "status": False,
                    "logs": [],
                    "segments": self.initialize_user_segments(),
                    "hours": 0,
                    "minutes": 0,
                    "seconds": 0,
                    "avatar": None,
                    "online": False
                }

            user_data[user_id]["durations"] += duration
            user_data[user_id]["status"] = log.status == "ONGOING"
            user_data[user_id]["logs"].append({"joinedAt": log.joined_at, "duration": duration})

            if self.timeframe == 'today':
                segment_index = self.get_segment_index(log.joined_at)
                user_data[user_id]["segments"] = self.add_duration_to_segments(user_data[user_id]["segments"],
                                                                               segment_index, log.duration)
            print(f'{user_nick} : duration: {user_data[user_id]["durations"]}')

        # Second loop: compile data for each user
        for user_id, user_info in user_data.items():
            user_info["avatar"] = await self.get_avatar_url(user_id)
            user_info["online"] = user_info["status"]
            hours, remainder = divmod(user_info["durations"], 3600)
            minutes, seconds = divmod(remainder, 60)
            user_info["hours"] = hours
            user_info["minutes"] = minutes
            user_info["seconds"] = seconds

            if self.timeframe == 'today':
                user_info["segments"] = self.calculate_segment_percentage(user_info["segments"])

        # Sort the user_data dictionary by duration in descending order
        sorted_output_array = sorted(
            user_data.values(),
            key=lambda x: (x["hours"], x["minutes"], x["seconds"]),
            reverse=True,
        )[:10]
        for user in sorted_output_array:
            print(user['nick'], user['minutes'])
        return sorted_output_array
    # async def sum_and_format(self, input_array):
    #     # Chek if the data is just for today
    #     user_durations = defaultdict(int)
    #     user_status = defaultdict(bool)  # dictionary to track user status
    #     user_nicknames = {}  # dictionary to store user nicknames
    #     user_logs = defaultdict(list)  # New dictionary to store user logs
    #     user_segments = defaultdict(self.initialize_user_segments)  # New dictionary to store user segments
    #
    #
    #     for log in input_array:
    #         temp_users = {}
    #         user_id = log.user_id
    #         duration = log.duration
    #         if log.nick is not None:
    #             user_nick = log.nick
    #         else:
    #             user_nick = f"User {user_id}"
    #
    #         user_durations[user_id] += duration
    #         user_nicknames[user_id] = user_nick  # Store the user_nick
    #         if log.status == "ONGOING":
    #             user_status[user_id] = True
    #
    #         # Use the boolean variable for the check
    #         if self.timeframe == 'today':
    #             segment_index = self.get_segment_index(log.joined_at)
    #             user_segments[user_id] = self.add_duration_to_segments(user_segments[user_id], segment_index,
    #                                                                    log.duration)
    #         user_logs[user_id].append({"joinedAt": log.joined_at, "duration": duration})
    #         print(f'{log.nick} : duration: {user_durations[user_id]}')
    #     output_array = []
    #     for user in user_durations.keys():
    #         online = user_status[user_id]
    #         user_nick = user_nicknames[user_id]
    #         avatar_url = await self.get_avatar_url(user_id)
    #         # Convert duration to hours, minutes, and seconds
    #         hours, remainder = divmod(duration, 3600)
    #         minutes, seconds = divmod(remainder, 60)
    #         segments = self.calculate_segment_percentage(user_segments[user_id]) if self.timeframe == 'today' else []
    #         output_array.append(
    #             {
    #                 "nick": user_nick,
    #                 "hours": hours,
    #                 "minutes": minutes,
    #                 "seconds": seconds,
    #                 "online": online,
    #                 "avatar": avatar_url,
    #                 "user_logs": user_logs[user_id],
    #                 "segments": segments
    #             }
    #         )
    #
    #     # Sort the output_array by duration in descending order
    #     sorted_output_array = sorted(
    #         output_array,
    #         key=lambda x: (x["hours"], x["minutes"], x["seconds"]),
    #         reverse=True,
    #     )[:10]
    #     print(sorted_output_array)
    #     return sorted_output_array

    async def get_avatar_url(self, member_id):
        guild = bot.get_guild(789814373434654731) #TODO: refactor: guild should probably just be fetched once
        member = guild.get_member(member_id)

        # Get the avatar URL
        avatar_url = str(member.display_avatar)
        return avatar_url
    def calculate_duration(self, entry):
        new_duration = time_difference(entry.joined_at)
        setattr(entry, "duration", new_duration)
        return entry

    def get_active_with_duration(self, ongoing):
        ongoing_arr = []
        for entry in ongoing:
            ongoing_arr.append(self.calculate_duration(entry))
        return ongoing_arr

    async def calculate_update(self):
        all_entries = self.complete + self.get_active_with_duration(self.ongoing)
        return await self.sum_and_format(all_entries)




class Dataset(utils):
    def __init__(self, filter_name, manager):
        self.manager = manager
        self.name = "dataset"
        # self.filter = data.manager.instances
        self.image = self.manager.image
        self.filter_manager = self.manager.filter_manager
        self.filter_pattern = self.manager.filter_manager.filter_patterns[filter_name]
        self.event_manager = self.manager.event_manager
        self.key = filter_name
        self.lb_instances = {}
        self.timeframe = self.filter_pattern['date_range']

    """ 
    I had to find a tradeoff between fast reactivity
    and not creating an unneccessary amount of images
    so every view will by default be updated every
    15 minutes.

    when a user is currently viewing one of the views it will be updated
    every minute
    """
    async def _one_minute_passed(self, time):
        if len(self.lb_instances) > 0:
            await self.update_dataset()
            print(f'updated {self.key}')
        else:
            print('no one here')
    async def _fifteen_minutes_passed(self, time):
        if len(self.lb_instances) == 0:
            await self.update_dataset()
        else:
            print('already updated')

    async def create(self, data):
        await self.update_dataset()

    """
    the difference between update_active and
    update_dataset is that update_dataset 
    also fetches the data again
    """
    async def update_dataset(self):
        print(self.lb_instances)
        await self.get_data()
        self.data = await self.calculate_update()
        self.image_url = await self.image.create_image(self.data, self.timeframe)
        await self.manager.event_manager.publish("_updated_image", self)


    async def update_active_entries_timing(self):
        self.data = await self.calculate_update()
        self.image_url = await self.image.create_image(self.data, self.timeframe)
        await self.manager.event_manager.publish("_updated_image", self)


    async def get_data(self):

        """
        I have to wrap the fetches into a sync_to_async because
        Django does not support async operations
        """
        try:
            self.ongoing, self.complete = await self.manager.filter_manager.get_data(self)
        except Exception as e:
            print(e)




