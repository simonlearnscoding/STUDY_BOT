from enum import Enum

# from dataclasses import dataclass
from discord import Member, VoiceState


class VCEvent:
    def __init__(self, member: Member, before: VoiceState, after: VoiceState):
        self.member = member
        self.before = before
        self.after = after


class VCEventType(Enum):
    excluding_condition_met = "excluding condition met (user muted | deafened)"
    user_joins_tracking_channel = "user joins tracking channel"
    user_changed_type_of_tracking = "user changed type of tracking"
    user_left_channel = "user left channel"
    user_changed_channel = "user changed channel"
