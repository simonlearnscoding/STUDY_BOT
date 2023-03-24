import discord
from discord.ext import commands
from vc import server
from settings_switch import db, client



# RENAME MYCOG TO NAME OF THE MODULE
class DataBase(commands.Cog):
    def __init__(self, client):
        self.client = client


    # on message event if message channel is generalText reply with hi



async def setup(client):
    # RENAME MYCOG TO THE NAME OF THE MODULE
    await client.add_cog(DataBase(client))


async def teardown(client):
    return
