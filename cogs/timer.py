import discord
from discord.ext import commands
from discord.ext.commands import bot

import asyncio

from discord.client import Client
import sys

import requests

sys.path.append('/.../')
from vc import vc
from mydb import db



running = False
InLoop = False
InBreak = False


class timer(commands.Cog):

    # SETTING UP THE BOT
    def __init__(self, client):
        self.client = client
    
    # Update Timer
    async def updateEmbed(timer, Message):
        embed = discord.Embed(
            title = "Title",
            description = "This is a description",
            color = discord.Colour.blue()
        )
        embed.set_footer(text="this is a footer")
        embed.set_image(url="https://www.google.com/imgres?imgurl=https%3A%2F%2Fwallpaperaccess.com%2Ffull%2F1292603.jpg&imgrefurl=https%3A%2F%2Fwallpaperaccess.com%2Ffocus-hd&tbnid=g0SruTrJmwyIOM&vet=12ahUKEwid9uiJ5czwAhWOgKQKHV97A6MQMygEegUIARC7AQ..i&docid=HVVoV_HKTdvIEM&w=1600&h=900&q=focus%20wallpaper&client=opera-gx&ved=2ahUKEwid9uiJ5czwAhWOgKQKHV97A6MQMygEegUIARC7AQ")
        embed.add_field(name="Time", value=timer, inline=False)
        embed.add_field(name="Field Name", value="Field Value", inline=True)
        embed.add_field(name="Field Name", value="Field Value", inline=True)
        await Message.channel.edit(embed=embed)


    # Display timer    
    async def displayembed(self, message, timer):
        embed = discord.Embed(
            title="Time left: ", description=timer,
            color = discord.Colour.blue(),
        )

        embed.set_image(url="https://cdn.discordapp.com/attachments/827601223317585991/843290053107253288/1292603.jpg") 
        Message = await message.channel.send(embed=embed)
        return Message.id
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

    # THE TIMER FUNCTION IS HERE
    async def RunTimer(self, message, member, SessionTime, SessionBreak):
        # get group role to tag in message
        guild = discord.utils.find(lambda g: g.id == vc.guild_id, self.client.guilds)
        global InLoop
        global running
        if InLoop == True:
            channel = self.client.get_channel(vc.chores_vc_id)
            await message.channel.send(f'The timer is already running')
            return
        
        # Start the timer
        if member.voice is None: 
            channel = self.client.get_channel(vc.chores_vc_id)
            await message.channel.send(f'{member.mention}join Chores or Sparta first')
            return
        if member.voice.channel.id == vc.sparta_id:
            Mention = discord.utils.get(guild.roles, name="VC-Sparta")
        else:
            Mention = discord.utils.get(guild.roles, name="VC-Chores")
        #countdoiwn in session

        while True: 
            InLoop = True
            channel = self.client.get_channel(vc.chores_vc_id)
            if await self.Anyonethere(message):
                await message.channel.send(f'{Mention.mention} The Timer starts now!')
            #safetysecond
            running = True
            channel =self.client.get_channel(vc.timer_id)
            await asyncio.sleep(1) #das sind 5 sek mal 60 also 5 minute
            minutes = SessionTime
            timer = "starting"
            try: 
                if Message is not None:
                    await Message.delete()
            except:
                pass
            ID = await self.displayembed(message, timer)
            Message = print(f"bot ID is {ID}")
            Message = await message.channel.fetch_message(ID)
            await Message.pin()
            await message.channel.purge(limit = 1)
            await channel.edit(name=f"-- Sesh: {minutes}m") 
            await self.StoicQuote(message)          
            while minutes != 0 :
                minutes = minutes - 1
                if minutes % 5 == 0 and minutes != 0:
                    await channel.edit(name=f"-- Sesh: {minutes}m")  
                Seconds = 60
                if minutes % 4 == 0 and minutes != 0 and minutes % 5 != 0:

                    print(Message)
                    OldMessage = Message
                    ID = await self.displayembed(message, timer)
                    Message = print(f"bot ID is {ID}")
                    Message = await message.channel.fetch_message(ID)
                    await OldMessage.delete()
                    await Message.pin()
                    await message.channel.purge(limit = 1)
                        
                while Seconds != 0:
                    if Seconds == 60:
                        timer = f"{minutes + 1}:00"
                        Embed = discord.Embed(title="Time left: ", description=timer,
                        colour = discord.Colour.blue()
                        )
                        Embed.set_image(url="https://cdn.discordapp.com/attachments/827601223317585991/843290053107253288/1292603.jpg")                    
                        await Message.edit(embed=Embed)
                    elif Seconds == 5:
                        

                        Embed = discord.Embed(title="Time left: ", description=timer,
                        colour = discord.Colour.blue())
                        Embed.set_image(url="https://cdn.discordapp.com/attachments/827601223317585991/843290053107253288/1292603.jpg")
                        await Message.edit(embed=Embed)

                        timer = f"{minutes}:05"
                        print(timer)

                        
                        
                    else:        
                        timer = f"{minutes}:{Seconds}"
                        print(timer)
                        Embed = discord.Embed(title="Time left: ", description=timer,
                        colour = discord.Colour.blue())
                        Embed.set_image(url="https://cdn.discordapp.com/attachments/827601223317585991/843290053107253288/1292603.jpg")
                        await Message.edit(embed=Embed)
                    await asyncio.sleep(5)  
                    Seconds = Seconds -5         
                    if (running == False):
                        return           

            #Check if people still there
            if not await self.Anyonethere(message):
                await asyncio.sleep(300)
                await channel.edit(name=f"!start x y")
                return

            await message.channel.send(f'{Mention.mention} good job! The Break starts now')
            await asyncio.sleep(1) #das sind 5 sek mal 60 also 5 minute
            #TODO delete and repost the timer message maybe
        
            minutes = SessionBreak
            await channel.edit(name=f"Break: {minutes}m")
            
            while minutes != 0:

                minutes = minutes - 1
                if minutes % 5 == 0 and minutes != 0:
                    await channel.edit(name=f"Break: {minutes}m")       
                Seconds = 60

                while Seconds != 0:
                    if Seconds == 60:
                        timer = (f"{minutes + 1}:00")
                        print(timer)
                        Embed = discord.Embed(title="Break: ", description=timer,
                        colour = discord.Colour.red())
                        Embed.set_image(url="https://cdn.discordapp.com/attachments/827601223317585991/843294912128090112/9774_728.jpg")
                        await Message.edit(embed=Embed)
                    elif Seconds == 5:
                        timer = f"{minutes}:05"
                        print(timer)
                        Embed = discord.Embed(title="Break: ", description=timer,
                        colour = discord.Colour.red())
                        Embed.set_image(url="https://cdn.discordapp.com/attachments/827601223317585991/843294912128090112/9774_728.jpg")
                        await Message.edit(embed=Embed)       
                    else:        
                        timer = f"{minutes}:{Seconds}"
                        print(timer)
                        Embed = discord.Embed(title="Break: ", description=timer,
                        colour = discord.Colour.red())
                        Embed.set_image(url="https://cdn.discordapp.com/attachments/827601223317585991/843294912128090112/9774_728.jpg")
                        await Message.edit(embed=Embed)                     
                    await asyncio.sleep(5)  
                    Seconds = Seconds -5         
                if not running:
                    print("stopped running")
                    await asyncio.sleep(300) 
                    await channel.edit(name=f"!start x y")
                    running = False
                    InLoop = False
                    return

    async def StoicQuote(self, message):
        resp = requests.get('https://stoicquotesapi.com/v1/api/quotes/random')
        channel = self.client.get_channel(vc.chores_vc_id)
        if resp.status_code != 200:
            # This means something went wrong.
            #raise ApiError('GET /tasks/ {}'.format(resp.status_code))
            print("smth wnt rong")
        Resp = resp.text.split("\"")
        Quote = Resp[5]
        Author = Resp[11]
        print(Quote)
        print(Author)
        embed = discord.Embed(
            title=Author,
            description = Quote,
            color = discord.Colour.green(),                        
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/827601223317585991/843639567897591838/2d6e937af91e39fbbd8072a7059d96db.jpg") 
        await message.channel.send(embed=embed)
        return

    @commands.Cog.listener()
    async def on_message(self, message):
    
        # IGNORE IF MESSAGE FROM A BOT
        if message.author.bot:
            return

        # START A TIMER COMMAND
        if message.content.startswith('!start'):
            channel = self.client.get_channel(vc.chores_vc_id)
            msg = message.content.split(' ')
            print(len(msg))
            if (len(msg) != 3):
                output = "nope. you gotta do it like this \"!start 50 10 \" or something "
                await message.channel.send(output)
                return
            #which text channel for the bot to use
            the_channel = vc.chores_vc_id
            text_channel = self.client.get_channel(the_channel)
            SessionTime = int(msg[1])
            SessionBreak = int(msg[2])

            if (SessionBreak or SessionTime) % 5 != 0:
                output = f" \"I wAnNa WoRk FoR {int(msg[1])} minutes aNd HaVe A {int(msg[2])} minute BrEaK\" Do something that's dividable by 5 at least like 50 10"
                await channel.send(output)
                return
            """if SessionBreak or SessionTime < 1:
                output = f" \"Session and break time need to be at least 5"
                await channel.send(output)
                return"""
            # member = client.get_user(message.author.id)
            await self.RunTimer(message, message.author, SessionTime, SessionBreak)


        # END TIMER COMMAND
        if message.content.startswith('!end'):
            # get group role to tag in message
            global InLoop
            guild = discord.utils.find(lambda g: g.id == vc.guild_id, self.client.guilds)
            chores_vc = discord.utils.get(guild.roles, name="VC-Chores")
            channel = self.client.get_channel(vc.chores_vc_id)     
            
            if InLoop == False:
                await message.channel.send(f'there is no timer going on')
            else: 
                
                await message.channel.send(f'{chores_vc.mention} this function is still broken lol just leave VC and come back later (sorry)')
                #await message.channel.send(f'{chores_vc.mention} I will stop the timer now. the Voicechannel will be renamed in in 5 minutes')
                #global InLoop            
                InLoop = False
                running = False
                Leave = False
                #try: 
                #   if Message is not None:
                #      await Message.delete()
                #except:
                #   pass







def setup(client):
   client.add_cog(timer(client))


