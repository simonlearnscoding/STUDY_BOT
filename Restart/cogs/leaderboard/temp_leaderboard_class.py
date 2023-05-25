from Settings.main_settings import bot

import discord
from cogs.leaderboard.Content import Content_Manager
from cogs.SingletonFactoryManager import SingletonFactoryManager
from cogs.leaderboard.image import Image_Manager
# from cogs.leaderboard.filter import FilterInstance


class LeaderboardManager(SingletonFactoryManager):
    async def create_leaderboard(self, member):
        return await self.create(key=member, instance_class=Leaderboard)

    async def destroy_leaderboard(self, member):
        lb = self.instances[member]
        await lb.channel.delete()
        print("deleted the channel")
        lb.data.lb.remove(member)
        if len(lb.data.lb) == 0:
            await Content_Manager.destroy_dataset(lb.data.filter.name)
        await self.destroy(member)


class Leaderboard:
    def __init__(self, member):
        self.bot = bot
        self.member = member

    async def initialize(self, key):

        self.channel = await self.create_private_channel(self.member)
        self.message = await self.write_and_get_message(self.member, self.channel)

        # TODO: get the user preferred filter from the DB
        filter_name = "today_study_all_types"
        content = await Content_Manager.create_dataset(filter_name, self)  # TODO: YOU ARE HERE!
        self.data = content.data.data
        image_message = await Image_Manager.create_image(filter_name, self.data)
        self.image_url = image_message.url
        await self.update_in_channel(self.image_url)
    # def create_image(self, data):
    #     img = create_leaderboard_image(data)
    #     return img

    async def update_in_channel(self, image_url):
        embed = discord.Embed()
        embed.set_image(url=image_url)
        # get the leaderboard channel
        #TODO: replace the channel id by getting the channel from the user name
        # await channel.send(embed=embed)
        await self.message.edit(content="Leaderboard", embed=embed)

        pass

#TODO: Big bug: it seems to only work if the channed already exists

    async def create_private_channel(self, member):
        # TODO REMOVE THIS WHEN IM DONE WITH TESTING
        if member.id != 366276958566481920:
            return

        guild = self.bot.get_guild(789814373434654731)
        channel_name = f"{member.name}s leaderboard".lower().replace(" ", "-")
        # Check if the channel already exists
        for channel in guild.channels:
            if channel.name == channel_name:
                await channel.purge(limit=100)
                return channel  # If channel already exists, return it

        # If channel doesn't exist, create it
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
        }
        category_id = 789814373870075929  # Replace with your actual category ID
        category = guild.get_channel(category_id)
        try:
            return await guild.create_text_channel(
                channel_name, overwrites=overwrites, category=category
                )
        except Exception as e:
            print(e)

    async def write_and_get_message(self, member, channel):
        # if there is a message id in the DB and I can fetch it #TODO: create message id in SQL
        # self.message = await self.bot.get_channel(channel_id).fetch_message(message_id)
        # return message
        url = "https://upload.wikimedia.org/wikipedia/commons/b/b9/Youtube_loading_symbol_1_(wobbly).gif"
        self.message = await channel.send(url)
        return self.message
        # TODO: I need a function to destroy the leaderboard, call that function when the user leaves the channel

        # when leaderboard gets created:
        # send the leaderboard image to the channel
        message_id = None  # store the message id in the leaderboard object


# class leaderboard_utils:
#     async def create_private_channel(self, member):
#         # NOTE REMOVE THIS WHEN IM DONE WITH TESTING
#         if member.id != 366276958566481920:
#             return
# <!-- order:0 -->
#
#         guild = self.bot.get_guild(789814373434654731)
#         channel_name = f"{member.name}s leaderboard".lower().replace(" ", "-")
#         # Check if the channel already exists
#         for channel in guild.channels:
#             if channel.name == channel_name:
#                 await channel.purge(limit=100)
#                 return channel  # If channel already exists, return it
#
#         # If channel doesn't exist, create it
#         overwrites = {
#             guild.default_role: discord.PermissionOverwrite(read_messages=False),
#             member: discord.PermissionOverwrite(read_messages=True),
#         }
#         category_id = 789814373870075929  # Replace with your actual category ID
#         category = guild.get_channel(category_id)
#         return await guild.create_text_channel(
#             channel_name, overwrites=overwrites, category=category
#         )
#
#     async def write_and_get_message(self, member, channel):
#         # if there is a message id in the DB and I can fetch it #TODO: create message id in SQL
#         # self.message = await self.bot.get_channel(channel_id).fetch_message(message_id)
#         # return message
#         url = "https://upload.wikimedia.org/wikipedia/commons/b/b9/Youtube_loading_symbol_1_(wobbly).gif"
#         self.message = await channel.send(url)
#         return self.message
#         # TODO: I need a function to destroy the leaderboard, call that function when the user leaves the channel
#
#         # when leaderboard gets created:
#         # send the leaderboard image to the channel
#         message_id = None  # store the message id in the leaderboard object
#
leaderboard_manager = LeaderboardManager()
