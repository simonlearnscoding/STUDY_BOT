from Settings.main_settings import bot

import discord
from cogs.leaderboard.DataSets.dataset_class import DatasetManager
from cogs.leaderboard.filter import FilterInstance
from cogs.SingletonFactoryManager import SingletonFactoryManager


class LeaderboardManager(SingletonFactoryManager):
    async def create_leaderboard(self, member):
        return await self.create(key=member, instance_class=Leaderboard)

    async def destroy_leaderboard(self, member):
        lb = self.instances[member]
        await lb.channel.delete()  # TODO: test if it deletes the channel
        print('deleted the channel')
        # TODO: Test this
        lb.data.lb.remove(member)
        if len(lb.data.lb) == 0:
            #HERE: Test the destroy Dataset function
            await DatasetManager().destroy_dataset(lb.data.filter.name)
            ##

        # TODO: remove the message from the DB
        # TODO: remove the leaderboard from the dictionary of filters and data
        await self.destroy(member)


leaderboard_manager = LeaderboardManager()


class Leaderboard:
    def __init__(self, member):
        # TODO: 3. Test filter creation
        # I have to get the data
        # TODO: instead of filter data and image I should have just a lbContent Class
        # self.filter = FilterInstance("today_study_exclude_no_cam")

        self.bot = bot
        self.member = member

    async def initialize(self):
        self.channel = await self.create_private_channel(self.member)
        # TODO: create data and image and filter class
        self.message = await self.get_message(self.member, self.channel)
        self.filter_name = "today_study_exclude_no_cam"
        self.data = await DatasetManager().create_dataset(name=self.filter_name, lb=self.member)
        # self.data = self.get_data()

    async def create_private_channel(self, member):
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
        return await guild.create_text_channel(
            channel_name, overwrites=overwrites, category=category
        )

    # TODO: TEST
    async def get_message(self, member, channel):
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

        # self.image = self.create_image(self.data)

    def get_data(self):
        arr = db.get_entries_within_range(
            filter
        )  # Assuming this function is now synchronous
        arr = sum_durations(arr)
        return arr

    def create_image(self, data):
        img = create_leaderboard_image(data)
        return img
