import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import bot
import giphy_client
from giphy_client.rest import ApiException
from discord.client import Client
import sys
sys.path.append('/.../')

import random
import giphy_client
import asyncio

from vc import vc

Array = []
InSession = False
IsRunning = False
running = False
InLoop = False 
Giphy="QzcoyBOMjKL0v04krPNXz9A9PSJrg0oG"


class boot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def InSparta(self, member):
        if member.voice.channel.id == vc.sparta_id:
            return True


    async def wait_then_kick(self, member):

        # Making up a random number until kick
        print("kicktimer_started")
        n = random.randint(60, 360)
        print(n)
        sleeptime = n
        await asyncio.sleep(sleeptime)

        # If cam just got turned off
        if ((member.voice.self_video == False) and (member.voice.self_stream == False)):
            print("turn it on now")
            Channel = self.client.get_channel(id=839100861497606174)
            if Channel.name.startswith("Break"):  # if channel rename = Break
                "print: cam off but in break so idc"
                return
            elif Channel.name.startswith("Sesh:"):  # if channel rename = Break
                # Move member into Lions Cage
                if member.id == "744545219260842014":
                    pass
                channel = self.client.get_channel(vc.lions_cage_id)
                text_channel = self.client.get_channel(vc.lions_cage_text_id)
                DaChannel = self.client.get_channel(vc.chores_vc_id)
                
                # Print a gif for kicking
                api_instance = giphy_client.DefaultApi()
                try:
                    p = ["kick", "punch", "take out the trash",
                        "sacked", "get out", "you're fired"]
                    r = random.randint(0, (len(p) - 1))
                    a = p[r]
                    api_response = api_instance.gifs_search_get(Giphy, a, limit=5)
                    lst = list(api_response.data)
                    giff = random.choice(lst)
                    chennel = self.client.get_channel(vc.chores_vc_id)
                    await chennel.send(giff.embed_url)
                except ApiException as e:
                    print("Exception when calling Api..")

                #TODO: send a catchphrase:
                
                # Send Member to the lions Cage       
                channel = self.client.get_channel(vc.lions_cage_id)
                text_channel = self.client.get_channel(vc.lions_cage_text_id)
                await member.move_to(channel)
                await text_channel.send(f"{member.mention} funny catchphrase broken for now")
        
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        
        # IF THE SESSION STARTS
        global Array
        if before.name.startswith("-- Break") and after.name.startswith("-- Sesh:"): 
            
            # EMPTY THE ARRAY OF PEOPLE WHO MESSAGED
            # EMPTY THE ARRAY OF PEOPLE WHO MESSAGED
            print("the Array has been emptied")
            print(Array)
            Array = []
            print(Array)

            # CHECK CAM STATE OF EVERY MEMBER 
            Sparta = self.client.get_channel(vc.sparta_id)
            Members = Sparta.voice_states
            for i in range(len(Sparta.members)):
                print(Sparta.members[i].id)
                await self.wait_then_kick(Sparta.members[i])

    @commands.Cog.listener()
    #start wait then kick if cam turned off
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return    
        channel = self.client.get_channel(id=vc.sparta_id)
        if (after.self_video == False and after.self_stream == False):
            if (await self.InSparta(member)):
                print("LOL")        
                await self.wait_then_kick(member)

"""  @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == vc.gestapo:
            if (len(message.mentions) > 0):
                User = message.mentions[0]
                if await self.InSparta(User):
                    Reason = message.content.split()
                    if Reason[0].startswith("-warn"):
                        DaChannel = self.client.get_channel(vc.chores_vc_id)
                        del Reason[0]
                        if len(Reason) == 0:
                            Reason = ' '.join(Reason)
                            Reason = "no reason lol"
                        Reason = ' '.join(Reason)
                        
                        await DaChannel.send(f"{User.mention} you've been warned ) - Reason: {Reason}")

                    else:
                        del Reason[0]
                        if len(Reason) == 0:
                            Reason = ' '.join(Reason)
                            Reason = "no reason lol"
                        Reason = ' '.join(Reason)
                        "print: cam off during session smh"
                        #Kick into Lions Cage
                        channel = self.client.get_channel(vc.lions_cage_id)
                        text_channel = self.client.get_channel(vc.lions_cage_text_id)
                        DaChannel = self.client.get_channel(vc.chores_vc_id)

                        await User.move_to(channel)
                        await DaChannel.send(f"{User.mention} has been ratted out - Reason: {Reason}")
                        #TODO Replace w array
                        #TODO Add boot count            
        
            #TODO: SUBMIT A BOOT
            if message.content.startswith('!submit'):
                Reason = message.content.split()
                if len(Reason) == 0:
                    await message.channel.send(f"you need to type it like this !submit *your slogan here*") 
                    return
                del Reason[0]
                Reason = ' '.join(Reason) 
                #Sentences().append(Reason)
                #TODO Sentences append Database
                
                await message.channel.send(f"thank you, {Reason} has been added to the collection of booting phrases") 
                return
            await message.channel.purge(limit = 1)

        # Kick the Traitors who Chat while in Sparta
        if await self.InSparta(message.author):
            #Get timer VC
            Channel =self.client.get_channel(vc.timer_id) 
            global Array
            if Channel.name.startswith("-- Break"): # chatting but in break so idc
                "print: chatting but in break so idc"        
                return
            elif Channel.name.startswith("-- Sesh:"): # chatting mid sesh
                if message.content.startswith("!day"):
                    pass
                print(Array)
                if message.author.id in Array:
                    print(f"{message.author} member in array")
                    n = random.randint(1,100)
                    print(n)
                    p = 15
                    if n < p:
                    #Kick into Lions Cage
                        channel =self.client.get_channel(vc.lions_cage_id)
                        text_channel =self.client.get_channel(vc.lions_cage_text_id)
                        api_instance = giphy_client.DefaultApi()
                        try:
                            p = ["please be quiet", "you're talking too much", "just stop it", "stfu", "shush", "be quiet", "calm down"]
                            r = random.randint(0, (len(p) - 1))
                            a = p[r]
                            print(a)
                            api_response = api_instance.gifs_search_get(Giphy, a, limit=5)
                            lst = list(api_response.data)
                            giff = random.choice(lst)
                            await message.channel.send(giff.embed_url)
                        except ApiException as e:
                            print("Exception when calling Api..")
                        
                        #TODO gif stfu
                        member = message.author
                        await member.move_to(channel)

                        await text_channel.send(f"{member.mention} booted - no funny phrase for now sorrry")
                        #TODO give prisoner of war role
                else: 
                    Array.append(message.author.id)
                    print(Array)
      """




def setup(client):
   client.add_cog(boot(client))