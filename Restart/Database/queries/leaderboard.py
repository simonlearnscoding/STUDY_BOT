import itertools

from utils.time import get_start_end, time_difference

from Restart.Database.connector import *


class lb_queries():
    def __init__(self):
        pass
    
    async def get_all_entries(filter):
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

    async def get_active_with_duration(filter): 
        ongoing_arr = []
        ongoing = await get_active(filter)
        for entry in ongoing:
            ongoing_arr.append(self.calculate_duration(entry))  
        return ongoing_arr

    def calculate_duration(entry):
        new_duration = time_difference(entry.joinedAt)
        setattr(entry, "duration", new_duration)
        return entry

    # calculate the duration for the ongoing entries
        
    async def get_completed(filter):
        filter_copy = filter.copy()
        filter_copy["AND"][0] = {"status": "COMPLETED"}
        return await create_query(
            "activitylog",
            "find_many",
            where=filter_copy,
        )
