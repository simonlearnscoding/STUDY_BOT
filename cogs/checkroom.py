import vc
import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import bot

class checkroom():
    async def InSparta(self, member):
        if member.voice.channel.id == vc.sparta_id:
            return True

    async def Anyonethere(self, message):
        global running
        sparta = self.client.get_channel(vc.sparta_id)
        study_vc = self.client.get_channel(vc.study_id)
        if not bool(sparta.voice_states):
            print("no one in sparta")
            if not bool(study_vc.voice_states):
                print("no one in study either")
                running = False
                return False
        return True
