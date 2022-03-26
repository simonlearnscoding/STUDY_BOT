from discord.ext import commands
import sys
import time
from cogs.vc import vc
from cogs.challenge import challenge
sys.path.append('/.../')
from mydb import db
from cogs.tasks import tasks
from trackingsessions import timeTrack
from cogs.heatmap import heatmap

class updateNew(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def selectPeople(Timezone):
        sql = f"SELECT * FROM users.daily Where Timezone = {Timezone} and Switch = False"  # Todo:

        db.cur.execute(sql, )
        return db.cur.fetchall()
    async def selectPeopleSwitch(Timezone):
        sql = f"SELECT * FROM users.daily Where Timezone != {Timezone} and Switch = True"
        sql = str(sql)
        db.cur.execute(sql, )
        return db.cur.fetchall()

    async def resetGoals(id):
        sql = f"DELETE FROM users.goal WHERE ID = {id}"
        db.cur.execute(sql, )
        db.mydb.commit()
    async def switch(Result, list, Bool):
        sql = f"update users.{list} set Switch = {Bool} where ID = {Result}"
        db.cur.execute(sql, )
        db.mydb.commit()
    async def setToFalse(Timezone):
        Result = await updateNew.selectPeopleSwitch(Timezone)
        if Result is None:  # if there is no user in this timezone exit function
            print("everything's been done")
            pass
        else:
            for i in range(len(Result)):
                await updateNew.switch(Result[i][0], "daily", "False")
    async def updateTables(userData, time1, time2):
        activity = ("Study", "Workout", "Yoga", "Reading", "Meditation", "Chores", "Creative", "Total")
        for i in range(0, 8):
            Activity = str(activity[i])
            Minutes = str(userData[i + 1])
            id = str(userData[0])
            # Set weekly = weekly.today
            sql = f"Update users.{time2} set {Activity} = {Activity} + {Minutes} WHERE  ID = {id};"
            db.cur.execute(sql, )
            db.mydb.commit()
            #Set Today = 0
            sql = f"Update users.{time1} set {Activity} = 0 WHERE  ID = {id};"
            db.cur.execute(sql, )
            db.mydb.commit()

    Switch = False
    async def update(self):

        minute = time.localtime().tm_min
        hour = time.localtime().tm_hour
        weekday = time.localtime().tm_wday
        monthday = time.localtime().tm_mday
        switchtime = 45 #TODO: fix switchtime


        if minute < switchtime:
            Timezone = hour
            print("tried to update")
            if updateNew.Switch == False:
                print("update went through")
                updateNew.Switch = True
                if monthday == 1:  # TODO: change this to 1
                    print("rewardchallengewinner")
                    await challenge.challengeWinners(self, vc.guild)
                # Challenge New Message
                if hour == 9: #todo change hour
                        await challenge.NewDay(self, vc.guild)
                # Set Switch people last hour to false for next day
                await updateNew.setToFalse(Timezone)

                # Get all users with Current Timezone
                Result = await updateNew.selectPeople(Timezone)
                # if there is no user in this timezone exit function
                if Result is None:
                    print("everything's been done")
                    return

                # Reboot all Members in vc
                await timeTrack.rebootUpdate(self, Result)

                for i in range(len(Result)): #reset user's Tasks
                    # Log user Daily Data
                    heatmap.addRow(Result[i])
                    id = Result[i][0]
                    # Reset Users Task List
                    await tasks.resetDay(self, id)
                    # Reset users Challenge
                    await updateNew.resetGoals(id)
                    # Update his Daily Challenge Thing
                    await updateNew.updateTables(Result[i], "daily", "weekly")
                    try:
                        member = vc.getmember(id)
                        # Add user Challenge Stat
                        await heatmap.commandHeatmap("CHALLENGE1", vc.challenge_1, member)
                        await heatmap.commandHeatmap("CHALLENGE2", vc.challenge_2, member)
                    except:
                        print(id)
                    await updateNew.switch(Result[i][0], "daily", "True")  # Set Switch to True
                    if weekday == 0:
                        await updateNew.updateTables(Result[i], "weekly", "monthly")
        else:
            updateNew.Switch = False






def setup(client):
    client.add_cog(updateNew(client))
