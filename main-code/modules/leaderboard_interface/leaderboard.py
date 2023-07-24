# from modules.leaderboard_interface.Content import Content_Manager
import uuid
from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager
from setup.bot_instance import bot
import discord
from discord.ui import Button, View
from spqrapp.models import User

class LeaderboardManager(LifeCycleManager):
    def __init__(self, datasets):
        self.instance_class = Leaderboard
        super().__init__()
        self.datasets = datasets
    async def _user_joins_tracking_channel(self, data):
        key = data["member"].id
        await super().create(data, key)

class Leaderboard():
    def __init__(self, data, manager):
        self.bot = bot
        self.manager = manager
        self.member = data["member"]
        self.name = "leaderboard"
        self.key = self.member.id
        self.changed_filter = False
        # self.avoid_update_twice = True
    async def _user_left_tracking_channel(self, data):
        if data["member"] != self.member:
            return
        await self.manager.destroy(self)

    async def change_user_filter(self, filter):
        try:
            #TODO: I have to check how many instances of the old filter there are
            # and destroy it if it was the last one
            await User.object.change_user_filter(self.member, filter)
            self.filter = filter
            #TODO: I think I am repeating myself here, I should DRY it out
            self.dataset.lb_instances.pop(self.key, None)
            self.dataset = self.manager.datasets.instances[self.filter]
            self.dataset.lb_instances[self.key] = self
            self.image_url = self.dataset.image_url
            await self.update_image_in_lb_message()
        except Exception as e:
            print(e)
    async def create(self, data):
        self.channel = await self.create_private_channel()
        self.filter = await User.object.get_user_filter(data)
        # print(self.manager.datasets.instances)
        self.dataset = self.manager.datasets.instances[self.filter]
        self.image_url = self.dataset.image_url
        self.message = await self.write_and_get_message()
        await self.update_image_in_lb_message()
        self.dataset.lb_instances[self.key] = self


    async def destroy(self):
        await self.channel.delete()
        self.dataset.lb_instances.pop(self.key, None)

    async def _updated_image(self, data_set):
        # I should move this one to the lb manager to improve performance probably
        #TODO: manage with different subscribers
        if data_set.key != self.filter:
            return
        await self.update_image_in_lb_message()
        
    async def update_image_in_lb_message(self):
            try:
                """
                this is to make sure the update never happens right 
                after the user just changed the filter because that would be 
                annoying
                """

                # I might put it back in later but for now I just gotta check some stuff

                # if self.changed_filter == True:
                #     self.changed_filter = False
                #     return
                self.dataset = self.manager.datasets.instances[self.filter]
                self.image_url = self.dataset.image_url
                embed = discord.Embed()
                embed.set_image(url=self.image_url)
                values = self.filter.split('-')
                def spacer_button():
                    spacer_button = {
                        "custom_id": str(uuid.uuid4()),
                        "label": "_"

                    }
                    return spacer_button
                buttons_type = [
                    {
                        str(uuid.uuid4()) : spacer_button(),
                        "today" : {
                            "custom_id": "today",
                            "emoji": "📅",
                            "label": "today.........."
                        },
                        "this_week" : {
                            "custom_id": "this_week",
                            "emoji": "📆",
                            "label": "this week..."
                        },
                        "this_month": {
                            "custom_id": "this_month",
                            "emoji": "🗓️",
                            "label": "this month"
                        },
                        str(uuid.uuid4()) : spacer_button(),
                    },
                    {
                        str(uuid.uuid4()): spacer_button(),
                        "study": {
                            "custom_id": "study",
                            "emoji": "📖",
                            "label": "study only.."
                        },
                        "all_activities": {
                            "custom_id": "all_activities",
                            "emoji": "👣",
                            "label": "all activities "
                        },
                        str(uuid.uuid4()): spacer_button(),
                        str(uuid.uuid4()): spacer_button(),

                    },
                    {
                        str(uuid.uuid4()): spacer_button(),
                        "both_only": {
                        "custom_id": "both_only",
                        "emoji": "🔥",
                        "label": "cam and ss"
                    },
                    "exclude_no_cam": {
                        "custom_id": "exclude_no_cam",
                        "emoji": "📷",
                        "label": "cam or ss....."
                    },
                    "all_types": {
                        "custom_id": "all_types",
                        "emoji": "☎️",
                        "label": "no cam"
                    },
                    str(uuid.uuid4()): spacer_button(),

                    },
                ]

                # Then in your main code:
                buttons = []
                for i, button_row in enumerate(buttons_type):
                    for button in button_row.values():
                        buttons.append(MyButton(self, button, values[i], i))
                main_view = MainView(buttons)
                await self.message.edit(content="", embed=embed, view=main_view)
            except Exception as e:
                print(e)

    async def create_private_channel(self):
        member = self.member
        # uncomment this if you want to only make the lb show up to trusted members!
        # allowed_members = [
        #     366276958566481920,
        #     248433538938961932,
        #     476139043768500227,
        #     226720984936218624,
        #     508711391826280451
        # ]
        # # TODO REMOVE THIS WHEN IM DONE WITH TESTING
        # if member.id not in allowed_members:
        #     return

        guild = self.bot.get_guild( 789814373434654731 )  # LATER: I will need to make this scalable if I want to use my bot for multiple servers
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
        try:
            # self.message = await self.channel.send(".")
            self.message = await self.channel.send(self.image_url)

        except Exception as e:
            print(e)
        return self.message



class RowView(View):
    def __init__(self, buttons, filter_value):
        super().__init__()
        for button in buttons.values():
            self.add_item(MyButton(button, filter_value))

class MainView(View):
    def __init__(self, buttons):
        super().__init__()
        for button in buttons:
            self.add_item(button)

# # class MyView(View):
#
#     def __init__(self, buttons, filter_value):
#         super().__init__()
#         for button in buttons.values():
#             self.add_item(MyButton(button, filter_value))


class MyButton(discord.ui.Button):
    def __init__(self, lb, button, filter_value, i, style=discord.ButtonStyle.grey):
        self.lb = lb
        self.i = i
        self.filter_value = filter_value
        disabled = False
        if button["label"] == '_':
            disabled = True
        super().__init__(style=style, custom_id=button["custom_id"], disabled=disabled)
        if button.get("emoji"):
            self.emoji = button["emoji"]
        self.custom_id = button["custom_id"]
        self.label = button["label"]
        if filter_value == self.custom_id:
            self.style = discord.ButtonStyle.green

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            self.updated_filter = False
            values = self.lb.filter.split('-')
            values[self.i] = self.custom_id
            new_filter = '-'.join(values)
           #TODO: I have to change only one thing not all but how...
            await self.lb.change_user_filter(new_filter)
            self.updated_filter = True
        except Exception as e:
            print(e)
