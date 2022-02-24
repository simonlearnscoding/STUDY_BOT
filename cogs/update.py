
from discord.ext import commands, tasks
from cogs.challenge import challenge
from cogs.tracking import tracking

import time

import sys


sys.path.append('/.../')
from mydb import db
from vc import vc

class update(commands.Cog):
    def __init__(self, client):
        self.client = client



        second = time.localtime().tm_sec



    async def update(self):

        switch = True
        switch2 = True
        switch3 = True
        switch4 = True
        switch5 = True
        minute = time.localtime().tm_min
        hour = time.localtime().tm_hour
        weekday = time.localtime().tm_wday
        monthday = time.localtime().tm_mday

        # daily update
        # if hour == 4:
        guild = self.get_guild(vc.guild_id)
        if hour == 2 and minute == 10:
            if switch is True:
                switch = False
                #await tracking.reboot1(self, guild)
                await update.updateTables("daily", "weekly")
                sql = "DELETE FROM users.goal"
                db.cur.execute(sql, )
                await tracking.reboot2(self, guild)
        if hour == 2 and minute == 12:
            switch = True
            print("switch back on")

        # weekly update
        if weekday == 0 and hour == 3 and minute == 40:
            if switch2 is True:
                switch2 = False
                #await tracking.reboot1(self, guild)
                await update.updateTables("weekly", "monthly")
                await tracking.reboot2(self, guild)
        if weekday == 0 and hour == 3 and minute == 45:
            switch2 = True

        # TODO monthly switch
        if monthday == 1 and hour == 3 and  minute == 50:
            if switch3 is True:
                switch3 = False
                #await tracking.reboot1(self, guild)
                print("monthly switch")
                await tracking.reboot2(self, guild)
                # TODO monthly switch
        if monthday == 1 and hour == 3  and minute == 55:
            switch3 = True

    async def updateTables(time1, time2):
        print("one")
        column = ("STUDY", "WORKOUT", "YOGA", "READING", "MEDITATION", "CHORES", "CREATIVE", "TOTAL")
        for j in range(len(column)):
            sql = f"SELECT ID, {column[j]} FROM users.{time1} WHERE {column[j]} > 0"
            sql = str(sql)
            db.cur.execute(sql)
            result = db.cur.fetchall()
            for i in range(len(result)):
                ID = int(result[i][0])
                value = int(result[i][1])
                sql = f"UPDATE users.{time2} SET {column[j]} = {column[j]} + %s WHERE ID = %s"
                sql = str(sql)
                val = (value, ID)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = f"UPDATE users.{time1} SET {column[j]} = 0 WHERE ID = %s"
                sql = str(sql)
                val = (ID,)
                db.cur.execute(sql, val)
                db.mydb.commit()


def setup(client):
    client.add_cog(update(client))
