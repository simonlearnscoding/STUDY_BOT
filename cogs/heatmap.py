import discord
from discord.ext import commands, tasks
from easy_pil import Canvas, Editor, Font, Text, font

import datetime
import sys
sys.path.append('/.../')
from vc import vc
from mydb import db
import time
import asyncio

Augustus = Font(vc.Augustus, size=40)
SmallFont = Font(vc.SmallFont, size=24)
SmallerFont = Font(vc.SmallerFont, size=21)

class heatmap(commands.Cog):
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    switch = True
    def __init__(self, client):
        self.client = client



    def updateUser(self, ID, Date, Minutes, Name , Activity):
        pass

    def addRow(self, userData):
        activity = ("STUDY", "WORKOUT", "YOGA", "READING", "MEDITATION", "CHORES", "CREATIVE", "TOTAL")
        for i in range(0, 7):
            Activity = str(activity[i])
            Minutes = str(userData[i + 1])
            now = datetime.datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            id = str(userData[0])
            sql = f"INSERT INTO users.log (ID, Date, Minutes, Activity) VALUES (%s, %s, %s, %s);"
            val = (id, formatted_date, Minutes, Activity)
            db.cur.execute(sql, val)
            db.mydb.commit()

    def selectAll(self):
        # Select entire Daily DB
        sql = f"SELECT * FROM users.daily"
        sql = str(sql)
        db.cur.execute(sql)
        result = db.cur.fetchall()
        return result

    def addDataDaily(self):
        result = heatmap.selectAll(self)
        for i in range(len(result)):
            heatmap.addRow(self, result[i])

    async def checkAdder(self):
        if heatmap.hour == 0 and heatmap.minute == 2:
            if heatmap.switch is True:
                heatmap.switch = False
                heatmap.addDataDaily(self)
        if heatmap.hour == 1 and heatmap.minute == 4:
            heatmap.switch = True
    def pickColor(self, Tresholds, Colors, Time):
        for i in range(len(Tresholds)):
            if Time < Tresholds[i]:
                return Colors[i]
            else:
                i = i+1

    def pickColorScheme(self, activity):

        if activity == "STUDY":
            return "#60EFE4", [1, 20, 60, 180, 5000], ["#2C3B3A", "#3D7773", "#499F98", "#54C7BE", "#60EFE4"]
        if activity == "YOGA":
            return "#94E8B4", [1, 10, 20, 40, 5000], ["#313A35", "#476151", "#689B7C", "#7EC198", "#94E8B4"]
        if activity == "CREATIVE":
            return "#94E8B4", [1, 10, 20, 40, 5000], ["#313A35", "#476151", "#689B7C", "#7EC198", "#94E8B4"]
        if activity == "WORKOUT":
                return "#DA2C38", [1, 10, 20, 40, 5000], ["#382829", "#802A30", "#A42B33", "#C82C36", "#DA2C38"]
        if activity == "READING":
                return "#D69F7E", [1, 10, 20, 40, 5000], ["#383330", "#7E6353", "#A17B64", "#B3876D", "#D69F7E"]
        if activity == "MEDITATION":
                return "#7FD8BE", [1, 5, 15, 20, 5000], ["#2F3936", "#538073", "#5B9182", "#6DB5A0", "#7FD8BE"]
        if activity == "CHORES":
                return "#D69F7E", [1, 10, 30, 60, 5000], ["#383330", "#7E6353", "#A17B64", "#B3876D", "#D69F7E"]
        if activity == "TOTAL":
                return "#F56476", [1, 15, 60, 180, 5000], ["#3B2D2F", "#8E464F", "#B7525E", "#CC5866", "#F56476"]
        if activity == "CHALLENGE1":
                return "#FDD692", [1, 2], ["#3C3932", "#FDD692"]
        if activity == "CHALLENGE2":
                return "#D8F1A0", [1, 2], ["#3C3932", "#D8F1A0"]





    async def DisplayHeatmap(self, data, activity, Today, channel, member):

        background = Editor(Canvas((840, 516), "#2C2F33"))
        background.rectangle(position=(0,0), width=840, height=516, color="#262727", radius=11)
        initialHeight = 104
        initialWidth = 112
        initialWidth2 = 64
        height= initialHeight
        width = initialWidth
        width= initialWidth
        Decrease= 48
        color = 0
        dailySum = 0
        currentstreak = 0
        longestSreak = 0
        daysDone = 0
        daysNotDone = 0


        # Calculating extra stats
        x = len(data)
        for x in range(len(data)):
            dailySum += data[x][0]
            if data[x][0] != 0:
                daysDone +=1
                currentstreak += 1
            else:
                daysNotDone +=1
                if currentstreak > longestSreak:
                    longestSreak = currentstreak
                    currentstreak = 0
        if longestSreak == 0:
            longestSreak = currentstreak
        daysDoneSum = daysDone + daysNotDone
        daysDone = round(((daysDone / daysDoneSum ) * 100),1)
        dailyAverage = int(dailySum / len(data))

        if dailyAverage > 60:
            dailyAverage = dailyAverage / 60
            dailyAverage =round(dailyAverage, 1)
            dailyAverage = str(f"{dailyAverage} h")
        elif dailyAverage < 2:
            dailyAverage = "/"
        else:
            dailyAverage = str(f"{dailyAverage} m")

        x = (len(data)) - 1
        Color, Tresholds, Colors = heatmap.pickColorScheme(self, activity)


        background.rectangle(position=(initialWidth2, initialHeight), width=40, height=40,
                             color=f"{heatmap.pickColor(self, Tresholds, Colors, Today)}", radius=4)
        height = height + Decrease
        for i in range(6):
            try:
                background.rectangle(position=(initialWidth2, height), width=40, height=40,
                                     color=f"{heatmap.pickColor(self, Tresholds, Colors, data[x][0])}", radius=4)
            except:
                background.rectangle(position=(initialWidth2, height), width=40, height=40,
                                     color=f"{heatmap.pickColor(self, Tresholds, Colors, 0)}", radius=4)
            height = height + Decrease
            if x > 0:
                x -= 1
            else:
                x = -200
        height = initialHeight
        for j in range (14):
            for i in range (7):
                try:
                    background.rectangle(position=(width,height), width=40, height=40, color=f"{heatmap.pickColor(self, Tresholds, Colors, data[x][0])}", radius=4)
                except:
                    background.rectangle(position=(width, height), width=40, height=40, color=f"{heatmap.pickColor(self, Tresholds, Colors, 0)}", radius=4)
                height = height + Decrease
                if x > 0:
                    x -= 1
                else:
                    x = -200


            width = width + Decrease
            height = initialHeight
        background.text((68, 40), str(f" {member.name} {activity}"), font=Augustus, color="white")


        initialPos=[(64, 460), (249, 462), (450, 459),(635, 458)]
        initialPosVal= [(164, 460), (360, 461), (590, 460),(755, 459)]
        increase = [150, 180, 185, 185]
        increase2 = [165, 245, 170, 170]
        text= ["Daily Avg:", "Days Done:", "Longest Streak:", "Curr. Streak:"]
        values=[dailyAverage, f"{daysDone}%", longestSreak, currentstreak]
        for i in range (4):
            background.text((initialPos[i]), str(f"{text[i]}"), font=SmallerFont, color="white")
            background.text((initialPosVal[i]), str(f"{values[i]}"), font=SmallerFont, color=Color)

        file = discord.File(fp=background.image_bytes, filename="card.png")
        Message = await channel.send(file=file)

        if channel.id == (vc.lions_cage_text_id):

            return
        else:
            await asyncio.sleep(5)
            await Message.delete()





    async def commandHeatmap(self, activity, channel, member):
        sql="select Minutes from users.log where ID =%s and Activity = %s"
        val=(member.id, activity)
        db.cur.execute(sql, val)
        result = db.cur.fetchall()


        if ((activity != "CHALLENGE1") and (activity != "CHALLENGE2")):
            Activity = activity.title()

            sql= f"select {Activity} from users.daily where ID =%s"
            val=(member.id, )
            db.cur.execute(sql, val)
            resultToday = db.cur.fetchone()
            Today = resultToday[0]

        if (activity == "CHALLENGE1"):
            sql= f"select donetoday from users.challenge where userID =%s AND challengeID = 1"
            val=(member.id, )
            db.cur.execute(sql, val)
            resultToday = db.cur.fetchone()
            Today = resultToday[0]

        elif (activity == "CHALLENGE2"):
            sql= f"select donetoday from users.challenge where userID =%s AND challengeID = 2"
            val=(member.id, )
            db.cur.execute(sql, val)
            resultToday = db.cur.fetchone()
            Today = resultToday[0]

        await heatmap.DisplayHeatmap(self, result, activity, Today, channel, member)

    #for i in range(len(result)):





        #print(result[i][0][0])
        #d0 = datetime.datetime(2022, 5, 18)
        #numberOfDays = d0 - result[i][0]
    #addDataDaily()

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        print(channel)
        if message.content.startswith('!track'):
            member = message.author

            Id = member.id
            result = message.content.split(" ")
            try:
                activity = str(result[1]).upper()
                await heatmap.commandHeatmap(self, activity, channel, member)
            except:
                if channel.id != (vc.lions_cage_text_id):
                    await message.delete()
                vcs = [vc.challenge_1, vc.challenge_2]
                activities = ["CHALLENGE1", "CHALLENGE2"]
                for i in range(len(vcs)):
                    if message.channel.id == vcs[i]:
                        activity = activities[i]
                        await heatmap.commandHeatmap(self, activity, channel, member)
                        return
                vcs= [vc.study_id, vc.sparta_id, vc.meditation_id, vc.reading_id, vc.chores_id, vc.workout_id, vc.yoga_id, vc.creative_id, vc.producing_id]
                activities=["STUDY", "STUDY", "MEDITATION", "READING", "CHORES", "WORKOUT", "YOGA", "CREATIVE", "CREATIVE", ]
                if message.author.voice is not None:
                    for i in range(len(vcs)):
                        if message.author.voice.channel.id == vcs[i]:
                            activity = activities[i]
                            await heatmap.commandHeatmap(self, activity, channel, member)
                            return
                else:
                    activity = "TOTAL"
                    await heatmap.commandHeatmap(self, activity, channel, member)

            try:
                if channel.id != (vc.lions_cage_text_id):
                    await message.delete()
            except:
                pass


    async def launchHeatmap(self, activity, member):
        channel = self.client.get_channel(vc.chores_vc_id)
        Message = await channel.send(f"View your Study Stats, type !track (when in vc) or !track {activity}")
        await heatmap.commandHeatmap(self, f"{activity.upper()}", channel, member)
        await Message.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # ALL THE START AND STOP STATEMENTS
        if member.bot:
            return

        if (before.channel != after.channel):
            if (after.channel is None):
                return
            # Select entire Daily DB
            sql = f"SELECT * FROM users.daily WHERE ID = %s"
            val = (member.id,)
            db.cur.execute(sql, val)
            result = db.cur.fetchall()
            if ((after.channel.id==vc.study_id) or (after.channel.id==vc.sparta_id)):
                if (int(result[0][1]) == 0):
                    await heatmap.launchHeatmap(self, "study", member)

            if (after.channel.id==vc.workout_id):
                if (int(result[0][2]) == 0):
                    await heatmap.launchHeatmap(self, "workout", member)

            if (after.channel.id==vc.yoga_id):
                if (int(result[0][3]) == 0):
                    await heatmap.launchHeatmap(self, "yoga", member)

            if (after.channel.id==vc.reading_id):
                if (int(result[0][4]) == 0):
                    await heatmap.launchHeatmap(self, "reading", member)

            if (after.channel.id==vc.meditation_id):
                if (int(result[0][5]) == 0):
                    await heatmap.launchHeatmap(self, "meditation", member)

            if (after.channel.id==vc.chores_id):
                if (int(result[0][6]) == 0):
                    await heatmap.launchHeatmap(self, "chores", member)

            if ((after.channel.id==vc.creative_id) or (after.channel.id==vc.producing_id)):
                if (int(result[0][7]) == 0):
                    await heatmap.launchHeatmap(self, "creative", member)


def setup(client):
    client.add_cog(heatmap(client))


    #for i in range(len(result)):
        #self.addRow(self, result[i])
