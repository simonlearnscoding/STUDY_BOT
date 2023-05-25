import discord
from discord.ext import commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "*", intents = intents)

@client.event
async def on_ready():
    server = client.get_guild(917547601539264623)
    text_channel_list = []
    for channel in server.channels:
        if str(channel.type) == 'text':
            text_channel_list.append(channel)
            print(text_channel_list)

    print(client.get_all_channels())


client.run("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk")
