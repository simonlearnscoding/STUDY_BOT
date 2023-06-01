import json
import os

from setup.bot_instance import bot, serverName

# replace with bot object if using a bot account


class serverFetcher:
    def __init__(self, serverName):
        self.bot = bot  # discord bot object
        self.channel_id = {}  # dictionary of channel ids
        self.channel_name = {}
        # LOAD THE APPROPRIATE JSON FILE BASED ON THE TESTING FLAG
        # get the cwd
        cwd = os.path.dirname(os.getcwd())
        print(cwd)
        with open(f"{cwd}/Restart/setup/server_ids/{serverName}.json") as f:
            channel_ids = json.load(f)

        # GET THE tEXTcHANNEL OBJECTS FOR EACH CHANNEL id
        for name, id in channel_ids.items():
            print(name, id)
            self.channel_id[name] = int(id)
            self.channel_name[id] = name

    def getChannel(self, name):
        return self.bot.get_channel(self.channel_id[name])


server = serverFetcher(serverName)
