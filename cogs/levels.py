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



class levels(commands.Cog):

    def __init__(self, client):
        self.client = client

    def addXP(client, member, xp):
        print(f"{member.name} - {xp}")

        sql = "UPDATE users.user SET XP = XP + %s WHERE ID = %s"
        val = (xp, member.id)
        db.cur.execute(sql, val)
        db.mydb.commit()
def setup(client):
    client.add_cog(levels(client))
