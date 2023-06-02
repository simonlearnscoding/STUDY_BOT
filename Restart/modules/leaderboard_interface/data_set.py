from utils.time import get_start_end
from collections import defaultdict
from bases.connector import create_query
from utils.time import time_difference
# from cogs.leaderboard.filter import Filter_Manager
from bases.state_manager import SingletonFactoryManager

from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager


class DatasetManager(LifeCycleManager):
    def __init__(self):
        self.instance_class = Dataset
        super().__init__()

    """
    this gets triggered when the first lb 
    instance of one filter 
    gets created
    """
    async def _created_instance_filter(self, data):
        """
        set filter name as key and create the object
        """
        key = data.filter
        await super().create(data, key)



class queries:
    async def get_active(self, filter):
        filter_copy = filter.copy()
        # TODO: check whats up with create query, is it accessible or not?
        filter_copy["AND"][0] = {"status": "ONGOING"}
        return await create_query(
            "activitylog",
            "find_many",
            where=filter_copy,
        )

    async def get_completed(self, filter):
        filter_copy = filter.copy()
        filter_copy["AND"][0] = {"status": "COMPLETED"}
        return await create_query(
            "activitylog",
            "find_many",
            where=filter_copy,
        )

class utils:
    def sum_and_format(self, input_array):
        user_durations = defaultdict(int)
        user_status = defaultdict(bool)  # dictionary to track user status
        user_nicknames = {}  # dictionary to store user nicknames
        #TODO: I should probably add an array of join time an length for later reference to do cool stuff
        for log in input_array:
            user_id = log.userId
            duration = log.duration
            if log.nick is not None:
                user_nick = log.nick
            else:
                user_nick = f"User {user_id}"

            user_durations[user_id] += duration
            user_nicknames[user_id] = user_nick  # Store the user_nick
            if log.status == "ONGOING":
                user_status[user_id] = True

        output_array = []
        for user_id, duration in user_durations.items():
            online = user_status[user_id]

            # Get the user_nick from the user_nicknames dictionary
            user_nick = user_nicknames[user_id]

            # Convert duration to hours, minutes, and seconds
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)

            output_array.append(
                {
                    "nick": user_nick,
                    "hours": hours,
                    "minutes": minutes,
                    "seconds": seconds,
                    "online": online,
                }
            )

        # Sort the output_array by duration in descending order
        sorted_output_array = sorted(
            output_array,
            key=lambda x: (x["hours"], x["minutes"], x["seconds"]),
            reverse=True,
        )

        return sorted_output_array

    def calculate_duration(self, entry):
        new_duration = time_difference(entry.joinedAt)
        setattr(entry, "duration", new_duration)
        return entry

    def get_active_with_duration(self, ongoing):
        ongoing_arr = []
        for entry in ongoing:
            ongoing_arr.append(self.calculate_duration(entry))
        return ongoing_arr


    def calculate_update(self):
        all_entries = self.complete + self.get_active_with_duration(self.ongoing)
        return self.sum_and_format(all_entries)


    async def get_data(self):
        try:
            self.ongoing = await self.get_active(self.filter)
            self.complete = await self.get_completed(self.filter)
        except Exception as e:
            print(e)


class Dataset(queries, utils):
    def __init__(self, data, manager):
        self.manager = manager
        self.name = "dataset"
        # self.filter = data.manager.instances
        self.key = data.filter
        self.filter = data.where

    async def create(self, data):
        await self.update_dataset()

    async def update_dataset(self):
        await self.get_data()
        self.data = self.calculate_update()
        await self.manager.event_manager.publish("_updated_dataset", self)

    async def _destroyed_instance_filter(self, instance):
        if instance.key == self.key:
            await self.manager.destroy(self)
    async def _any_voice_state_update(self, data):
        await self.update_dataset()

    # TODO: CALL (UPDATE) EVERY THIRTY SECONDS OR SO
    # self.calculate_update()

# class lb_data(queries, utils):

