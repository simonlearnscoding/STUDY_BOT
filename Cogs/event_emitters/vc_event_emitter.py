from Cogs.vc_event_wrappers import ensure_user_exists, ensure_user_has_active_session
from Cogs.VC_events import VCEventType, VCEvent
# import asyncio
"""
ALL OF THE THINGS THAT HAPPEN AS A RESULT OF VC EVENTS WILL HAPPEN HERE!
"""
# I can use bot dispatch
# @bot.event
# async def on_my_event(a, b, c):
#   # ...


class vc_event_manager():
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    @ensure_user_exists
    def user_joins_tracking_channel(vc_event: VCEvent):
        print('called user joins')
        pass

    @staticmethod
    def excluding_condition_met(vc_event: VCEvent):
        pass

    @staticmethod
    @ensure_user_exists
    @ensure_user_has_active_session
    def user_changed_type_of_tracking(vc_event: VCEvent):
        print('called user changed type of tracking')
        pass

    @staticmethod
    @ensure_user_exists
    @ensure_user_has_active_session
    def user_left_channel(vc_event: VCEvent):
        print('called user left channel')
        pass

    @staticmethod
    @ensure_user_exists
    @ensure_user_has_active_session
    def user_changed_channel(vc_event: VCEvent):
        print('called changed channel')
        pass

    @staticmethod
    def handle_vc_event(event_name: VCEventType, vc_event: VCEvent):
        # Dynamically get the corresponding method
        action = getattr(vc_event_manager, event_name.name, None)

        # Check if the method exists and is callable
        if callable(action):
            action(vc_event)
        else:
            print(f"No action defined for this event: {event_name.name}")
