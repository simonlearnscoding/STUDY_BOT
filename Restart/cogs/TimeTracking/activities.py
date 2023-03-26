import discord
from Restart.Settings import server


def getActivity(id):
    try:
        ac = VC_to_Activity[id]
        return ac
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
