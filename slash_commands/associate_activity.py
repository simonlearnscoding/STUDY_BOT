import asyncio
from discord import Message, TextChannel
from typing import Optional
import asyncio
from model_managers_tortoise.table_manager import ServerSetterMixin

from tortoise_models import Channel, Activity
from discord import TextChannel
import discord
from discord import app_commands
from discord.ext import commands
# from vc import bot, server

from utils.error_handler import error_handler


class AssociateActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog has been loaded')

        # Register the slash command
        await self.bot.register_command(self.associations)
        await self.bot.register_command(self.associate)

    @app_commands.command(description="associate a VC with an activity", name="associate")  # "**_server rules_**" ** = bold, _=italicized
    async def associate(self, interaction: discord.Interaction) -> None:
        if not interaction.permissions.administrator:
            await interaction.response.send_message('sorry only admins can use this command for now')
        interaction_class = AssociateAnActivity(self.bot, interaction)
        await interaction_class.associate_activity()

    @app_commands.command(description="Show the associations", name="associations")  # "**_server rules_**" ** = bold, _=italicized
    async def associations(self, interaction: discord.Interaction) -> None:
        interaction_class = AssociateAnActivity(self.bot, interaction)
        await interaction_class.show_associations()


async def setup(bot):
    await bot.add_cog(AssociateActivity(bot))


class StringFormatting():
    @staticmethod
    def format_two_strings(str1, str2):
        formatted_output = f"```\n{str1}\n\n{str2}\n```"
        return formatted_output

    @staticmethod
    def format_string_list(strings):
        formatted_list = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(strings)])
        return f"```{formatted_list}```"


class AssociateAnActivity(StringFormatting, ServerSetterMixin):
    def __init__(self, bot, interaction):
        self.bot = bot
        self.interaction = interaction
        self.guild = self.interaction.guild

    async def get_db_entries(self):
        await self.set_server()
        self.activities = await Activity.all()
        self.channels = await Channel.filter(server=self.server_db, channel_type="Voice").all()

    async def show_associations(self):
        # TODO: Test
        await self.get_db_entries()
        channels_with_activity = [channel for channel in self.channels if channel.activity_id is not None]
        string = await self.format_channel_activity_string(channels_with_activity)
        await self.interaction.response.send_message(string)

    async def format_channel_activity_string(self, channels):
        string = "List of channels with associated activities:\n"
        for channel in channels:
            activity = await channel.activity.filter().first()
            string += f"{channel.name} - {activity.name}\n"
        return string

    def get_list_activity_names(self, db_list):
        # TODO: Test
        names = [db_item.activity.name for db_item in db_list]
        return names
        pass

    async def associate_activity(self):
        await self.get_db_entries()
        [user_respone_1, user_response_2, user_response_3] = await self.user_bot_interaction()
        print('user entered something wrong so nevermind')
        if user_response_3 != "y":
            return

        print('alright lets go')
        await self.associate(user_respone_1, user_response_2)

    async def associate(self, user_respone_1, user_response_2):
        # TODO: Test
        channel = await self.channels[int(user_respone_1) - 1]
        activity = await self.activities[int(user_response_2) - 1]
        channel.activity = activity
        await self.interaction.channel.send(f"associated {channel.name} with {activity.name}")
        await channel.save()

    async def get_channel_by_name(self, channel_name):
        # TODO: Test
        discord_channel = discord.utils.get(self.interaction.guild.channels, name=channel_name)
        return await Channel.filter(discord_id=discord_channel.id).first()

    async def get_activity_by_name(self, target_name):
        # TODO: Test
        matching_activity = next((activity for activity in self.activities if activity.name == target_name), None)
        return matching_activity

        # then I need to make a function that
        # deletes any association the vc has then
        # creates a db entry that links the vc to the activity

    async def format_message(self, first_message, db_array):
        list = self.get_list(db_array)
        list_str = self.format_string_list(list)
        return self.format_two_strings(first_message, list_str)

    def get_list(self, db_list):
        # TODO: Test
        names = [db_item.name for db_item in db_list]
        return names

    async def user_bot_interaction(self):
        message_channels = await self.format_message("What VC would you like to link to an activity?", self.channels)
        message_activities = await self.format_message("What activity would you like to link to this VC?", self.activities)
        message_3 = "Are you sure you want to create this connection? y/n"
        # await self.interaction.defer()

        channel = self.interaction.channel
        try:
            user_respone_1 = await self.send_message_and_wait_for_reply(message_content=message_channels, channel=channel)
            user_response_2 = await self.send_message_and_wait_for_reply(message_content=message_activities, channel=channel)
            user_response_3 = await self.send_message_and_wait_for_reply(message_content=message_3, channel=channel)
            return [user_respone_1.content, user_response_2.content, user_response_3.content]

        except IndexError:
            await channel.send("Invalid option. Please select a valid option from the list.")
            return [None, None, None]
            # I can choose to handle this error in other ways, like asking the user to retry.

    async def send_message_and_wait_for_reply(self, channel: TextChannel, message_content: str, timeout: Optional[float] = 60.0) -> Optional[Message]:
        try:
            bot_message = await channel.send(message_content)

            def check(m):
                return m.author == channel.guild.get_member(self.interaction.user.id) and m.channel == channel

            user_reply = await self.bot.wait_for('message', check=check, timeout=timeout)

            if user_reply:
                # Process the user's reply
                await asyncio.gather(
                    asyncio.sleep(2),  # A delay to make sure the user's message is sent before deleting
                    bot_message.delete(),
                    user_reply.delete(),
                )

            return user_reply

        except asyncio.TimeoutError:
            await channel.send("You didn't respond within the time limit.")
            return None
