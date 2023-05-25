from utils.time import get_start_end, time_difference


class Filters:
    
    def __init__ (self):
        self.instances = {}
        self.filters = {
            "today_study_exclude_no_cam": {
                "date_range": "today",
                "activity": "Study",
                "exclude_type": "VC",
            },
            "today_study_all_types": {
                "date_range": "today",
                "activity": "Study",
            },
        }
        
    def get_filter(self, filter_name):
        if filter_name in self.instances:
                return self.instances[filter_name]
        filter = self.create_filter(filter_name)
        self.instances[filter_name] = filter
        return filter
    
    def refresh_filters(self): # TODO: call this one hourly I guess
        for filter_name in self.instances:
            self.instances[filter_name] = self.create_filter(filter_name)
            
    def create_filter(self, filter_name):
        # Creating from the filter templates
        filter = self.filters[filter_name]
        filter["date_range"] = get_start_end(filter["date_range"])
        activity = filter.get("activity")
        type_of_activity = filter.get("type_of_activity")
        exclude_type = filter.get("exclude_type")  # define the base wheRe clause
        where = {
            "AND": [
                {
                    "joinedAt": {"gte": filter["date_range"]["start"], "lt": filter["date_range"]["end"]},
                },
            ]
        }
        if activity:
            where["AND"].append({"activity": activity})
        if type_of_activity:
            where["AND"].append({"activityType": type_of_activity})
        if exclude_type:
            where["AND"].append(
                {"activityType": {"not": {"equals": exclude_type}}}
            )  # <-- Update field structure here
        return where

filter_singleton = Filters()
