import asyncio
from datetime import datetime, time, timedelta, timezone

from modules.leaderboard_interface.lifecycle_manager import EventSubscriber
from modules.session_tracking.database_queries.queriess import (create_object,
                                create_query,
                                                                delete_all,
                                                                get_all)
from utils.time import *
from setup.bot_instance import bot

cet_timezone = pytz.timezone("CET")


class checkTime(EventSubscriber):
    def __init__(self):
        super().__init__()
        self.events = {
            self.is_start_of_hour: "_start_of_hour",
            self.is_fifteen_minutes_passed: "_fifteen_minutes_passed",
            self.is_start_of_day: "_start_of_day",
            self.is_start_of_week: "_start_of_week",
            self.is_start_of_month: "_start_of_month",
        }
        self.name_to_event = {
            "hour": "_start_of_hour",
            "day": "_start_of_day",
            "week": "_start_of_week",
            "month": "_start_of_month",
        }
        self.event_to_name = {
            "_start_of_hour": "hour",
            "_start_of_day": "day",
            "_start_of_week": "week",
            "_start_of_month": "month",
        }

    async def check_events(self):
        """
        this function runs at every  start of the minute
        it checks if it is the start of an hour, day, week, etc.
        If this is the case it will fire the  corresponding event
        for other classes to react to

        then it will up date the time where that event has last been
        fired. This is needed for other safety checks.
        If for example the last time that the hourly event has been fired is more
        than an hour ago it means something went wrong and I can counteract
        """
        timeStamp = datetime.now(cet_timezone)  # calculate timestamp here
        for event, message in self.events.items():
            if event(timeStamp):
                await self.publish(message, timeStamp)
                await self.update_switch(message, timeStamp)

    async def update_switch(self, message, timeStamp):
        """
        update the last time that the event has been triggered
        """

        if message == "_fifteen_minutes_passed":
            return

        switchName = self.event_to_name[message]
        where = {"name": switchName}
        data = {"switch": timeStamp, "name": switchName}
        update = await create_query("switches", "update_many", where=where, data=data)
        print(f"updated {switchName} to {timeStamp}")
        if update == 0:
            print(f"No entries found for {switchName}, creating new entry...")
            # Here, you will need to replace "create_entry" with the actual function name to create a new entry in your database
            create = await create_query("switches", "create", data=data)
            print(await get_all("switches"))
            print(f"Created new entry for {switchName} with timestamp {timeStamp}")
        return update

    def is_specific_minute(self, timeStamp, minutes):
        """check if it is currently a specific time"""
        return timeStamp.minute in minutes

    def is_start_of_hour(self, timeStamp):
        return self.is_specific_minute(timeStamp, [0])

    def is_fifteen_minutes_passed(self, timeStamp):
        return self.is_specific_minute(timeStamp, [0, 15, 30, 45])

    def is_start_of_day(self, timeStamp):
        return timeStamp.hour == 0 and self.is_start_of_hour(timeStamp)

    def is_start_of_week(self, timeStamp):
        today = datetime.today()
        return today.weekday() == 0 and self.is_start_of_day(timeStamp)

    def is_start_of_month(self, timeStamp):
        today = datetime.today()
        return today.day == 1 and self.is_start_of_day(timeStamp)

class TimeEvents(checkTime):
    def __init__(self):
        super().__init__()
    async def _fifteen_minutes_passed(self, timeStamp):
        await self.update_if_its_overdue("hour", timeStamp)

    async def _start_of_hour(self, timeStamp):
        await self.update_if_its_overdue("day", timeStamp)
        await self.update_if_its_overdue("week", timeStamp)

    async def functions_to_run(self):
        if bot.ready != False:
            await self.check_events()
            await self.publish("_one_minute_passed", None)


        """ 
        instead of setting a sleep of sixty second I chose to
        calculate the time until the next minute every time.
        This way if something takes  longer I can still
        make sure that the  function will never skip
        a minute
        """
        now = datetime.now(cet_timezone)
        seconds_until_next_minute = 60 - now.second
        await asyncio.sleep(seconds_until_next_minute)

    async def run_periodically(self):
        while True:
            await self.functions_to_run()

    async def update_if_its_overdue(self, type, timeStamp):
        """
        if an update is overdue it will perform it manually
        """
        if await self.safety_check("hour"):
            message = self.name_to_event["hour"]
            await self.update_switch(message, timeStamp)
            await self.publish(message, timeStamp)


    async def get_switch(self, name):
        where = {"name": name}
        result = await create_query("switches", "find_first", where=where)
        return result

    def calculate_time_passed(self, timestamp):
        time_passed = time_difference(timestamp)
        return time_passed

    async def safety_check(self, type):
        objects = {
            "hour": 3650,
            "day": 86500,
            "week": 604900,
        }

        treshold = objects[type]
        result = await self.get_switch(type)
        timestamp = result.switch
        time_passed = self.calculate_time_passed(timestamp)
        if time_passed >= treshold:
            print(f"last update more than {time_passed} seconds old")
            return True
        return False






