
import discord
from discord import app_commands
from discord.ext import commands
import os
import pathlib
from dotenv import load_dotenv

load_dotenv('.env')
# SET THE SERVER THE BOT SHOULD BE WORKING ON
# CHOOSE BETWEEN THE FOLLOWING OPTIONS:
# testing
# SPQR
serverName = "SPQR"  # testing and SPQR server


intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.message_content = True

application_id = os.getenv('APPLICATION_ID')
bot = commands.Bot(command_prefix="!", intents=intents)

bot.ready = False

token = os.getenv('TOKEN')
