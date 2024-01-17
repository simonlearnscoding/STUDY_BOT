import asyncio
from discord import Message, TextChannel
from typing import Optional
import asyncio

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
        await self.bot.register_command(self.associate)

    @app_commands.command(description="associate a VC with an activity", name="associatorree")  # "**_server rules_**" ** = bold, _=italicized
    async def associate(self, interaction: discord.Interaction) -> None:
        if not interaction.permissions.administrator:
            await interaction.response.send_message('sorry only admins can use this command for now')
        await interaction.response.send_message('hi there whats up')
        interaction_class = AssociateAnActivity(self.bot, interaction)
        await interaction_class.associate_activity()


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


class AssociateAnActivity(StringFormatting):
    def __init__(self, bot, interaction):
        self.bot = bot
        self.interaction = interaction

    @error_handler
    async def associate_activity(self):
        [user_respone_1, user_response_2, user_response_3] = await self.user_bot_interaction()
        print('user entered something wrong so nevermind')
        if user_response_3 != "y":
            return

        print('alright lets go')
        # now I need to well create activities first
        # then I need to fix the get_activity function
        # then I need to make a function that
        # deletes any association the vc has then
        # creates a db entry that links the vc to the activity

    async def user_bot_interaction(self):
        message = self.create_vc_list_message()
        vc_list = self.get_vc_list()
        activities_list = await self.get_activities_list()
        channel = self.interaction.channel
        # await self.interaction.defer()

        try:
            user_respone_1 = await self.send_message_and_wait_for_reply(message_content=message, channel=channel)
            user_response_vc = vc_list[int(user_respone_1.content) - 1]
            await channel.send(f"VC: {user_response_vc}")

            message_2 = await self.create_activities_message()
            user_response_2 = await self.send_message_and_wait_for_reply(message_content=message_2, channel=channel)
            user_response_activity = activities_list[int(user_response_2.content) - 1]
            await channel.send(f"activity: {user_response_activity}")

            message_3 = "Are you sure you want to create this connection? y/n"
            ur_3 = await self.send_message_and_wait_for_reply(message_content=message_3, channel=channel)
            user_response_3 = ur_3.content
            return [user_respone_1, user_response_2, user_response_3]

        except IndexError:
            await channel.send("Invalid option. Please select a valid option from the list.")
            return [None, None, None]
            # You can choose to handle this error in other ways, like asking the user to retry.

    # Rest of your code...

    async def create_activities_message(self):
        activities_list = await self.get_activities_list()
        activities_list_str = self.format_string_list(activities_list)
        return self.format_two_strings("What activity would you like to link to this VC?", activities_list_str)

    def create_vc_list_message(self):
        vc_list = self.get_vc_list()
        vc_list_str = self.format_string_list(vc_list)
        return self.format_two_strings("What VC would you like to link to an activity?", vc_list_str)

    async def get_activities_list(self):
        # TODO: I have to do the activities
        return ['mock activity', 'another mock activity']

    def get_vc_list(self):
        # Assuming interaction.guild is a Guild object
        guild = self.interaction.guild
        vc_list = [channel.name for channel in guild.voice_channels]
        return vc_list

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
