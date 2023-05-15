from utils.time import get_start_end, time_difference

# TODO I could create a
# STATEMANAGER WRAPPER here if this pattern will be common


class FilterManager:
    def __init__(self):
        self.filters = {}

    def create(self, filter_name):
        if filter_name not in self.filters:
            filter = FilterInstance(filter_name)
            self.filters[filter_name] = filter
            return filter
        return self.filters[filter_name]

    # def get_all(self):  --  is this one still necessary?
    #     return self.filters


class Filter:
    def __init__(self):
        self.leaderboards = []
        self.filters = {
            "today_study_exclude_no_cam": {
                "date_range": get_start_end("today"),
                "activity": "Study",
                "exclude_type": "VC",
            },
            "today_study_all_types": {
                "date_range": get_start_end("today"),
                "activity": "Study",
            },
        }

    def get_filter(self, filter_name):
        filter = self.filters[filter_name]
        date_range = filter.get("date_range")
        activity = filter.get("activity")
        type_of_activity = filter.get("type_of_activity")
        exclude_type = filter.get("exclude_type")  # define the base wheRe clause
        where = {
            "AND": [
                {
                    "joinedAt": {"gte": date_range["start"], "lt": date_range["end"]},
                },
            ]
        }

        if activity:
            where["AND"].append({"activity": activity})
        # add activitytype to the where clause based on the given parameters
        if type_of_activity:
            where["AND"].append({"activityType": type_of_activity})
        if exclude_type:
            where["AND"].append(
                {"activityType": {"not": {"equals": exclude_type}}}
            )  # <-- Update field structure here
        return where


class FilterInstance(Filter):
    def __init__(self, initial_filter):
        super().__init__()
        self._filter = self.filters[initial_filter]

    def get_current_filter(self):
        return self._filter

    def set_filter(self, new_filter):
        if new_filter in self.filters:
            self._filter = self.filters[new_filter]
