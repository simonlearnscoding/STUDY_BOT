
from event_emitters.server_event_emitter import server_event_emitter
import discord
from discord.ext import commands

from bases.event_manager_base import event_manager_baseclass
from utils.error_handler import class_error_handler


async def setup(bot):
    await bot.add_cog(server_events_cog(bot))


@class_error_handler
class server_events_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f'joined guild {guild.name}')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f'removed guild{guild.name}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'Member joined: {member.name} (ID: {member.id})')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'Member left: {member.name} (ID: {member.id})')
