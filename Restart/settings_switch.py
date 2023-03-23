# SET THE SERVER THE BOT SHOULD BE WORKING ON
# CHOOSE BETWEEN THE FOLLOWING OPTIONS:

# testing
# SPQR
<<<<<<< HEAD:Restart/settings.py
=======

serverName = "testing" 


>>>>>>> master:Restart/settings_switch.py
import discord
from discord.ext import commands

serverName = "testing"  # testing and SPQR server


intents = discord.Intents.all()
intents.message_content = True
application_id = 839089655189864508


client = commands.Bot(command_prefix="~", intents=intents)

token = "ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk"
