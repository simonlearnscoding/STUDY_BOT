import uuid
import os

from PIL import Image, ImageDraw, ImageFont
from setup.bot_instance import bot

import discord

from bases.state_manager import SingletonFactoryManager
class Image_Manager_Class(SingletonFactoryManager):

    def __init__(self):
        self.instance_class = image_instance
    async def create_image(self, key, data):
        image = await self.create(key=key, instance_class=image_instance, data=data)
        return image

Dataset




Image_Manager = Image_Manager_Class()

