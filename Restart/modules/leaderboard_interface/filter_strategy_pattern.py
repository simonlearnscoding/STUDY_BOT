from asgiref.sync import async_to_sync
from django.db.models import Q
from copy import deepcopy
from djangoproject.spqrapp.models import *
from utils.time import get_start_end

class QueryBuilder:
    def __init__(self):
        self.query = Q()

    def set_date_range(self, date_range):
        date_range = get_start_end(date_range)
        self.query &= Q(joined_at__gte=date_range["start"], joined_at__lt=date_range["end"])
        return self

    def set_activity(self, activity):
        if activity:
            self.query &= Q(activity=activity)
        return self

    def set_type_of_activity(self, type_of_activity):
        if type_of_activity:
            self.query &= Q(activity_type__name=type_of_activity)
        return self

    def exclude_type(self, exclude_type):
        if exclude_type:
            self.query &= ~Q(activity_type__name=exclude_type)
        return self

    def add(self, condition, combinator):
        if combinator == Q.AND:
            self.query &= condition
        elif combinator == Q.OR:
            self.query |= condition
        return self

    def build(self):
        return self.query



class FilterManager:
    def __init__(self):
        # Generate new filters
        self.filter_patterns = self.generate_filters()

    def generate_filters(self):
        # LATER: I think that I am creating an unneccessary layer of
        # abstraction by calculating the times  in the queryCreator
        # class just something to consider
        time_periods = {
            "today" : { "date_range" : "today" },
            "this_week" : { "date_range" : "this_week" },
            "this_month" : { "date_range" : "this_month" }
        }

        activity_types = {
            "exclude_no_cam": {"exclude_type" : "VC"},
            "all_types" : {},
            "both_only" : {"type_of_activity" : "BOTH"},
        }
        activities = {
            "study" : {"activity" : "Study"}
            , "all_activities" : {},
        }
        new_filters = {}
        for time_period_key, time_period_value in time_periods.items():
            for activity_type_key, activity_type_value in activity_types.items():
                for activity_key, activity_value in activities.items():
                    new_filter_name = f"{time_period_key}-{activity_key}-{activity_type_key}"
                    new_filters[new_filter_name] = {**time_period_value, **activity_type_value, **activity_value}
        return new_filters



    async def get_data(self, target):
        builder = QueryBuilder()
        pattern = self.filter_patterns[target.key]
        base_query = builder.set_date_range(pattern.get("date_range")) \
            .set_activity(pattern.get("activity")) \
            .set_type_of_activity(pattern.get("type_of_activity")) \
            .exclude_type(pattern.get("exclude_type")).build()

        try:
            # Create a copy of base_query and add a new condition
            filter_ongoing = deepcopy(base_query).add(Q(status="ONGOING"), Q.AND)
            # Wrap the synchronous Django ORM operations with async_to_sync
            ongoing = await ActivityLog.object.get_all_filtered(filter_ongoing)

            filter_completed = deepcopy(base_query).add(Q(status="COMPLETED"), Q.AND)
            complete = await ActivityLog.object.get_all_filtered(filter_completed)
            return [ongoing, complete]
        except Exception as e:
            print(e)
