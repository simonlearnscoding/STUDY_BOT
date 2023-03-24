import discord
from Restart.vc import server


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


class Activity:
    def __init__(self, name, reward=defaultRewards(), vcName=None):
        self.name = name
        self.reward = reward
        for channel in vcName:
            id = server.channel_id[channel]
            VC_to_Activity[id] = name


VC_to_Activity = {}

# TODO: check if this compares to the vc names
Activities = {
    "Study": Activity("Study", defaultRewards, ["VC_STUDY", "VC_SPARTA"]),
    "Workout": Activity("Workout", workoutRewards, ["VC_WORKOUT"]),
    "Meditation": Activity("Meditation", defaultRewards, ["VC_MEDITATION"]),
    "Yoga": Activity("Yoga", defaultRewards, ["VC_YOGA"]),
    "Reading": Activity("Reading", defaultRewards, ["VC_READING"]),
    "Chores": Activity("Chores", defaultRewards, ["VC_CHORES"]),
    "Creative": Activity(
        "Creative", defaultRewards, ["VC_CREATIVE"]
    ),  # TODO: Add producing vc here
}
print(VC_to_Activity)
print(Activities)
