import discord
from discord.ext import commands

from bases.event_manager_base import event_manager_baseclass
from utils.error_handler import class_error_handler
from model_managers_tortoise.server_instance import server
from model_managers_tortoise.user_server import user_server_class, UserServerEntity


async def setup(bot):
    await bot.add_cog(server_events_cog(bot))


@class_error_handler
class server_events_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server_instance = server(self.bot, guild)
        await server_instance.create_or_nothing()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        server_instance = server(self.bot, guild)
        await server_instance.delete_strategy.delete(server_instance)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user_instance = user_server_class(self.bot, entity=UserServerEntity(member, member.guild))
        await user_instance.create_or_nothing()
        # I need to create the UserServer not the user Instance

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        user_instance = user_server_class(self.bot, entity=UserServerEntity(member, member.guild))
        await user_instance.delete_strategy.delete(user_instance)
        # I need to create the UserServer not the user Instance
