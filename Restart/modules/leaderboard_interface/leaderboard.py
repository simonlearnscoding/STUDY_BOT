# from modules.leaderboard_interface.Content import Content_Manager
from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager
from setup.bot_instance import bot
from modules.session_tracking.database_queries.queries.user_queries import get_user

import discord
from discord.ui import Button, View

class LeaderboardManager(LifeCycleManager):
    def __init__(self):
        self.instance_class = Leaderboard
        super().__init__()

    async def _user_joins_tracking_channel(self, data):
        key = data["member"].id
        await super().create(data, key)
    async def _any_voice_state_update(self, data):
        member = data["member"]
        if member.voice is None:
            return
        id = member.id
        if self.instances.get(id):
            return
        else:
            key = data["member"].id
            await super().create(data, key)


class Leaderboard:
    def __init__(self, data, manager):
        self.bot = bot
        self.manager = manager
        # self.manager.event_manager.subscribe(self)
        self.member = data["member"]
        self.name = "leaderboard"
        self.key = self.member.id
    async def _user_left_tracking_channel(self, data):
        if data["member"] != self.member:
            return
        await self.manager.destroy(self)
    async def get_user_filter(self, data):
        default = "today_study_exclude_no_cam"
        user = await get_user(data["member"])
        if user.filter is None:
            return default
        else:
            #TODO: Test this
            return user.filter
    async def set_user_filter(self, data):
        await
    async def create(self, data):
        self.filter = await self.get_user_filter(data)
        self.channel = await self.create_private_channel()
        self.message = await self.write_and_get_message()

        # self.image_url = self.content.image.url
        # await self.update_in_channel(self.image_url)

    async def destroy(self):
        # self.manager.event_manager.unsubscribe(self)
        try:
            await self.channel.delete()
        except Exception as e:
            print(e)
    # TODO: this probably belongs to the image class
    async def update_in_channel(self, image_url):
        embed = discord.Embed()
        embed.set_image(url=image_url)
        # get the leaderboard channel
        # await channel.send(embed=embed)
        view = MyView(self)
        await self.message.edit(content="Leaderboard", embed=embed, view=view)
        pass



    # class button(discord.ui.View):
    #     def __init__(self):
    #         super().__init__()
    #         self.value = None
    #
    #         @discord.ui.button(label="Hi", style=discord.ButtonStyle.grey)
    #         async def menu1(self, button: discord.ui.Button, interaction: discord.Interaction):
    #             await interaction.response.send_message("hioo")
    async def _destroyed_instance_filter(self, instance):
        if instance.key == self.key:
            await self.manager.destroy(self)
    async def _updated_image(self, imageInstance):
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
        allowed_members = [
            366276958566481920,
            248433538938961932,
            226720984936218624
        ]
        # TODO REMOVE THIS WHEN IM DONE WITH TESTING
        # TODO  test with multiple users
        if member.id not in allowed_members:
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
        url = "https://upload.wikimedia.org/wikipedia/commons/b/b9/Youtube_loading_symbol_1_(wobbly).gif"
        try:
            self.message = await self.channel.send(url)
        except Exception as e:
            print(e)
        return self.message

class MyView(View):
    def __init__(self, lb):
        super().__init__()
        self.lb = lb
        self.filters = {
            "today_all_both_only" : {
                "custom_id": "today_all_both_only",
                "emoji": "🔥",
                "label": "cam and ss"
            },
            "today_study_exclude_no_cam" : {
                "custom_id": "today_study_exclude_no_cam",
               "emoji": "📷",
                "label": "cam or ss"
            },
            "today_all" : {
                "custom_id": "today_all",
                "emoji": "☎️",
                "label": "no cam"
            },
        }
        for filter_key in self.filters:
            self.add_item(MyButton(self.filters[filter_key], lb=self.lb))

        # self.add_item(discord.ui.Button(emoji="🔥", style=discord.ButtonStyle.grey, custom_id="hiii", label="cam & ss"))
        # self.add_item(discord.ui.Button(emoji=self.emoji, style=discord.ButtonStyle.grey, custom_id="hi", label=self.description))
        # self.add_item(discord.ui.Button(emoji="☎️", style=discord.ButtonStyle.grey, custom_id="hii", label="no cam"))
        # self.add_item(MyButton(custom_id="my_custom_id",  lb=self.lb))



class MyButton(discord.ui.Button):
    def __init__(self, filter, lb, style=discord.ButtonStyle.grey):
        super().__init__(style=style, custom_id=filter["custom_id"])
        self.emoji = filter["emoji"]
        self.custom_id = filter["custom_id"]
        self.label = filter["label"]
        self.lb = lb
        if self.lb.filter == self.custom_id:
            self.style = discord.ButtonStyle.green

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Showing {self.label} button.', delete_after=3)
        await self.lb.filter=
