import discord
from discord.ext import commands, tasks
import asyncio
import sys
sys.path.append('/.../')

from mydb import db
from cogs.vc import vc
from easy_pil import Editor, load_image_async, Font, Canvas
from cogs.heatmap import heatmap
from discord import File



class levels(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def checkNewLevel(member, currentLevel, experience):

        # Calculate Levels List
        levels = {1: 100}
        for i in range(2, 100):
            levels[i] = round(((levels[i - 1] + 100) * 1.06) / 10) * 10

        # calculate current level
        i = 1
        UserLevel = 0
        while experience > levels[i]:
            UserLevel = UserLevel + 1
            i = i + 1


        if UserLevel > currentLevel:

            try:
                  channel = await member.create_dm()
                  message = await channel.send(f"good job, {member.mention}! you just reached level {UserLevel}!")
            except:
                pass

            # update user.lvl
            sql = "UPDATE users.user SET LVL = %s WHERE ID = %s"
            val = (UserLevel, member.id)
            db.cur.execute(sql, val)
            db.mydb.commit()

            socialRank = ["Gladiator", "Freedman", "Plebeian", "Equestrian", "Patrician", "Senator", "Emperor"]
            levelNum = [2, 5, 10, 20, 30, 40, 50]

            #check if new Rank
            for i in range(len(levelNum)):
                if UserLevel == levelNum[i]:
                    try:
                        role = discord.utils.get(member.guild.roles, name=socialRank[i - 1])
                        await member.remove_roles(role)
                    except:
                        pass
                    role = discord.utils.get(member.guild.roles, name=socialRank[i])
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith('!day'):
            id = message.author.id
            xp, lvl = await workaround.selectXPLVL(id)
            # message = await message.channel.send(f"xp: {xp}! Level: {lvl}!")

            await workaround.checkNewLevel(message.author, lvl, xp)
            # Calculate Levels List
            levels = {1: 100}
            for i in range(2, 100):
                levels[i] = round(((levels[i - 1] + 100) * 1.06) / 10) * 10

            current_lvl = list(levels)[(lvl - 1)]
            next_lvl = list(levels)[(lvl)]

            curlvlxp = levels[(lvl)]
            nextlvlxp = levels[(lvl + 1)]

            missingxp = nextlvlxp - curlvlxp
            alreadydone = (xp - curlvlxp)
            percentage = round((alreadydone / missingxp) * 100)
            if percentage < 0:
                percentage = 0

            print(f" {message.author.name} current level: {current_lvl}  next level: {next_lvl}  {nextlvlxp}")
            print(f"{percentage}%")
            await workaround.displayMessage(message, xp, lvl, nextlvlxp, percentage)
            if message.channel.id == (vc.lions_cage_text_id):
                pass
            else:
                try:
                    await message.delete()
                except:
                    print("someone wants to know it lol")
                    pass


    async def giveXP(member, time, Activity):

        xp = int(round(time / 5.0) * 5.0)
        contentplus = ""
        if Activity != "STUDY":
            xp, contentplus = await levels.multiplier(member, Activity, time, xp)
        content = f"{member.name}, {Activity.title()} for {int(time)} minutes! {contentplus}"

        #create embed if in vc for more than 5m
        if time > 5:
            await levels.popupMessage(member, xp, content)


        await levels.addXP(member, xp)


    async def popupMessage(member, xp, content):
        sleeptime = 3
        Embed = discord.Embed()
        Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
        Embed.add_field(
            name=f"{content}",
            value=f"+ {xp}xp",
            inline=False)
        channel = levels.checkUserVoice(member)
        message = await channel.send(embed=Embed)
        if member.voice is not None:
            await asyncio.sleep(sleeptime)
            await message.delete()

    def getActivity(Activity, id):
        sql = f"SELECT {Activity} FROM users.daily WHERE ID = {id}"
        db.cur.execute(sql, )
        return db.cur.fetchone()

    def checkifFirst(member, Activity):
        result = levels.getActivity(Activity, member.id)
        if result[0] == 0:
            return True
        else:
            return False

    def checkUserVoice(member):
        if member.voice is None:
            return vc.bot_spam
        else:
            return vc.vc_chat

    async def multiplier(member, Activity, time, xp):
        if Activity == "MEDITATION":
            xp = xp * 2
        if levels.checkifFirst(member, Activity):
            xp = xp + 15
            contentplus = "+15 xp for doing it today!"
            channel = levels.checkUserVoice(member)
            await heatmap.commandHeatmap(Activity, channel, member)

        else:
            contentplus = ""
        return xp, contentplus

    # Calculates the level the user is currently on
    def userLevelCalculate(xp, levels):
        i = 1
        UserLevel = 0
        while xp > levels[i]:
            UserLevel = UserLevel + 1
        return UserLevel
    # Updates DB if user Reached a Nev Level

    async def selectXPLVL(id):

        try:
            sql = "SELECT XP, LVL FROM users.user WHERE ID = %s"
            val = (id, )
            db.cur.execute(sql, val)
            result = db.cur.fetchone()
            lvl = result[1]
        except:
            print(f"{id} maybe not in db yet?")
            return

        if lvl is None:
            sql = "UPDATE users.user SET LVL = 1 WHERE ID = %s"
            val = (id,)
            db.cur.execute(sql, val)
            db.mydb.commit()

            sql = "SELECT XP, LVL FROM users.user WHERE ID = %s"
            val = (id,)
            db.cur.execute(sql, val)
            result = db.cur.fetchone()
        return result[0], result[1]

    async def addXP(member, xp):
        if member.bot:
            return
        print(f"{member.name} - {xp}")
        sql = "UPDATE users.user SET XP = XP + %s WHERE ID = %s"
        val = (xp, member.id)
        db.cur.execute(sql, val)
        db.mydb.commit()
        try:
            xp, lvl = await levels.selectXPLVL(member.id)
            await levels.checkNewLevel(member, lvl, xp)
        except:
            print(f"{member} couldnt update level")

    async def displayMessage(message, xp, lvl, nextlvlxp, percentage):

        #Chosen Fonts
        Augustus = Font(vc.Augustus, size=28)
        SmallFont = Font(vc.SmallFont, size=24)
        SmallerFont = Font(vc.SmallerFont, size=16)

        canvas = Canvas((900, 300), color="black")

        profile = await load_image_async(str(message.author.avatar.url))
        profile = await load_image_async(str(message.author.avatar.url))

        profile = Editor(profile).resize((140, 140)).circle_image()
        editor = Editor(canvas)
        pic = await load_image_async("https://c4.wallpaperflare.com/wallpaper/193/219/663/black-background-marcus-aurelius-statue-hd-wallpaper-preview.jpg")
        background = Editor(pic).resize((550, 300))
        square = Canvas((500, 500), "white")
        square = Editor(square)
        square.rotate(30, expand=True)
        background.paste(square.image, (600, -250))
        background.paste(profile.image, (16, 16))

        background.rectangle((30, 240), width=490, height=35, fill="white", radius=9)
        background.bar((30, 240), max_width=490, height=35, percentage=percentage, fill="#84DCCF", radius=9)   #353a47
        background.text((200, 25), str(f"{message.author.name}"), font=Augustus, color="white")
        background.rectangle((200, 60), width=220, height=1, fill="#adf7b6", )

        background.text((40, 210), f"Level: {lvl}", font=SmallFont, color="white")
        background.text((380, 215), f"XP: {xp}/{nextlvlxp}", font=SmallerFont, color="white")

        file = discord.File(fp=background.image_bytes, filename="card.png")
        Message = await message.channel.send(file=file)

        if message.channel.id == (vc.lions_cage_text_id):
            return
        else:
            await asyncio.sleep(7)
            await Message.delete()


class workaround:
    async def selectXPLVL(id):
        return await levels.selectXPLVL(id)

    async def checkNewLevel(member, currentLevel, experience):
        return await levels.checkNewLevel(member, currentLevel, experience)
    async def displayMessage(message, xp, lvl, nextlvlxp, percentage):
        return await levels.displayMessage(message, xp, lvl, nextlvlxp, percentage)

async def setup(client):
    await client.add_cog(levels(client))

async def teardown(client):
    return

