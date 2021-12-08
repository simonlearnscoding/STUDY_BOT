from asyncio.tasks import wait
import discord
from discord.ext import commands, tasks
from discord.channel import VoiceChannel
from discord.client import Client
from giphy_client.rest import ApiException
import asyncio
import datetime
from datetime import date
import time

import sys

sys.path.append('/.../')
from mydb import db


class update(commands.Cog):
    def __init__(self, client):
        self.client = client



        second = time.localtime().tm_sec



    async def update(self):

        switch = True
        switch2 = True
        switch3 = True
        minute = time.localtime().tm_min
        hour = time.localtime().tm_hour
        weekday = time.localtime().tm_wday
        monthday = time.localtime().tm_mday

        # daily update
        # if hour == 4:
        if hour == 1 and minute == 00:
            if switch is True:
                switch = False
                await update.updateTables("daily", "weekly")
                sql = "DELETE FROM users.goal"
                db.cur.execute(sql, )


        if hour == 0 and minute == 55:
            switch = True
            print("switch back on")
        # weekly update
        if weekday == 0 and minute == 12:
            if switch2 is True:
                switch2 = False
                await update.updateTables("weekly", "monthly")

        if weekday == 0 and minute == 15:
            switch2 = True

        # TODO monthly switch
        # TODO monthly switch
        if monthday == 1 and minute == 20:
            if switch3 is True:
                switch3 = False
                print("monthly switch")

                # TODO monthly switch
        if monthday == 1 and minute == 26:
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
