import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext import commands, tasks
import datetime
import asyncio
import User
import sys

sys.path.append('/.../')
from vc import vc
from mydb import db
from User import userfunction, user, User, Users



class challenge(commands.Cog):

    def __init__(self, client):
        self.client = client
    def start(client):
        print("hello world!")

def setup(client):
    client.add_cog(challenge(client))
