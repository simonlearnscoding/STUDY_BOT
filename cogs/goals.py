import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext import commands, tasks
import datetime
import asyncio
import re
import sys
import User
import emoji
sys.path.append('/.../')
from vc import vc
from mydb import db
from User import userfunction, user, User, Users
import itertools


NameCheck = False


# db = db()

class goals(commands.Cog):

    def __init__(self, client):
        self.client = client

    # CHECK PERIODICALLY IF SOMEONE STUDIED AN HOUR
    RankingList = []
    async def ranking(client):

        sql = "SELECT ID, TOTAL FROM users.daily"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        sql = "SELECT ID, NAME FROM users.user"
        db.cur.execute(sql, )
        result2 = db.cur.fetchall()
        RankingList = []
        for i, j in result:
            for x, y in result2:
                if i == x:
                    RankingList.append([y, j, x, 0])
        for x in Users:
            # add current study time
            if x.StartStudy is not None:
                extratimesec = (int((datetime.datetime.now() - x.StartStudy).total_seconds()))
                extratime = extratimesec / 60
                print(itertools.product(RankingList))
                for i in range(len(RankingList)):
                    for j in range(len(RankingList[i])):
                        if RankingList[i][j] == x.id:
                            RankingList[i][1] = int(RankingList[i][1] + extratime)
                            RankingList[i][3] = 1
        minutes = lambda RankingList: RankingList[1]
        RankingList.sort(key=minutes, reverse=True)
        return RankingList

    async def displayranking(client, list):
        embed = discord.Embed(

        )
        channel = client.get_channel(916484382091513917)
        embed.set_image(url="https://c4.wallpaperflare.com/wallpaper/10/477/184/vaporwave-statue-sculpture-wallpaper-thumb.jpg")
        for i in range(10):
            online = ""
            if list[i][3] == 0:
                online = ""
            else:
                online = ":tennis:"
            embed.add_field(name=f"{i + 1} {list[i][0]} - {list[i][1]}m  {online}", value="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", inline=False)
        Message = channel.get_partial_message(916518831676071946)
        await Message.edit(embed=embed)

    # add their current time
    async def check_goals(client):
        global NameCheck
        # for rows in goals:

        sql = "SELECT * FROM users.goal WHERE Won is False"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        result = list(result)
        for i in (range(len(list(result)))):

            # get user total
            sql = "SELECT total FROM users.daily WHERE ID = %s"
            val = (result[i][0],)
            db.cur.execute(sql, val)
            totaltime = db.cur.fetchone()
            totaltime = int(totaltime[0])
            print(totaltime)
            for x in Users:
                if x.id == val:
                    # add current study time
                    if x.StartStudy is not None:
                        extratimesec = (int((datetime.datetime.now() - x.StartStudy).total_seconds()))
                        extratime = extratimesec / 60
                        totaltime = totaltime + extratime
                        print("totaltime")
                        # get user OldCurrent
            sql = "SELECT Current FROM users.goal WHERE ID = %s"
            db.cur.execute(sql, val)
            OldCurrent = db.cur.fetchone()
            OldCurrent = int(OldCurrent[0])
            NewCurrent = int(totaltime / 50)  # TODO add / 50
            if OldCurrent != NewCurrent:
                UserId = result[i][0]
                # set user measuredmin, user current
                sql = "UPDATE users.goal SET Current = %s, measuredMin = %s WHERE ID = %s"
                val = (NewCurrent, totaltime, UserId)
                db.cur.execute(sql, val)
                db.mydb.commit()
                guild = client.get_guild(vc.guild_id)
                member = guild.get_member(UserId)

                sql = "SELECT NickName FROM users.goal WHERE ID = %s"
                val = (UserId,)
                db.cur.execute(sql, val)
                Nick = db.cur.fetchone()
                Nick = str(Nick[0])

                sql = "SELECT Goal FROM users.goal WHERE ID = %s"
                val = (UserId,)
                db.cur.execute(sql, val)
                Goal = db.cur.fetchone()
                Goal = int(Goal[0])
                if NewCurrent >= Goal:
                    channel = client.get_channel(vc.chores_vc_id)
                    await channel.send(f"good job on reaching your daily goal, {Nick}")

                    # Set Won to true 
                    sql = "UPDATE users.goal SET Won = True WHERE ID = %s"
                    val = (member.id,)
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    sql = "UPDATE users.achievements SET Won = Won + 1 WHERE ID = %s"
                    val = (member.id,)
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    # kann ich vl löschen
                    # GoalCount = cur.fetchone()
                    # GoalCount = int(GoalCount[0])
                    # GoalCount = GoalCount + 1

                    Nick = f"{Nick} done"
                    await asyncio.sleep(5)
                    NameCheck = True
                    await member.edit(nick=Nick)

                    role = discord.utils.get(member.guild.roles, id=vc.challenge_role_id)
                    await asyncio.sleep(5)
                    await member.remove_roles(role)
                    role = discord.utils.get(member.guild.roles, name="winner")
                    await asyncio.sleep(5)
                    await member.add_roles(role)
                    # TODO EXP

                NameCheck = True
                Nick = f"{Nick} {NewCurrent}/{Goal}"
                await asyncio.sleep(5)
                try:
                    await member.edit(nick=Nick)
                except:
                    (f"can't rename member{member.name}")

                #   FROM user.total table days reached goal += 1
                #   give user some XP
                #   give user role

    # CHECK IF MEMBER CHANGED NAME
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        global NameCheck
        if NameCheck == True:
            NameCheck = False
            return
        print("user update")
        if before.display_name != after.display_name:
            print(f"{after.name} changed name")
            Nick = after.display_name
            txt = str.split(Nick)
            name = txt[0]
            print(name)
            ID = after.id

            # get current minutes
            try:
                sql = "SELECT Total FROM users.daily WHERE ID = %s"
                print(after.id)
                val = (ID,)
                db.cur.execute(sql, val)
                result = db.cur.fetchone()
                if result is None:
                    guild = self.client.get_guild(vc.guild_id)
                    member = guild.get_member(ID)
                    await userfunction.AddMember(self, member)
                    sql = "SELECT Total FROM users.daily WHERE ID = %s"
                    print(after.id)
                    val = (after.id,)
                    db.cur.execute(sql, val)
                    result = db.cur.fetchone()
                    print(result)
                print(result)
            except Exception as e:
                print("Error looking up user id %s", (e))

            print(result)
            # print(result[8])
            measuredMin = int(result[0])
            # get user value
            current = int(measuredMin / 50)  # TODO add /50

            # see if id in datenbank
            try:
                sql = "SELECT * FROM users.goal WHERE ID = %s"
                val = (ID,)
                db.cur.execute(sql, val)
                result = db.cur.fetchone()

                if not result:
                    print("user not in goal db yet: %s", ID)
                    # add row if user not in db

                    number = txt[-1]
                    x = re.split("/", number)
                    Goal = int(x[1])
                    print(Goal)

                    sql = "INSERT INTO goal (ID, Goal, Current, NickName, measuredMin, Won) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (ID, Goal, current, name, measuredMin, False)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
                    # started daily goal

                    guild = self.client.get_guild(vc.guild_id)
                    member = guild.get_member(ID)
                    role = discord.utils.get(member.guild.roles, id=vc.challenge_role_id)
                    await asyncio.sleep(5)
                    await member.add_roles(role)

                    channel = self.client.get_channel(vc.chores_vc_id)
                    await channel.send(f"{name} you've set your goal of the day to be {Goal} hours, good luck")
                    Nick = f"{name} {current}/{Goal}"
                    await after.edit(nick=Nick)

                else:
                    print("User in Database")
                    # is won it true?
                    sql = "SELECT Won FROM users.goal WHERE ID = %s"
                    val = (after.id,)
                    db.cur.execute(sql, val)
                    result = db.cur.fetchone()
                    result = int(result[0])
                    print(result)
                    # TODO change channel into after.channel or whatever it is

                    channel = self.client.get_channel(vc.chores_vc_id)
                    guild = self.client.get_guild(vc.guild_id)

                    if result == 0:

                        sql = "SELECT Goal FROM users.goal WHERE ID = %s"
                        val = (after.id,)
                        db.cur.execute(sql, val)
                        result = db.cur.fetchone()
                        Goal = int(result[0])
                        await channel.send(f"You're already on the list, {name}")
                        Nick = f"{name} {current}/{Goal}"
                        ID = after.id
                        member = guild.get_member(after.id)
                        await member.edit(nick=Nick)
                        # rename user
                    else:
                        #await channel.send(f"you already won, {name} you can set a new goal tomorrow")
                        #await asyncio.sleep(5)
                        #Nick = after.name
                        #await after.edit(nick=Nick)
                        pass
                    # return result
            except Exception as e:
                print("Error looking up userid %s", (e))


def setup(client):
    client.add_cog(goals(client))
