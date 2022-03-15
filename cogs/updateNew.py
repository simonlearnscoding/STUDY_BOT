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

    def selectPeople(Timezone):
        sql = f"SELECT * FROM users.daily Where Timezone = {Timezone} and Switch = False"  # Todo:
        sql = str(sql)
        db.cur.execute(sql)
        return db.cur.fetchall()
    def selectPeopleSwitch(Timezone):
        Timezone = Timezone - 1
        if Timezone < 0:
            Timezone = 23
        sql = f"SELECT * FROM users.daily Where Timezone <= {Timezone} and Switch = True"
        sql = str(sql)
        db.cur.execute(sql)
        return db.cur.fetchall()
    def resetGoals(id):
        sql = f"DELETE FROM users.goal WHERE ID = {id}"
        db.cur.execute(sql, )
        db.mydb.commit()
    def switch(Result, list, Bool):
        for i in range(len(Result)):
            print(Result[i][0])
            sql = f"update users.{list} set Switch = {Bool} where ID = {Result[i][0]}"
            db.cur.execute(sql, )
            db.mydb.commit()
    def setToFalse(Timezone):
        Result = updateNew.selectPeopleSwitch(Timezone)
        if Result is None:  # if there is no user in this timezone exit function
            print("everything's been done")
            pass
        else:
            updateNew.switch(Result, "daily", "False")
    def updateTables(userData, time1, time2):
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

    async def update(self):

        minute = time.localtime().tm_min
        hour = time.localtime().tm_hour
        weekday = time.localtime().tm_wday
        monthday = time.localtime().tm_mday
        switchtime = 30 #TODO: fix switchtime

        if minute < switchtime:
            Timezone = hour
            print("tried to update")

            if monthday == 1:  # TODO: change this to 1
                print("rewardchallengewinner")
                await challenge.challengeWinners(self, vc.guild)

            Result = updateNew.selectPeople(Timezone)
            if Result is None:  # if there is no user in this timezone exit function
                print("everything's been done")
                return
            await timeTrack.rebootUpdate(self, Result) #Reboot all Members in vc
            updateNew.switch(Result, "daily", "True") #Set Switch to True
            for i in range(len(Result)): #reset user's Tasks
                heatmap.addRow(Result[i])
                id = Result[i][0]
                tasks.resetDay(self, id)
                updateNew.resetGoals(id)
                updateNew.updateTables(Result[i], "daily", "weekly")
                await heatmap.commandHeatmap("CHALLENGE1", vc.challenge_1, vc.guild.get_member(id))
                await heatmap.commandHeatmap("CHALLENGE2", vc.challenge_2, vc.guild.get_member(id))

                if weekday == 0:
                    updateNew.updateTables(Result[i], "weekly", "monthly")



            if hour == 5: #todo change hour
                await challenge.NewDay(self, vc.guild)


            updateNew.setToFalse(Timezone) #Set Switch people last hour to false for next day


def setup(client):
    client.add_cog(updateNew(client))
