import utils.vc_event_cnd as cnd


# TODO: test
# fetch the user from DB
# member = await User.object.get_or_create_user(member)


class vc_event_handler():
    def __init__(self, bot):
        self.bot = bot

    async def handle(self, VCEvent) -> str:

        did_user_change_activity_record_type = cnd.did_user_change_activity_record_type(
            handle_if=cnd.EmitUserChangedActivityRecordType,
            handle_else=cnd.is_user_after_activity_none
        )
        is_user_after_activity_same_as_user_current_activity = cnd.is_user_after_activity_same_as_user_current_activity(
            handle_if=cnd.is_user_after_activity_none,
            handle_else=cnd.is_user_after_activity_same_as_user_current_activity

        )

        is_user_activity_same_server_as_event = cnd.is_user_activity_same_server_as_event(
            handle_if=is_user_after_activity_same_as_user_current_activity,
            handle_else=None
        )

        has_user_active_session = cnd.has_user_active_session(
            handle_if=is_user_activity_same_server_as_event,
            handle_else=cnd.is_after_channel_activity
        )

        root_node = cnd.is_ignore_case_met(bot=self.bot,
                                           event=VCEvent,
                                           handle_if=None,
                                           handle_else=has_user_active_session)
        await root_node.handle_case()
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
