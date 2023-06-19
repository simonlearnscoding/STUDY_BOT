import asyncio
import uuid
import os
import requests
from io import BytesIO
from setup.bot_instance import bot
from PIL import Image, ImageDraw, ImageFont, ImageOps
from setup.bot_instance import bot
import datetime

import discord
from modules.leaderboard_interface.lifecycle_manager import LifeCycleManager
class ImageManager(LifeCycleManager):
    def __init__(self):
        self.instance_class = ImageClass
        super().__init__()


    async def _changed_filter(self, instance):
        image = self.instances[instance.filter]
        await instance.update_image_in_lb_message(image)

    async def _created_instance_leaderboard(self, instance):
        image = self.instances[instance.filter]
        #this is suboptimal because it creates interdependency but I dont know of another way to solve this for now
        await instance.update_image_in_lb_message(image)
    async def _created_instance_dataset(self, data):

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
        self.key = dataSet.key
        self.filter = dataSet.filter
        self.data = dataSet.data
    async def create(self, data):
        await self.create_image(data)
        await self.manager.event_manager.publish("_updated_image", self)

    async def _updated_dataset(self, data):
        if self.key != data.key:
            return
        await self.create_image(data)
        await self.manager.event_manager.publish("_updated_image", self)
    async def create_image(self, data):
        data = data.data


        image_filename = self.create_leaderboard_image(data)
        self.url = await self.send_temp_message(image_filename)

    def draw_current_date_on_image(self, draw, font, padding, image_width):
        # Get current date
        current_date = datetime.datetime.now().strftime("%d.%m")
        # Calculate the text width and height
        date_text_width, date_text_height = draw.textsize(current_date, font=font)
        # Position of the date text (top-right corner, with padding)
        date_position = (image_width - date_text_width - padding, padding - 20)
        # Draw the date
        draw.text(date_position, current_date, fill=(230, 230, 230), font=font)

    async def send_temp_message(self, image_filename):
         temp_channel_id = 1105618200718221424 #TODO: this should get the channel by name instead
         with open(image_filename, "rb") as file:
            buffer_channel = await self.bot.fetch_channel(temp_channel_id)
            image_attachment = discord.File(file, image_filename)
            message = await buffer_channel.send(file=image_attachment)
            #sleep one sec to avoid getting rate limited
            await asyncio.sleep(1)
            Url = message.attachments[0].url
            os.remove(image_filename)
            return Url

    #TODO: I need to call this
    # and the update in channel every time that the data changed
    def calculate_total_pixel_space(self, avatar_x_position, time_x_position):
        total_pixel_space = time_x_position - avatar_x_position - 16
        return total_pixel_space

    def calculate_pixel_per_segment(self, total_pixel_space, num_segments=96):
        pixel_per_segment = total_pixel_space // num_segments
        return pixel_per_segment

    def create_green_shades(self):
        start_color = (49, 51, 56)  # 0% color
        end_color = (117, 202, 177)  # 100% color

        green_shades = [
            (
                start_color[0] + int(i * (end_color[0] - start_color[0]) / 10),
                start_color[1] + int(i * (end_color[1] - start_color[1]) / 10),
                start_color[2] + int(i * (end_color[2] - start_color[2]) / 10)
            )
            for i in range(10)
        ]
        green_shades[0] = start_color
        green_shades[9] = end_color

        return green_shades


    def draw_line_segments(self, draw, user_data, avatar_x_position, time_x_position, ROW_HEIGHT):
        total_pixel_space = self.calculate_total_pixel_space(avatar_x_position, time_x_position)
        pixel_per_segment = self.calculate_pixel_per_segment(total_pixel_space)
        green_shades = self.create_green_shades()
        line_thickness = 20  # Set the thickness of the line here

        for i, segment_percentage in user_data["segments"].items():
            line_color = green_shades[min(9, int(segment_percentage / 10))]

            segment_start_x = avatar_x_position + i * pixel_per_segment
            segment_end_x = segment_start_x + pixel_per_segment

            # Calculate the top and bottom y coordinates for the thick line
            half_thickness = line_thickness / 2
            line_top = user_data["y_position"] + ROW_HEIGHT / 2 - half_thickness
            line_bottom = line_top + line_thickness

            # Draw a rectangle as a thick line
            draw.rectangle([(segment_start_x, line_top), (segment_end_x, line_bottom)],
                           fill=line_color)

    def draw_current_time_line(self, draw, IMAGE_WIDTH, IMAGE_HEIGHT, avatar_x_position,  pixel_per_segment, PADDING, first_row_y, last_row_y ):
        # Get current time
        now = datetime.datetime.now()

        # Convert current time to segments
        current_time_segments = now.hour * 4 + now.minute // (60 // 4)

        # Calculate current time position in pixels
        current_time_position = current_time_segments * pixel_per_segment + avatar_x_position

        # Check if the current time position exceeds the image width, if so cap it to the image width
        current_time_position = min(current_time_position, IMAGE_WIDTH - PADDING)

        # Draw a vertical line at the current time position
        draw.line((current_time_position, first_row_y, current_time_position, last_row_y), fill=(80, 150, 120), width=2)
    def create_leaderboard_image(self, data):

        ROW_HEIGHT = 80

        TIMELINE_HEIGHT = 60  # Height for the timeline row (increased for more space)
        IMAGE_HEIGHT = ROW_HEIGHT * 10 + TIMELINE_HEIGHT + 20  # Add space for the timeline row

        IMAGE_WIDTH = int(IMAGE_HEIGHT * 4 / 3)
        PADDING = 40
        SEGMENTS_PER_HOUR = 4  # Modify this to match your settings
        avatar_x_position = 24 + 40  # Avatar's x position (24 + width of avatar)

        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        timeline_font = ImageFont.truetype(font_path, size=16)  # Further reduce font size for timeline
        row_font = ImageFont.truetype(font_path, size=24)  # Font size for row text

        image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(49, 51, 56))
        draw = ImageDraw.Draw(image)

        # Calculate the total pixel space and pixel per segment
        total_pixel_space = self.calculate_total_pixel_space(avatar_x_position, IMAGE_WIDTH - PADDING)
        pixel_per_segment = self.calculate_pixel_per_segment(total_pixel_space)

        # Calculate the number of segments in 24 hours
        segments_in_24_hours = 24 * SEGMENTS_PER_HOUR

        # Draw the timeline row
        for i in range(0, segments_in_24_hours, SEGMENTS_PER_HOUR):
            hour = i // SEGMENTS_PER_HOUR
            # Draw a small dot for every hour
            dot_radius = 2
            dot_center = (i * pixel_per_segment + avatar_x_position, TIMELINE_HEIGHT - dot_radius * 2)
            draw.ellipse(
                [dot_center[0] - dot_radius, dot_center[1] - dot_radius,
                 dot_center[0] + dot_radius, dot_center[1] + dot_radius],
                fill=(255, 255, 255)
            )
            if hour % 3 == 0:  # Only show every third hour
                hour_label = f"{hour if hour < 13 else hour - 12}{'am' if hour < 13 else 'pm'}"
                draw.text(
                    (dot_center[0], dot_center[1] - dot_radius * 10),  # Draw above the dot
                    hour_label,
                    fill=(255, 255, 255),
                    font=timeline_font,
                    anchor="ms",  # center align the text
                )

        for i, row_data in enumerate(data):
            y_position = i * ROW_HEIGHT + 5 + TIMELINE_HEIGHT  # shift rows down to accommodate timeline
            row_data["y_position"] = y_position
            # Draw a rectangle around the row
            draw.rectangle(
                [(0, y_position), (IMAGE_WIDTH, y_position + ROW_HEIGHT)],
                outline=(152, 153, 156)
            )

            # # Draw small grey dots for every hour
            # for j in range(0, segments_in_24_hours, SEGMENTS_PER_HOUR):
            #     dot_center = (j * pixel_per_segment + avatar_x_position, y_position + ROW_HEIGHT - dot_radius * 2)
            #     draw.ellipse(
            #         [dot_center[0] - dot_radius, dot_center[1] - dot_radius,
            #          dot_center[0] + dot_radius, dot_center[1] + dot_radius],
            #         fill=(150, 150, 150)  # fill with grey color
            #     )

            time_text = f"{row_data['hours']:02}:{row_data['minutes']:02}"

            time_text_width, time_text_height = draw.textsize(time_text, font=row_font)
            x_position_time = IMAGE_WIDTH - time_text_width - PADDING
            y_position_time_centered = y_position + (ROW_HEIGHT - time_text_height) // 2

            fill = (255, 255, 255)

            if row_data["online"]:
                fill = (117, 202, 177)
            draw.text(
                (x_position_time, y_position_time_centered),
                time_text,
                fill=fill,
                font=row_font,
            )

            # Fetch the avatar image
            response = requests.get(row_data["avatar"])
            avatar_image = Image.open(BytesIO(response.content))

            # Resize the avatar image
            avatar_image = avatar_image.resize((40, 40))
           # If you want the avatar to be circular
            mask = Image.new('L', avatar_image.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0) + avatar_image.size, fill=255)
            avatar_image = ImageOps.fit(avatar_image, mask.size, centering=(0.5, 0.5))
            avatar_image.putalpha(mask)
            # Calculate the center of the row
            row_center = y_position + ROW_HEIGHT // 2

            # Calculate the new y_position for the avatar image
            avatar_y_position = row_center - avatar_image.height // 2



            # Paste the avatar image onto the leaderboard image
            image.paste(avatar_image, (24, avatar_y_position), avatar_image)
            # Paste the avatar image onto the leaderboard image
            # image.paste(avatar_image, (10, y_position), avatar_image)
            self.draw_line_segments(draw, row_data, 24 + avatar_image.width, x_position_time, ROW_HEIGHT)

        first_row_y = TIMELINE_HEIGHT + 5  # y-coordinate of the start of the first user row
        last_row_y = first_row_y + len(data) * ROW_HEIGHT  # y-coordinate of the end of the last user row

        self.draw_current_time_line(draw, IMAGE_WIDTH, IMAGE_HEIGHT, avatar_x_position, pixel_per_segment, PADDING, first_row_y, last_row_y)
        self.draw_current_date_on_image(draw, row_font, PADDING, IMAGE_WIDTH)

        random_file_name = f"leaderboard_image_{uuid.uuid4()}.png"
        image.save(random_file_name, dpi=(300, 300))
        return random_file_name

