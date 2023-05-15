from utils.time import get_start_end, time_difference

from Restart.Database.connector import *


class DataManager:
    def __init__(self):
        self.datasets = []

class dataset:
    def __init__(self, filter):
        self.filter = filter
        self.data = self.get_all_entries(self.filter)
        ## I am fetching twice by using get_active like this
        ## Do I need to store the active tasks? -> yes I do, to reduce the update 
        # fetching
        
        # Self.completed is not useful to store actually..
        
        # when a new leaderboard instance is created I need to:
        # push to the lb manager array


        # when a dataset is stored it should always add to 
        self.active = self.get_active(filter)
        self.active_with_duration = self.get_active_with_duration(self.active)
        self.completed = self.get_completed(self.filter)
        self.all_entries = self.get_all_entries(self.filter)
        # get formatted

        self.leaderboards = [] # how do I connect lb to dataset?
        # update_active_with_duration
 

    async_def get_all_entries(filter):
        completed = await get_completed(filter) 
        ongoing_arr = await get_active_with_duration(filter)
        entries = completed + ongoing_arr
        UserArr = []
        for entry in entries:
            UserArr.append(entry)
        return UserArr

    async def get_active(filter):
        filter_copy = filter.copy()
        filter_copy["AND"][0] = {"status": "ACTIVE"}
        return await create_query(
            "activitylog",
            "find_many",
            where=filter_copy,
        )

    async def get_active_with_duration(ongoing): 
        ongoing_arr = []
        for entry in ongoing:
            new_duration = time_difference(entry.joinedAt)
            new_entry = entry.copy()  # Creates a copy of the entry object
            setattr(new_entry, "duration", new_duration)
            ongoing_arr.append(new_entry)  
        return ongoing_arr

    async def get_completed(filter):
        filter_copy = filter.copy()
        filter_copy["AND"][0] = {"status": "COMPLETED"}
        return await create_query(
            "activitylog",
            "find_many",
            where=filter_copy,
        )
