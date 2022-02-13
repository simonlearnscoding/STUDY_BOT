import discord
from discord import client
from mydb import db
from discord.ext import commands, tasks
import sys

import time
from cogs.levels import levels

sys.path.append('/.../')
from vc import vc



class challenge(commands.Cog):
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    monthday = time.localtime().tm_mday
    missing1 = []
    done1 = []
    missing2 = []
    done2 = []
    switch2 = True
    new_line = '\n'
    emoji = '\N{RAISED HAND}'
    switch = True
    def __init__(self, client):
        self.client = client


    async def checktimes(client):
        guild = client.get_guild(vc.guild_id)
        channel = guild.get_channel(917547602277453857)

        if challenge.hour == 20 and challenge.minute == 30:
            if challenge.switch is True:
                challenge.switch = False
                # reminder
                await channel.send("!reminder")

        if challenge.hour == 20 and challenge.minute == 31:
            switch = True
            print("switch back on")

        if challenge.hour == 0 and challenge.minute == 56:
            if challenge.switch2 is True:
                challenge.switch2 = False
                # reminder
                await channel.send("!newday")

        if challenge.hour == 0 and challenge.minute == 57:
            switch2 = True
            print("switch back on")

    async def removeRole(userID, challengeID):
            guild = client.get_guild(vc.guild_id)
            member = guild.get_member(userID)
            if challengeID == 1:
                role = discord.utils.get(member.guild.roles, id=vc.challenge_role_1)
                await member.remove_roles(role)
            elif challengeID == 2:
                role = discord.utils.get(member.guild.roles, id=vc.challenge_role_2)
                await member.remove_roles(role)
            else:
                print("type that from a challenge channel pls")
    def SetToMissing(client):
        sql = "UPDATE users.challenge SET donetoday = 0;"
        db.cur.execute(sql)
        db.mydb.commit()
    def emptyArrays(client):
        challenge.done1 = []
        challenge.done2 = []
        challenge.missing1 = []
        challenge.missing2 = []
    def FillEmptyArrays(client):
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
    def FillDoneArrays(client):
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
    def updateArrays(client):
        challenge.emptyArrays(client)
        challenge.FillEmptyArrays(client)
        challenge.FillDoneArrays(client)

    def SetToDone(int):
        pass
        #on User React Hand To Message
        #update  donetoday = 1 where id = userid and challengeid = int
    def startDay(client):
        challenge.SetToMissing(client)
        challenge.updateArrays(client)
    async def reminder(client):

        sql = "SELECT * from users.challenge WHERE username is not NULL AND donetoday != 1"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        guild = client.get_guild(vc.guild_id)
        for i in range(len(result)):
            member = guild.get_member(result[i][0])
            if result[i][4] == 1:
                channel = guild.get_channel(vc.challenge_1)
                message = await challenge.fillMessages(3)
            elif result[i][4] == 2:
                channel = guild.get_channel(vc.challenge_2)
                message = await challenge.fillMessages(4)
            content = f"don't forget to complete your challenge {channel.name} today! you can go to this message and react with {challenge.emoji} when you did it! {message.jump_url}"
            channel = await member.create_dm()
            await channel.send(content)

    async def MakeMessage(self, channel):
        Embed = discord.Embed()
        Embed.add_field(name=f"Day {challenge.monthday}", value=f"...", inline=False)
        if channel.id == vc.challenge_1:
            Embed.add_field(name="Done: ", value=f"{challenge.done1}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing1}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message1 = await channel.send(embed=Embed)
            challenge.MessageGetId(self, challenge.Message1, 3)
            challenge.Message1 = await challenge.fillMessages(self, 3)
            await challenge.Message1.add_reaction(challenge.emoji)

        elif channel.id == vc.challenge_2:
            Embed.add_field(name="Done: ", value=f"{challenge.done2}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing2}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message2 = await channel.send(embed=Embed)
            challenge.MessageGetId(challenge.Message2, 4)
            challenge.Message2 = await challenge.fillMessages(4)
            await challenge.Message2.add_reaction(challenge.emoji)

    async def updateMessage(channel):

        if channel.id == vc.challenge_1:
            Embed = discord.Embed()
            Embed.add_field(name=f"Day {challenge.monthday}", value=f"...", inline=False)
            challenge.updateArrays(client)
            Embed.add_field(name="Done: ", value=f"{challenge.done1}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing1}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message1 = await challenge.fillMessages(3)
            await challenge.Message1.edit(embed=Embed)

        elif channel.id == vc.challenge_2:
            Embed = discord.Embed()
            Embed.add_field(name=f"Day {challenge.monthday}", value=f"...", inline=False)
            challenge.updateArrays(client)
            Embed.add_field(name="Done: ", value=f"{challenge.done2}\n", inline=False)
            Embed.add_field(name="Missing: ", value=f"{challenge.missing2}\n", inline=False)
            Embed.add_field(name="react with :raised_hand: if you did it", value="...", inline=False)
            challenge.Message2 = await challenge.fillMessages(4)
            await challenge.Message2.edit(embed=Embed)

    def MessageGetId(message, id):

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
        channel = discord.Client.get_channel(self, vc.challenge_1)
        await challenge.MakeMessage(channel)
        channel = discord.Client.get_channel(self, vc.challenge_2)
        await challenge.MakeMessage(channel)
        #for every member where failed is false and challenge is 1:
            #get member name by id
            #put member name in missing list

        #send message in server

    async def NewDay(client):
        #get all users
        sql = "SELECT * from users.challenge WHERE username is not NULL"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        guild = discord.Client.get_guild(client, vc.guild_id)

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
                if result[i][2] >= 5:
                    await challenge.removeRole(result[i][0], result[i][4])
                    val = (result[i][0], result[i][4])
                    sql = "DELETE FROM users.challenge WHERE userID = %s AND challengeId = %s;"
                    db.cur.execute(sql, val)
                    db.mydb.commit()
                    member = guild.get_member(result[i][0])
                    if result[i][4] == 1:
                        channel = guild.get_channel(vc.challenge_1)
                    elif result[i][4] == 2:
                        channel = guild.get_channel(vc.challenge_2)
                    content = f"unfortunately, you lost the challenge {channel.name} because you have missed it for more than 5 days in total. better luck next time"
                    channel = await member.create_dm()
                    await channel.send(content)
                # IF member misses more than 2 days in a row
                if result[i][3] >= 2:
                    await challenge.removeRole(result[i][0], result[i][4])
                    val = (result[i][0], result[i][4])
                    sql = "DELETE FROM users.challenge WHERE userID = %s AND challengeId = %s;"
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    member = guild.get_member(result[i][0])
                    if result[i][4] == 1:
                        channel = guild.get_channel(vc.challenge_1)
                    elif result[i][4] == 2:
                        channel = guild.get_channel(vc.challenge_1)
                    content = f"unfortunately, you lost the challenge {channel.name} because you have missed it for more than two days in a row. better luck next time"
                    channel = await member.create_dm()
                    await channel.send(content)
            if result[i][6] == 1:
                val = (result[i][0], result[i][4])
                sql = "UPDATE users.challenge SET missedstreak = 0 WHERE userID = %s AND challengeId = %s;"
                db.cur.execute(sql, val)
                db.mydb.commit()
                sql = "UPDATE users.challenge SET streak = streak + 1 WHERE userID = %s AND challengeId = %s;"
                db.cur.execute(sql, val)
                db.mydb.commit()
            await client.AddToUndone(result[i][0], result[i][4])

        if challenge.monthday == 1:
            for i in range(len(result)):
                # Give user +2000xp
                member = guild.get_member(result[i][0])
                levels.addXP(member, 2000)

                if result[i][4] == 1:
                    channel = guild.get_channel(vc.challenge_1)
                elif result[i][4] == 2:
                    channel = guild.get_channel(vc.challenge_2)
                # let user know
                content = f"Congratulations on completing the challenge {channel.name}! {challenge.new_line} +2000xp Social Credit points have been added to your account!"
                channel = await member.create_dm()
                await channel.send(content)
                # Delete all users

            sql = "DELETE FROM challenge WHERE challengeId = 1 OR 2"
            db.cur.execute(sql)
            db.mydb.commit()


        await challenge.SendMessage(client)
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

    async def AddToDone(essage, memberid, inter):
        sql = "UPDATE users.challenge SET donetoday = 1 WHERE userID = %s AND challengeId = %s;"
        val = (memberid, inter)
        db.cur.execute(sql, val)
        db.mydb.commit()
    async def AddToUndone(memberid, inter):
        sql = "UPDATE users.challenge SET donetoday = 0 WHERE userID = %s AND challengeId = %s;"
        val = (memberid, inter)
        db.cur.execute(sql, val)
        db.mydb.commit()

    def fillMessages(self, integ):

        if integ == 3:
            guild = discord.Client.get_guild(self, vc.guild_id)
            sql = "SELECT userID FROM challenge WHERE challengeId = 3"
            db.cur.execute(sql, )
            result = db.cur.fetchone()
            channel = guild.get_channel(vc.challenge_1)
            return channel.fetch_message(result[0])

        elif integ == 4:
            guild = discord.Client.get_guild(vc.guild_id)
            sql = "SELECT userID FROM challenge WHERE challengeId = 4"
            db.cur.execute(sql, )
            result = db.cur.fetchone()
            channel = guild.get_channel(vc.challenge_2)
            return channel.fetch_message(result[0])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("!message"):
            await challenge.SendMessage()
        if message.content.startswith("!add"):
            await challenge.giveRole(message)
        if message.content.startswith("!starter"):
            challenge.startDay()
        if message.content.startswith("!newday"):
            if message.author.bot is False:
                return
            await challenge.NewDay(challenge)
        if message.content.startswith("!reminder"):
            await challenge.reminder(challenge)
    @commands.Cog.listener()
    async def on_raw_reaction_add(payload):
        print(payload.member)
        challenge.Message1 = await challenge.fillMessages(3)
        challenge.Message2 = await challenge.fillMessages(4)
        if payload.member.bot:
            print("the N word")
            return
        if payload.message_id == challenge.Message1.id:
            #add user
            challenge.addUser(payload.member, 1)
            await challenge.AddToDone(challenge.Message1, payload.user_id, 1)
            await challenge.updateMessage(channel=client.client.get_channel(vc.challenge_1))
        elif payload.message_id == challenge.Message2.id:
            challenge.addUser(payload.member, 2)
            await challenge.AddToDone(challenge.Message2, payload.user_id, 2)
            await challenge.updateMessage(channel=client.get_channel(vc.challenge_2))
    @commands.Cog.listener()
    async def on_raw_reaction_remove(payload):
        challenge.Message1 = await challenge.fillMessages(3)
        challenge.Message2 = await challenge.fillMessages(4)

        if payload.message_id == challenge.Message1.id:
            print("In challenge 1")
            await challenge.AddToUndone(payload.user_id, 1)
            await challenge.updateMessage(channel=client.get_channel(vc.challenge_1))
        elif payload.message_id == challenge.Message2.id:
            print("challenge 2")
            await challenge.AddToUndone(payload.user_id, 2)
            await challenge.updateMessage(channel=client.get_channel(vc.challenge_2))
    def end():
        pass
        #for row in db:
         #if failed is false:
            #give user 2000xp


def setup(client):
    client.add_cog(challenge(client))

