from collections import defaultdict
from bases.connector import create_query
from modules.TimeTracking.utils.time import time_difference
from cogs.leaderboard.filter import Filter_Manager
from bases.state_manager import SingletonFactoryManager


class Dataset_Data_Manager(SingletonFactoryManager):
    def __init__(self):
        self.instance_class = dataset_instance

    #TODO: is it necessary to have a destroy_dataset method if it inherits the same from its parent class?
    #TODO: call it every time someone joins or leaves vc
    async def set_data(self):
        for dataset in self.instances:
            dataset.get_data()


class queries:
    async def get_active(self, filter):
        filter_copy = filter.copy()
        # TODO: check whats up with create query, is it accessible or not?
        filter_copy["AND"][0] = {"status": "ONGOING"}
        print(filter_copy)
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

# class lb_data(queries, utils):
class dataset_instance(queries, utils):
    def __init__(self, key):
        super().__init__()
        self.name = key

    async def initialize(self, key):
        self.filter = Filter_Manager.instances[key]
        self.name = key
        await self.set_data()
        self.data = self.calculate_update(self.complete, self.ongoing)

    # TODO: CALL THIS ONE EVERY THIRTY SECONDS OR SO
    def calculate_update(self, complete, ongoing):
        all_entries = complete + self.get_active_with_duration(ongoing)
        return self.sum_and_format(all_entries)


    async def set_data(self):
        try:
            self.ongoing = await self.get_active(self.filter)
            self.complete = await self.get_completed(self.filter)
        except Exception as e:
            print(e)


Dataset_Manager = Dataset_Data_Manager()