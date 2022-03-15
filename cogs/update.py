
from discord.ext import commands, tasks
from cogs.challenge import challenge
from cogs.tracking import tracking
from cogs.goals import goals
import time
from cogs.levels import levels
import sys
from cogs.heatmap import heatmap
import cogs.tasks
from User import User
sys.path.append('/.../')
from mydb import db
from vc import vc

class update(commands.Cog):
    def __init__(self, client):
        self.client = client

        second = time.localtime().tm_sec

    switch = True

    async def update(self):


        minute = time.localtime().tm_min
        hour = time.localtime().tm_hour
        weekday = time.localtime().tm_wday
        monthday = time.localtime().tm_mday

        # daily update
        guild = self.get_guild(vc.guild_id)
        print("update function got called")
        switchtime = 30

        if minute < switchtime:
            Timezone = hour
            print("tried to update")
            if update.switch is True:
                print("update passed")
                update.switch = False

                if monthday == 1: #TODO: Test this
                    print("rewardchallengewinner")
                    challenge.challengeWinners(guild)

                sql = f"SELECT * FROM users.daily Where Timezone = {Timezone}" #Todo:
                sql = str(sql)
                db.cur.execute(sql)

                Resultt = db.cur.fetchall()
                if Resultt is None: #if there is no user in this timezone exit function
                    return
                for i in range(len(Resultt)):
                    cogs.tasks.tasks.resetDay(self, Resultt[i][0])

                    sql = "DELETE FROM users.goal WHERE ID = %s"
                    val = (Resultt[i][0], )
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    member = guild.get_member(Resultt[i][0])
                    if member is None:
                        pass
                    elif member.voice is None:
                        pass
                    else:
                        try:
                            await tracking.QuitSomething(self, member)
                            await tracking.StartSomething(self, member)
                        except Exception as e: print(e)
                #await tracking.reboot1(self, guild) #TODO: Reboot function fix
                heatmap.addDataDaily(self, Timezone)



                await update.updateTables("daily", "weekly", Timezone)
                #TODO: adapt user goals to timezone

                if hour == 7: #todo
                    await challenge.NewDay(self, guild)

                    # Reward Daily Winners
                    # try:
                    # await update.rewardDailyWinner(client=self)
                    # except:
                    # print("theres been an error with the daily winner")
                    # try:
                    # await update.rewardTopFour(client=self)
                    # except:
                    # print("theres been an error with the daily winner")

                if weekday == 0:
                    await update.updateTables("weekly", "monthly", Timezone)
                    if monthday == 1:
                        print("monthlyUpdate")
                await tracking.reboot2(self, guild)

        if minute > switchtime:
            update.switch = True
            print("switch back on")


    async def updateTables(time1, time2, TimeZone):
        print("one")
        column = ("STUDY", "WORKOUT", "YOGA", "READING", "MEDITATION", "CHORES", "CREATIVE", "TOTAL")
        for j in range(len(column)):
            sql = f"SELECT ID, {column[j]} FROM users.{time1} WHERE {column[j]} > 0 AND Timezone = {TimeZone}" #TODO:
            sql = str(sql)
            db.cur.execute(sql)
            result = db.cur.fetchall()
            for i in range(len(result)):
                ID = int(result[i][0])
                value = int(result[i][1])
                sql = f"UPDATE users.{time2} SET {column[j]} = {column[j]} + %s WHERE ID = %s AND Timezone = {TimeZone}" #TODO:
                sql = str(sql)
                val = (value, ID)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = f"UPDATE users.{time1} SET {column[j]} = 0 WHERE ID = %s AND Timezone = {TimeZone}" #TODO:
                sql = str(sql)
                val = (ID,)
                db.cur.execute(sql, val)
                db.mydb.commit()

    async def rewardDailyWinner(client):
        RankList = await goals.ranking(client)
        print(f"the inner is: {[RankList[0][0]]}")
        list = [RankList[0][0][2]]
        id = list[0]
        member = client.get_user(id=id)
        content = f"congratulations, {member.name} you dominated the leaderboard yesterday! +50xp!"
        channel = await member.create_dm()
        try:
            await channel.send(content)
        except:
            pass
        await levels.addXP(client, member, 50)

    async def rewardTopFour(client):
        RankList = await goals.ranking(client)
        for i in range(1, 5):
            print(f"the inner is: {[RankList[0][i][0]]}")
            list = [RankList[0][i][2]]
            id = list[0]
            member = client.get_user(id=id)
            content = f"good job, {member.name} you made it to the top 5 on the leaderboard yesterday! +20xp!"
            channel = await member.create_dm()
            try:
                await channel.send(content)
            except:
                pass
            await levels.addXP(client, member, 25)

def setup(client):
    client.add_cog(update(client))
