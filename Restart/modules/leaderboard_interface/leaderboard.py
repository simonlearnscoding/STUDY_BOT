# from modules.leaderboard_interface.Content import Content_Manager
from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager
from setup.bot_instance import bot

import discord


class LeaderboardManager(LifeCycleManager):
    def __init__(self):
        self.instance_class = Leaderboard
        super().__init__()

    async def user_joins_tracking_channel(self, data):
        key = data["member"].id
        await super().create(data, key)


class Leaderboard:
    def __init__(self, data, manager):
        self.bot = bot
        self.manager = manager
        self.member = data["member"]
        self.name = "leaderboard"
        self.key = self.member.id
        # TODO: replace this with the get filter function
        self.filter = "today_study_exclude_no_cam"

    async def user_left_tracking_channel(self, data):
        await self.manager.destroy(self)

    async def create(self, data):
        self.channel = await self.create_private_channel()
        self.message = await self.write_and_get_message()

        # self.image_url = self.content.image.url
        # await self.update_in_channel(self.image_url)

    async def destroy(self):
        await self.channel.delete()

    # TODO: this probably belongs to the image class
    async def update_in_channel(self, image_url):
        embed = discord.Embed()
        embed.set_image(url=image_url)
        # get the leaderboard channel
        # await channel.send(embed=embed)
        await self.message.edit(content="Leaderboard", embed=embed)
        pass

    async def destroyed_instance_filter(self, instance):
        if instance.key == self.key:
            await self.manager.destroy(self)
    async def updated_image(self, imageInstance):
        await self.update_image_if_filter_lb(imageInstance)

    async def update_image_if_filter_lb(self, imageInstance):
        if imageInstance.key == self.filter:
            url = imageInstance.url
            try:
                await self.update_in_channel(url)
                print(imageInstance)
            except Exception as e:
                print(e)

    async def create_private_channel(self):
        member = self.member
        # TODO REMOVE THIS WHEN IM DONE WITH TESTING
        # TODO  test with multiple users

        if member.id != 366276958566481920:
            return

        guild = self.bot.get_guild(
            789814373434654731
        )  # LATER: I will need to make this scalable if I want to use my bot for multiple servers
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

    async def write_and_get_message(self):
        # if there is a message id in the DB and I can fetch it #TODO: create message id in SQL
        url = "https://upload.wikimedia.org/wikipedia/commons/b/b9/Youtube_loading_symbol_1_(wobbly).gif"
        self.message = await self.channel.send(url)
        return self.message
        # TODO: I need a function to destroy the leaderboard, call that function when the user leaves the channel