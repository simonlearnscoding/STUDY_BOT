import discord
from discord.ext import commands
from cogs.vc import vc

class vcroles(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def on_voice_state_update(member, before, after):
        if before.channel is None and after.channel is not None:
            print(member.roles)
            role = discord.utils.get(member.guild.roles, id=vc.challenge_role_1)

            # member joined a voice channel, add the roles here

        elif before.channel is not None and after.channel is None:
            pass
            # member left a voice channel, remove the roles here

async def setup(client):
    await client.add_cog(vcroles(client))

async def teardown(client):
    return