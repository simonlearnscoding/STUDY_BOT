import utils.Conditionals as cnd

from Cogs.VC_events import VCEventType

# TODO: test
# fetch the user from DB
# member = await User.object.get_or_create_user(member)


class decision_tree():

    @staticmethod
    def check_event_type(VCEvent) -> VCEventType:

        if cnd.excluding_condition_is_met(VCEvent):
            return VCEventType.excluding_condition_met

        if cnd.user_joins_tracking_channel(VCEvent):
            return VCEventType.user_joins_tracking_channel

        if cnd.user_changed_type_of_tracking(VCEvent):
            return VCEventType.user_changed_type_of_tracking

        if cnd.user_left_channel(VCEvent):
            print('user left channel')
            return VCEventType.user_left_channel

        if cnd.user_changed_channel(VCEvent):
            return VCEventType.user_changed_channel
        # # Default return value if none of the conditions are met
        # print('there was an error in the decision tree')
        return VCEvent
