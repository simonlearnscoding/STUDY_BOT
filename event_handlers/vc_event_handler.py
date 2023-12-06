import utils.vc_event_cnd as cnd


# TODO: test
# fetch the user from DB
# member = await User.object.get_or_create_user(member)


class vc_event_handler():

    @staticmethod
    def handle(VCEvent) -> str:

        if cnd.excluding_condition_is_met(VCEvent):
            return 'excluding_condition_met'

        if cnd.user_joins_tracking_channel(VCEvent):
            return 'user_joins_tracking_channel'

        if cnd.user_changed_type_of_tracking(VCEvent):
            return 'user_changed_type_of_tracking'

        if cnd.user_left_channel(VCEvent):
            return 'user_left_channel'

        if cnd.user_changed_channel(VCEvent):
            return 'user_changed_channel'

        # Default action if none of the conditions are met
        raise RuntimeError("Error in decision tree for VCEvent handling.")
