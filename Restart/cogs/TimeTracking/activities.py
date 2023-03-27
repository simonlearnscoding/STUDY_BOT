import discord

from Database 

from Database import queries as db

from Restart.Settings import server

PILLARS = {
    "PHYSICAL_WORK": "Physical Work",
    "DISCIPLINE": "Discipline",
    "THINKER": "Thinker"
}

# Mapping of activities to pillars
ACTIVITY_TO_PILLAR = {
    "Study": PILLARS["THINKER"],
    "Workout": PILLARS["PHYSICAL_WORK"],
    "Meditation": PILLARS["DISCIPLINE"],
    "Yoga": PILLARS["PHYSICAL_WORK"],
    "Reading": PILLARS["THINKER"],
    "Chores": PILLARS["DISCIPLINE"],
    "Creative": PILLARS["THINKER"]
}

def getActivity(id):
    try:
        return VC_to_Activity[id]
    except Exception as e:
        print(e)
        return None


class defaultRewards:
    def __init__(self):
        self.perMinute = (1,)
        self.perMinuteCam = (1.3,)
        self.perMinuteSS = (1.4,)
        self.perMinuteBoth = (1.7,)
        self.streakExtra = (0,)
        self.firstOfDay = (0,)
        self.maxReward = 1000


class workoutRewards(defaultRewards):
    def __init__(self):
        super().__init__()
        self.perMinute = (1.5,)
        self.perMinuteCam = (1.8,)
        self.streakExtra = (1.5,)
        self.firstOfDay = (15,)


class ActivityCreator:
    def __init__(self, name, reward=defaultRewards(), vcName=None):
        self.name = name
        self.reward = reward
        self.pillar = ACTIVITY_TO_PILLAR[name]  # Add the associated pillar
        for channel in vcName:
            id = server.channel_id[channel]
            VC_to_Activity[id] = name


def getActivityType(after):
    if after.self_stream and after.self_video:
        return "BOTH"
    if not after.self_stream and not after.self_video:
        return "VC"
    if after.self_stream:
        return "SS"
    if after.self_video:
        return "CAM"


VC_to_Activity = {}

# TODO: check if this compares to the vc names
Activities = {
    "Study": ActivityCreator("Study", defaultRewards, ["VC_STUDY", "VC_SPARTA"]),
    "Workout": ActivityCreator("Workout", workoutRewards, ["VC_WORKOUT"]),
    "Meditation": ActivityCreator("Meditation", defaultRewards, ["VC_MEDITATION"]),
    "Yoga": ActivityCreator("Yoga", defaultRewards, ["VC_YOGA"]),
    "Reading": ActivityCreator("Reading", defaultRewards, ["VC_READING"]),
    "Chores": ActivityCreator("Chores", defaultRewards, ["VC_CHORES"]),
    "Creative": ActivityCreator(
        "Creative", defaultRewards, ["VC_CREATIVE"]
    ),  # TODO: Add producing vc here
}
print(VC_to_Activity)
print(Activities)
