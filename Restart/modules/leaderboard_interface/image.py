
import uuid
import os

from setup.bot_instance import bot
from PIL import Image, ImageDraw, ImageFont
from setup.bot_instance import bot

import discord
from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager, destroyWhenNoLb
class ImageManager(LifeCycleManager):
    def __init__(self):
        self.instance_class = ImageClass
        super().__init__()


    async def created_instance_dataset(self, data):
        """
        set filter name as key and create the object
        """
        key = data.key
        await super().create(data, key)


class ImageClass:

    def __init__(self, dataSet, manager):
        self.manager = manager
        self.name = "image"
        self.bot = bot
        # self.filter = data.manager.instances
        self.key = dataSet.key
        self.filter = dataSet.filter
        self.data = dataSet.data
    async def create(self, data):
        await self.create_image(data)
        pass
    async def updated_dataset(self, data):
        await self.create_image(data)
        await self.manager.event_manager.publish("updated_image", self)
    async def create_image(self, data):
        data = data.data
        image_filename = self.create_leaderboard_image(data)
        self.url = await self.send_temp_message(image_filename)

    async def destroyed_instance_filter(self, instance):
        if instance.key == self.key:
            await self.manager.destroy(self)

    async def send_temp_message(self, image_filename):
#         #TODO: Test what happens if this gets spammed
         temp_channel_id = 1105618200718221424 #LATER: change if you want to scale multiple servers
         with open(image_filename, "rb") as file:
            buffer_channel = await self.bot.fetch_channel(temp_channel_id)
            image_attachment = discord.File(file, image_filename)
            message = await buffer_channel.send(file=image_attachment)
            Url = message.attachments[0].url
            os.remove(image_filename)
            return Url

    #TODO: I need to call this
    # and the update in channel every time that the data changed
    def create_leaderboard_image(self, data):
        ROW_HEIGHT = 40
        IMAGE_WIDTH = 600
        IMAGE_HEIGHT = ROW_HEIGHT * len(data) + 10

        # Create a new image with a dark background
        image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(30, 30, 30))
        draw = ImageDraw.Draw(image)

        # Use a default font provided by Pillow
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        font = ImageFont.truetype(font_path, size=20)

        for i, row_data in enumerate(data):
            y_position = i * ROW_HEIGHT + 5

            # Calculate the center alignment for the text
            text_width, text_height = draw.textsize(row_data["nick"], font=font)
            x_position = 10
            y_position_centered = y_position + (ROW_HEIGHT - text_height) // 2

            # Draw the text with white font
            draw.text(
                (x_position, y_position_centered),
                row_data["nick"],
                fill=(255, 255, 255),
                font=font,
            )

            time_text = f"{row_data['hours']}h {row_data['minutes']}m"

            # Calculate the center alignment for the time text
            time_text_width, time_text_height = draw.textsize(time_text, font=font)
            x_position_time = (
                    540 - time_text_width
            )  # Adjust the x position to move the time text closer to the green dot
            y_position_time_centered = y_position + (ROW_HEIGHT - time_text_height) // 2

            # Draw the time text with white font
            draw.text(
                (x_position_time, y_position_time_centered),
                time_text,
                fill=(255, 255, 255),
                font=font,
            )

            if row_data["online"]:
                # Create a green circular online indicator
                circle_radius = 10
                circle_center = (
                    580,
                    y_position + ROW_HEIGHT // 2,
                )  # Adjust the x position to move the green dot closer to the time text
                online_indicator = Image.new("RGBA", (circle_radius * 2, circle_radius * 2))
                draw_indicator = ImageDraw.Draw(online_indicator)
                draw_indicator.ellipse(
                    [(0, 0), (circle_radius * 2, circle_radius * 2)], fill=(0, 255, 0)
                )
                image.paste(
                    online_indicator,
                    (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
                )

        random_file_name = f"leaderboard_image_{uuid.uuid4()}.png"
        image.save(random_file_name)
        return random_file_name
"""
legacy code
"""
# class image_instance:
#     def __init__(self):
#         self.bot = bot
#     async def initialize(self, key, data):
#         self.name = key
#         image_filename = self.update_leaderboard_image(data)
#         self.url = await self.send_temp_message(image_filename)
#
#     async def send_temp_message(self, image_filename):
#         #TODO: Test what happens if this gets spammed
#         temp_channel_id = 1105618200718221424
#         with open(image_filename, "rb") as file:
#             buffer_channel = await self.bot.fetch_channel(temp_channel_id)
#             image_attachment = discord.File(file, image_filename)
#             message = await buffer_channel.send(file=image_attachment)
#             Url = message.attachments[0].url
#             os.remove(image_filename)
#             return Url
#
#     #TODO: I need to call this
#     # and the update in channel every time that the data changed
#     def update_leaderboard_image(self, data):
#         ROW_HEIGHT = 40
#         IMAGE_WIDTH = 600
#         IMAGE_HEIGHT = ROW_HEIGHT * len(data) + 10
#
#         # Create a new image with a dark background
#         image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(30, 30, 30))
#         draw = ImageDraw.Draw(image)
#
#         # Use a default font provided by Pillow
#         font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
#         font = ImageFont.truetype(font_path, size=20)
#
#         for i, row_data in enumerate(data):
#             y_position = i * ROW_HEIGHT + 5
#
#             # Calculate the center alignment for the text
#             text_width, text_height = draw.textsize(row_data["nick"], font=font)
#             x_position = 10
#             y_position_centered = y_position + (ROW_HEIGHT - text_height) // 2
#
#             # Draw the text with white font
#             draw.text(
#                 (x_position, y_position_centered),
#                 row_data["nick"],
#                 fill=(255, 255, 255),
#                 font=font,
#             )
#
#             time_text = f"{row_data['hours']}h {row_data['minutes']}m"
#
#             # Calculate the center alignment for the time text
#             time_text_width, time_text_height = draw.textsize(time_text, font=font)
#             x_position_time = (
#                     540 - time_text_width
#             )  # Adjust the x position to move the time text closer to the green dot
#             y_position_time_centered = y_position + (ROW_HEIGHT - time_text_height) // 2
#
#             # Draw the time text with white font
#             draw.text(
#                 (x_position_time, y_position_time_centered),
#                 time_text,
#                 fill=(255, 255, 255),
#                 font=font,
#             )
#
#             if row_data["online"]:
#                 # Create a green circular online indicator
#                 circle_radius = 10
#                 circle_center = (
#                     580,
#                     y_position + ROW_HEIGHT // 2,
#                 )  # Adjust the x position to move the green dot closer to the time text
#                 online_indicator = Image.new("RGBA", (circle_radius * 2, circle_radius * 2))
#                 draw_indicator = ImageDraw.Draw(online_indicator)
#                 draw_indicator.ellipse(
#                     [(0, 0), (circle_radius * 2, circle_radius * 2)], fill=(0, 255, 0)
#                 )
#                 image.paste(
#                     online_indicator,
#                     (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
#                 )
#
#         random_file_name = f"leaderboard_image_{uuid.uuid4()}.png"
#         image.save(random_file_name)
#         return random_file_name
