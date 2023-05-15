import os
import uuid

from easy_pil import Canvas, Editor, Font, Text, font
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import discord
from discord import Embed


def create_leaderboard_image(data):
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

    # image.show()
    random_file_name = f"leaderboard_image_{uuid.uuid4()}.png"
    image.save(random_file_name)
    return random_file_name


async def update_image(self, img):
    embed = discord.Embed()
    channel_id = 1105618200718221424
    Url = await send_temp_message(self, channel_id, img)
    embed.set_image(url=Url)
    # get the leaderboard channel
    channel = await self.bot.fetch_channel(1105263584101015592)
    # await channel.send(embed=embed)
    message = await channel.fetch_message(1105621631159767161)
    await message.edit(content="Leaderboard", embed=embed)
    os.remove(img)
    pass


async def send_temp_message(self, channel_id, img):
    with open(img, "rb") as file:
        buffer_channel = await self.bot.fetch_channel(1105618200718221424)
        image_attachment = discord.File(file, img)
        message = await buffer_channel.send(file=image_attachment)
        Url = message.attachments[0].url
        return Url
