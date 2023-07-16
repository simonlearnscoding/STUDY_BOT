
from django.db.models import Q
from utils.time import get_start_end
from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager

class Filter:
    def __init__(self, data, manager):
        self.manager = manager
        self.name = "filter"
        self.filter = data["filter"]
        self.key = data["filter"]
        self.where = self.get_filter_where()

    def get_filter_where(self):
        filter_data = self.manager.filter_patterns[self.key]
        filter_data["date_range"] = get_start_end(filter_data["date_range"])
        query = Q(joined_at__gte=filter_data["date_range"]["start"], joined_at__lt=filter_data["date_range"]["end"])
        if filter_data.get("activity"):
            query &= Q(activity=filter_data["activity"])
        if filter_data.get("type_of_activity"):
            query &= Q(activity_type__name=filter_data[
                "type_of_activity"])  # Filter by the name field of the related ActivityType object
        if filter_data.get("exclude_type"):
            query &= ~Q(activity_type__name=filter_data[
                "exclude_type"])  # Filter by the name field of the related ActivityType object
        return query

class FilterManager(LifeCycleManager):
    def __init__(self):
        self.instance_class = Filter
        super().__init__()
        self.filter_patterns = {
            "today_study_exclude_no_cam": {
                "date_range": "today",
                "activity": "Study",
                "exclude_type": "VC",
            },
            "today_study_all_types": {
                "date_range": "today",
                "activity": "Study",
            },
            "today_all_both_only": {
                "date_range": "today",
                "type_of_activity": "BOTH"
            },
            "today_all": {
                "date_range": "today",
            },
        }

    async def _bot_ready(self, bot):
        for pattern in self.filter_patterns:
            data = {}
            data["data"] = self.filter_patterns[pattern]
            data["filter"] = pattern
            await super().create(data=data, key=pattern)

#
#
# # ___ OLD CODE STARTS HERE I WILL KEEP IT FOR REF FOR NOW ___
# from utils.time import get_start_end
#
#
#
# from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager
#
#
# class FilterManager(LifeCycleManager):
#     def __init__(self):
#         self.instance_class = Filter
#         super().__init__()
#         self.filter_patterns = {
#         "today_study_exclude_no_cam": {
#             "date_range": "today",
#             "activity": "Study",
#             "exclude_type": "VC",
#         },
#         "today_study_all_types": {
#             "date_range": "today",
#             "activity": "Study",
#         },
#         "today_all_both_only": {
#             "date_range": "today",
#             "type_of_activity": "BOTH"
#         },
#         "today_all": {
#             "date_range": "today",
#         },
#         }
#     """
#     this gets triggered when the first lb
#     instance of one filter
#     gets created
#     """
#     # async def _changed_filter(self, data):
#     #     key = data.filter
#     #     await super().create(data, key)
#
#     async def _bot_ready(self, bot):
#         for pattern in self.filter_patterns:
#             data = {}
#             data["data"] = self.filter_patterns[pattern]
#             data["filter"] = pattern
#             await super().create(data=data, key=pattern)
#             pass
#     # async def _first_instance_with_filter_leaderboard(self, data):
#     #     """
#     #     set filter name as key and create the object
#     #     """
#     #     key = data.filter
#     #     await super().create(data, key)
#
#
# class Filter():
#     def __init__(self, data, manager):
#         self.manager = manager
#         self.name = "filter"
#         self.filter = data["filter"]
#         self.key = data["filter"]
#
#     async def _start_of_hour(self, time):
#         # LATER: I should probably leave this at _start of day for now until i choose to implement timezones
#
#         #TODO: Test this one (it seems not to work yet)
#         self.where = await self.get_filter_where()
#         await self.manager.publish("_updated_filter", self)
#     # async def _last_instance_with_filter_leaderboard(self, instance):
#     #     if instance.filter == self.filter:
#     #         await self.manager.destroy(self)
#     async def create(self, data):
#         self.where = await self.get_filter_where()
#
#
#     async def get_filter_where(self):
#         # Creating from the filter templates
#         filter = self.manager.filter_patterns[self.key]
#         filter["date_range"] = get_start_end(filter["date_range"])
#         activity = filter.get("activity")
#         type_of_activity = filter.get("type_of_activity")
#         exclude_type = filter.get("exclude_type")  # define the base wheRe clause
#         where = {
#             "AND": [
#                 {
#                     "joinedAt": {"gte": filter["date_range"]["start"], "lt": filter["date_range"]["end"]},
#                 },
#             ]
#         }
#         if activity:
#             where["AND"].append({"activity": activity})
#         if type_of_activity:
#             where["AND"].append({"activityType": type_of_activity})
#         if exclude_type:
#             where["AND"].append(
#                 {"activityType": {"not": {"equals": exclude_type}}}
#             )  # <-- Update field structure here
#         return where
#
#
