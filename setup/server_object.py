import json
import os

from setup.bot_instance import bot, serverName

# replace with bot object if using a bot account


class serverFetcher:
    def __init__(self, serverName):
        self.bot = bot  # discord bot object
        self.channel_id = {}  # dictionary of channel ids
        self.channel_name = {}
        with open(f"setup/server_ids/{serverName}.json") as f:
            channel_ids = json.load(f)

        # GET THE tEXTcHANNEL OBJECTS FOR EACH CHANNEL id
        for name, id in channel_ids.items():
            self.channel_id[name] = int(id)
            self.channel_name[id] = name

    # TODO: I feel like this whole function is redundant
    def getChannel(self, name):
        return self.bot.get_channel(self.channel_id[name])


server = serverFetcher(serverName)
