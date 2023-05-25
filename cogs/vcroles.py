import discord
from discord.ext import commands

from cogs.vc import vc
import asyncio
class vcroles(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def focusmode(member, minutes):
        focusrole = discord.utils.get(member.guild.roles, id=vc.focused_role)
        vcrole = discord.utils.get(member.guild.roles, id=vc.vc_role)

        await member.remove_roles(vcrole)
        await member.add_roles(focusrole)
        await asyncio.sleep(minutes * 60)
        #message here
        await member.remove_roles(focusrole)
        if (member.voice is not None):
            await member.add_roles(vcrole)
        await vc.bot_spam.send(f"Timer finished: {member.mention} !")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            print(member.roles)
            for i in range(len(member.roles)):
                if member.roles[i].name == "focused":
                    return

            role = discord.utils.get(member.guild.roles, id=vc.vc_role)
            await member.add_roles(role)

            # member joined a voice channel, add the roles here

        elif before.channel is not None and after.channel is None:
            role = discord.utils.get(member.guild.roles, id=vc.vc_role)
            await member.remove_roles(role)


async def setup(client):
    await client.add_cog(vcroles(client))

async def teardown(client):
    return