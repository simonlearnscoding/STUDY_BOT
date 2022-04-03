import discord
from discord import client
from mydb import db
from discord.ext import commands, tasks
import sys
import asyncio
import time
from cogs.levels import levels
from cogs.heatmap import heatmap
import datetime
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "*", intents = intents)


sys.path.append('/.../')
from cogs.vc import vc



class challenge(commands.Cog):
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    monthday = time.localtime().tm_mday
    missing1 = []
    done1 = []
    missing2 = []
    done2 = []

    new_line = '\n'
    emoji = '\N{RAISED HAND}'
    switch = True
    switch2 = True

    def __init__(self, client):
        self.client = client






    async def removeRole(self, userID, challengeID):

            member = vc.guild.get_member(userID)
            if challengeID == 1:
                role = discord.utils.get(member.guild.roles, id=vc.challenge_role_1)
                await member.remove_roles(role)
            elif challengeID == 2:
                role = discord.utils.get(member.guild.roles, id=vc.challenge_role_2)
                try:
                    await member.remove_roles(role)
                except:
                    name = member.name
                    member = vc.guild.get_member(userID)
                    content = f"{name} lost the challenge {challengeID}"
                    channel = await member.create_dm()

                    await channel.send(content)
            else:
                print("type that from a challenge channel pls")

    def SetToMissing(self):
        sql = "UPDATE users.challenge SET donetoday = 0;"
        db.cur.execute(sql)
        db.mydb.commit()
    def emptyArrays(self):
        challenge.done1 = []
        challenge.done2 = []
        challenge.missing1 = []
        challenge.missing2 = []
    def FillEmptyArrays(self):
        sql = "SELECT username, challengeId FROM users.challenge WHERE donetoday = 0"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        for i in range(len(result)):
            if result[i][1] == 1:
                challenge.missing1.append(result[i][0])
            elif result[i][1] == 2:
                challenge.missing2.append(result[i][0])
        print(challenge.missing1)
        print(challenge.missing2)
    def FillDoneArrays(self):
        sql = "SELECT username, challengeId FROM users.challenge WHERE donetoday = 1"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        for i in range(len(result)):
            if result[i][1] == 1:
                challenge.done1.append(result[i][0])
            elif result[i][1] == 2:
                challenge.done2.append(result[i][0])
        print(challenge.done1)
        print(challenge.done2)
    def updateArrays(self):
        challenge.emptyArrays(self)
        challenge.FillEmptyArrays(self)
        challenge.FillDoneArrays(self)

    def getChannel(result):
        if result == 1:
            return vc.challenge_1
        elif result == 2:
            return vc.challenge_2

    def startDay(self):
        challenge.SetToMissing(self)
        challenge.updateArrays(self)
    async def reminder(self, guild):

        sql = "SELECT * from users.challenge WHERE username is not NULL AND donetoday != 1"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        for i in range(len(result)):
            member = vc.guild.get_member(result[i][0])
            channel = challenge.getChannel([i][4])
            if result[i][4] == 1:
                message = await challenge.fillMessages(self, 3)
            elif result[i][4] == 2:
                message = await challenge.fillMessages(self, 4)
            try:
                content = f"Don't forget to complete your challenge {channel.name} today! {challenge.new_line}You can go to this message and react with {challenge.emoji} when you did it! {message.jump_url}"
                channel = await member.create_dm()
                await channel.send(content)
            except:
                pass

    async def MakeMessage(self, channel):
        Embed = discord.Embed()
        Embed.add_field(name=f"Day {time.localtime().tm_mday}", value=f"...", inline=False)
        if channel == vc.challenge_1:
            Embed.add_field(name="Done: ", value=f"{challenge.done1}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing1}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message1 = await channel.send(embed=Embed)
            challenge.MessageGetId(self, challenge.Message1, 3)
            challenge.Message1 = await challenge.fillMessages(self, 3)
            await challenge.Message1.add_reaction(challenge.emoji)

        elif channel == vc.challenge_2:
            Embed.add_field(name="Done: ", value=f"{challenge.done2}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing2}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message2 = await channel.send(embed=Embed)
            challenge.MessageGetId(self, challenge.Message2, 4)
            challenge.Message2 = await challenge.fillMessages(self, 4)
            await challenge.Message2.add_reaction(challenge.emoji)

    async def updateMessage(self, channel):

        if channel == vc.challenge_1:
            Embed = discord.Embed()
            Embed.add_field(name=f"Day {time.localtime().tm_mday}", value=f"...", inline=False)
            challenge.updateArrays(client)
            Embed.add_field(name="Done: ", value=f"{challenge.done1}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing1}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message1 = await challenge.fillMessages(self, 3)
            await challenge.Message1.edit(embed=Embed)

        elif channel == vc.challenge_2:
            Embed = discord.Embed()
            Embed.add_field(name=f"Day {time.localtime().tm_mday}", value=f"...", inline=False)
            challenge.updateArrays(client)
            Embed.add_field(name="Done: ", value=f"{challenge.done2}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing2}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message2 = await challenge.fillMessages(self, 4)
            await challenge.Message2.edit(embed=Embed)

    def MessageGetId(self, message, id):

        sql = "DELETE FROM challenge WHERE challengeId = %s"
        val = (id, )
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO challenge(userID, challengeId) VALUES(%s, %s)"
        val = (message.id, id)
        db.cur.execute(sql, val)
        db.mydb.commit()


    async def SendMessage(self):

        challenge.updateArrays(self)
        await challenge.MakeMessage(self, vc.challenge_1)
        await challenge.MakeMessage(self, vc.challenge_2)


    async def NewDay(self, guild):
        #get all users
        sql = "SELECT * from users.challenge WHERE username is not NULL"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        for i in range(len(result)):
            #if user missed the day
            if result[i][6] == 0:
                val = (result[i][0], result[i][4])
                sql = "UPDATE users.challenge SET missed = missed + 1 WHERE userID = %s AND challengeId = %s;"
                db.cur.execute(sql, val)
                db.mydb.commit()
                sql = "UPDATE users.challenge SET missedstreak = missedstreak + 1 WHERE userID = %s AND challengeId = %s;"
                db.cur.execute(sql, val)
                db.mydb.commit()

                Activity = str(f"CHALLENGE{result[i][4]}")
                Minutes = 0
                now = datetime.datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                id = str(result[i][0])
                sql = f"INSERT INTO users.log (ID, Date, Minutes, Activity) VALUES (%s, %s, %s, %s);"
                val = (id, formatted_date, Minutes, Activity)
                db.cur.execute(sql, val)
                db.mydb.commit()

                if result[i][2] >= 5:
                    await challenge.removeRole(self, result[i][0], result[i][4])
                    val = (result[i][0], result[i][4])
                    sql = "DELETE FROM users.challenge WHERE userID = %s AND challengeId = %s;"
                    db.cur.execute(sql, val)
                    db.mydb.commit()
                    member = client.get_user(result[i][0])

                    channel = challenge.getChannel(result[i][4])
                    content = f"unfortunately, you lost the challenge {channel.name} because you have missed it for more than 5 days in total. better luck next time"
                    try:
                        channel = await member.create_dm()
                        await channel.send(content)
                    except:
                        pass

                # IF member misses more than 2 days in a row
                if result[i][3] >= 2:
                    await challenge.removeRole(self, result[i][0], result[i][4])
                    val = (result[i][0], result[i][4])
                    sql = "DELETE FROM users.challenge WHERE userID = %s AND challengeId = %s;"
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    member = client.get_user(result[i][0])
                    if member is None:
                        try:
                            member = self.client.get_user(result[i][0])
                        except:
                            member = self.get_user(result[i][0])
                    channel = challenge.getChannel(result[i][4])
                    content = f"unfortunately, you lost the challenge {channel.name} because you have missed it for more than two days in a row. better luck next time"
                    channel = await member.create_dm()
                    try:
                        await channel.send(content)
                    except:
                        print(f"{member} lost the challenge")
                        pass
            if result[i][6] == 1:
                val = (result[i][0], result[i][4])
                sql = "UPDATE users.challenge SET missedstreak = 0 WHERE userID = %s AND challengeId = %s;"
                db.cur.execute(sql, val)
                db.mydb.commit()
                sql = "UPDATE users.challenge SET streak = streak + 1 WHERE userID = %s AND challengeId = %s;"
                db.cur.execute(sql, val)
                db.mydb.commit()

                Activity = str(f"CHALLENGE{result[i][4]}")
                Minutes = 1
                now = datetime.datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                id = str(result[i][0])
                sql = f"INSERT INTO users.log (ID, Date, Minutes, Activity) VALUES (%s, %s, %s, %s);"
                val = (id, formatted_date, Minutes, Activity)
                db.cur.execute(sql, val)
                db.mydb.commit()
            await challenge.AddToUndone(self, result[i][0], result[i][4])
        await challenge.SendMessage(self)

    async def challengeWinners(self, guild):
        sql = "SELECT * from users.challenge WHERE username is not NULL"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        for i in range(len(result)):
            # Give user +1000xp
            member = guild.get_member(result[i][0])
            if member is None:
                member = guild.get_user(result[i][0])
            await levels.addXP(member, 500)
            channel = challenge.getChannel(result[i][4])

            # let user know
            content = f"Congratulations on completing the challenge {channel.name}! {challenge.new_line} +1000xp Social Credit points have been added to your account!"
            try:
                channel = await member.create_dm()
                await channel.send(content)
            except:
                pass
            # Delete all users

        sql = "DELETE FROM users.challenge WHERE challengeId = 1 OR 2"
        db.cur.execute(sql)
        db.mydb.commit()

    # ADD NEW MEMBER
    def checkifNewMember(member, challengeId):
        sql = "SELECT * FROM challenge WHERE (userID, challengeId) = (%s, %s)"
        val = (member.id, challengeId)
        db.cur.execute(sql, val)
        result = db.cur.fetchone()
        if result is None:
            return True
    def addUser(member, challengeId):
        if (challenge.checkifNewMember(member, challengeId)) is True:
            sql = "INSERT INTO challenge(userID, username, missed, missedstreak, challengeId, failed, donetoday, streak) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (member.id, member.name, 0, 0, challengeId, False, 0, 0)
            db.cur.execute(sql, val)
            db.mydb.commit()
            print(f"we are adding{member.name}")

        else:
            print("he's already on the list!")
            #sql new row

    async def giveRole(message):
            member = message.mentions[0]
            if message.channel.id == vc.challenge_1:
                role = discord.utils.get(member.guild.roles, id=vc.challenge_role_1)
                await member.add_roles(role)
                challenge.addUser(member, 1)
            elif message.channel.id == vc.challenge_2:
                role = discord.utils.get(member.guild.roles, id=vc.challenge_role_2)
                await member.add_roles(role)
                challenge.addUser(member, 2)
            else:
                print("type that from a challenge channel pls")
    async def AddToDone(self, message, memberid, inter):
        sql = "UPDATE users.challenge SET donetoday = 1 WHERE userID = %s AND challengeId = %s;"
        val = (memberid, inter)
        db.cur.execute(sql, val)
        db.mydb.commit()




    async def AddToUndone(self, memberid, inter):
        sql = "UPDATE users.challenge SET donetoday = 0 WHERE userID = %s AND challengeId = %s;"
        val = (memberid, inter)
        db.cur.execute(sql, val)
        db.mydb.commit()

    def fillMessages(self, integ):
        guild = vc.guild_id
        if integ == 3:
            # Get Challenge id
            sql = "SELECT userID FROM challenge WHERE challengeId = 3"
            db.cur.execute(sql, )
            result = db.cur.fetchone()
            return vc.challenge_1.fetch_message(result[0])

        elif integ == 4:
            #get Challenge ID
            sql = "SELECT userID FROM challenge WHERE challengeId = 4"
            db.cur.execute(sql, )
            result = db.cur.fetchone()
            return vc.challenge_2.fetch_message(result[0])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("!message"):
            await challenge.SendMessage(self)
        if message.content.startswith("!add"):
            await challenge.giveRole(message)
        if message.content.startswith("!newday"):
            await challenge.NewDay(self, vc.guild)
        if message.content.startswith("!reminder"):
            await challenge.reminder(self, vc.guild)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload.member)

        #Get Challenges
        challenge.Message1 = await challenge.fillMessages(self, 3)
        challenge.Message2 = await challenge.fillMessages(self, 4)

        if payload.member.bot:
            print("the N word")
            return
        if payload.message_id == challenge.Message1.id:
            #add user
            challenge.addUser(payload.member, 1)
            await challenge.AddToDone(self, challenge.Message1, payload.user_id, 1)
            await challenge.updateMessage(self, channel=vc.challenge_1)

            Embed = discord.Embed()
            Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
            Embed.add_field(name=f"{payload.member}, Committing to the daily challenge! ",
                            value=f"+ 10xp",
                            inline=False)
            message = await vc.challenge_1.send(embed=Embed)
            await asyncio.sleep(4)
            await message.delete()

            await levels.addXP(payload.member, 10) # add xp


        elif payload.message_id == challenge.Message2.id:
            challenge.addUser(payload.member, 2)
            await challenge.AddToDone(self, challenge.Message2, payload.user_id, 2)
            await challenge.updateMessage(self, channel=vc.challenge_2)

            channel = vc.challenge_2
            await heatmap.commandHeatmap("CHALLENGE2", channel, payload.member)
            Embed = discord.Embed()
            Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
            Embed.add_field(name=f"{payload.member}, Committing to the daily challenge! ",
                            value=f"+ 10xp",
                            inline=False)
            message = await channel.send(embed=Embed)
            await asyncio.sleep(4)
            await message.delete()

            # add xp

            await levels.addXP(payload.member, 10)
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        challenge.Message1 = await challenge.fillMessages(self, 3)
        challenge.Message2 = await challenge.fillMessages(self, 4)

        if payload.message_id == challenge.Message1.id:
            print("In challenge 1")
            await challenge.AddToUndone(self, payload.user_id, 1)
            await challenge.updateMessage(self, channel=vc.challenge_1)
        elif payload.message_id == challenge.Message2.id:
            print("challenge 2")
            await challenge.AddToUndone(self, payload.user_id, 2)
            await challenge.updateMessage(self, channel=vc.challenge_2)




async def setup(client):
    await client.add_cog(challenge(client))

async def teardown(client):
    return