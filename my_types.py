from enum import Enum

# from dataclasses import dataclass
from discord import Member, VoiceState


class VCEvent:
    def __init__(self, member: Member, before: VoiceState, after: VoiceState):
        self.member = member
        self.before = before
        self.after = after


class ChannelEvent:
    def __init__(self, event_str, before=None, after=None):
        self.event_str = event_str
        self.before = before
        self.after = after
