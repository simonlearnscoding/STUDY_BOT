import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import re
import sys
from cogs.levels import levels
sys.path.append('/.../')
from vc import vc
from mydb import db
from User import userfunction, user, User, Users
from trackingsessions import timeTrack


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

        sql = "SELECT ID, TOTAL FROM users.weekly"
        db.cur.execute(sql, )
        result3 = db.cur.fetchall()

        RankingList = []
        RankingWeek = []
        for i, j in result:

            for x, y in result2:
                if i == x:
                    RankingList.append([y, j, x, 0])
        for i, j in result3:
            for x, y in result2:
                if i == x:
                    RankingWeek.append([y, j, x])


        sql = "Select ID, Start, Activity from users.sessionlog"
        db.cur.execute(sql, )
        Result = db.cur.fetchall()
        for i in range(len(Result)):
            extratime = timeTrack.calculateTime(Result[i][1], datetime.now())

            for j in range(len(RankingList)):
                    if Result[i][0] == RankingList[j][2]:
                        RankingList[j][1] = int(RankingList[j][1] + extratime)
                        RankingList[j][3] = 1

        for i in range(len(RankingWeek)):
            for j in range(len(RankingList)):
                if RankingWeek[i][2] == RankingList[j][2]:
                    RankingWeek[i][1] += RankingList[j][1]
                    RankingWeek[i][1] = round((RankingWeek[i][1] / 60), 1)

        minutes = lambda RankingList: RankingList[1]
        hours =  lambda RankingWeek: RankingWeek[1]
        RankingList.sort(key=minutes, reverse=True)
        RankingWeek.sort(key=minutes, reverse=True)
        return RankingList, RankingWeek

    async def displayranking(client, list, week):

        Embed = discord.Embed()
        embed = discord.Embed(
        
        )
        channel = client.get_channel(vc.leaderboard)
        embed.set_image(url="https://c4.wallpaperflare.com/wallpaper/10/477/184/vaporwave-statue-sculpture-wallpaper-thumb.jpg")
        for i in range(10):
            online = ""
            if list[i][3] == 0:
                online = ""
            else:
                online = ":tennis:"
            if list[i][1] == 0:
                pass
            else:
                rankInHours = int(list[i][1] / 60)
                rankInMinutes = int(list[i][1] % 60)
                if (rankInMinutes < 10):
                    rankInMinutes = "0" + str(rankInMinutes)

                embed.add_field(name=f"{i + 1} {list[i][0]} - {rankInHours}:{rankInMinutes}  {online}", value="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", inline=False)


        Embed.add_field(name="Weekly Rank:",
                        value="..",
                        inline=False)


        for i in range(10):
            Embed.add_field(name=f"{i + 1} {week[i][0]} - {week[i][1]}h",
                            value="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ",
                            inline=False)

        Message = channel.get_partial_message(vc.daily_message)
        Messsage = channel.get_partial_message(vc.weekly_message)
        try:
            await Message.edit(embed=Embed)
            await Messsage.edit(embed=embed)
        except:
            print('didnt work again...')
    # add their current time
    def seeifInDB(id):
        sql = f"SELECT * FROM users.goal WHERE ID = {id}"
        db.cur.execute(sql, )
        result = db.cur.fetchone()
        if result is None:
            return False
        else:
            return True

    async def check_goals(client):
        global NameCheck
        # for rows in goals:

        sql = "SELECT * FROM users.goal WHERE Won = 0"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        result = list(result)

        sql = "Select ID, Start from users.sessionlog"
        db.cur.execute(sql, )
        InSession = db.cur.fetchall()

        for i in (range(len(list(result)))):

            # get user total
            sql = "SELECT total FROM users.daily WHERE ID = %s"
            val = (result[i][0],)
            db.cur.execute(sql, val)
            totaltime = db.cur.fetchone()
            totaltime = int(totaltime[0])
            id = int(val[0])

            for i in range(len(InSession)):
                if id == InSession[i][0]:
                    extratime = timeTrack.calculateTime(InSession[i][1], datetime.now())
                    totaltime = totaltime + extratime


            # get user OldCurrent
            sql = "SELECT Current FROM users.goal WHERE ID = %s"
            db.cur.execute(sql, val)
            OldCurrent = db.cur.fetchone()
            OldCurrent = int(OldCurrent[0])
            NewCurrent = int(totaltime  )  # TODO add / 50
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

                    sql = "UPDATE users.goal SET Won = 1 WHERE ID = %s"
                    val = (member.id,)
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    Nick = f"{member.name}"
                    await asyncio.sleep(5)
                    try:
                        await member.edit(nick=Nick)
                    except:
                        pass
                    xp = 50
                    Embed = discord.Embed()
                    Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
                    Embed.add_field(
                        name=f"{Nick} Sticking to your Goals! +50xp!",
                        value=f"+ {xp}xp",
                        inline=False)
                    message = await channel.send(embed=Embed)
                    await asyncio.sleep(4)
                    await message.delete()
                    # add xp
                    await levels.addXP(member, xp)

                Nick = f"{Nick} {NewCurrent}/{Goal}"
                await asyncio.sleep(5)
                try:
                    await member.edit(nick=Nick)
                except:
                    (f"can't rename member{member.name}")

    # CHECK IF MEMBER CHANGED NAME
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        print("user update")
        if before.display_name != after.display_name:
            print(f"{after.name} changed name")
            if goals.seeifInDB(after.id):
                return
            Nick = after.display_name
            txt = str.split(Nick)
            name = txt[0]
            ID = after.id

            # get current minutes
            try:
                sql = "SELECT Total FROM users.daily WHERE ID = %s"
                val = (ID,)
                db.cur.execute(sql, val)
                result = db.cur.fetchone()
                if result is None:      #Add member if not in goals DB
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

                    channel = self.client.get_channel(vc.chores_vc_id)
                    guild = self.client.get_guild(vc.guild_id)

                    if result == 0:

                        sql = "SELECT Goal FROM users.goal WHERE ID = %s"
                        val = (after.id,)
                        db.cur.execute(sql, val)
                        result = db.cur.fetchone()
                        Goal = int(result[0])
                        #await channel.send(f"You're already on the list, {name}")
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




async def setup(client):
    await client.add_cog(goals(client))

async def teardown(client):
    return