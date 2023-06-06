
import discord
from discord import app_commands
from discord.ext import commands

# SET THE SERVER THE BOT SHOULD BE WORKING ON
# CHOOSE BETWEEN THE FOLLOWING OPTIONS:
# testing
# SPQR
serverName = "SPQR"  # testing and SPQR server


intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.message_content = True
application_id = 839089655189864508


bot = commands.Bot(command_prefix="!", intents=intents)
bot.ready = False


token = "ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk"
# token = "MTExNDg4MjIyNzE1OTk3ODAzNw.GQ4zRy.pnrZb3oYKsMvxpkH2Je5h9mEY61LJfCFHndYYE"
