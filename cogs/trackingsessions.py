from datetime import datetime
import asyncio
import discord
from discord.ext import commands

from mydb import db
from cogs.vc import vc
from cogs.heatmap import heatmap
from cogs.levels import levels





class trackings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        # IGNORE IF MESSAGE FROM A BOT
        if message.author.bot:
            return

        if message.content.startswith('!reboot'):
            await timeTrack.totalReboot(self)
            await timeTrack.deleteUserMessage(message)

        if message.channel.id == vc.tasks_id:
            # add xp
            if message.content.startswith('🔳'):
                content = "Setting a Goal for the Day! + 25 xp"
                levels.popupMessage(message.author, 25, content)

        if message.content.startswith('!day'):

            result = timeTrack.getUserStats(message.author.id)
            Activities = timeTrack.getActivities(self, result)

            embedVar = discord.Embed(title=f"{message.author.name}'s day", color=0xe86a75)
            await message.delete()
            CurrentlySomewhere = False
            try:
                Activity, timeInterval = await start.getSessionTime(message.author)
                CurrentlySomewhere = True
                embedVar.add_field(name=f"Currently in {Activity}",
                                   value=f"{timeInterval} m", inline=False)
            except:
                embedVar.add_field(name=f"Currently nowhere",
                                   value=f"-", inline=False)
                Activity = "Workout"
                timeInterval = 0
                pass

            Results = await timeTrack.addThingsDoneToday(self, Activities, CurrentlySomewhere, timeInterval, Activity.title())
            messageTodayDone = timeTrack.addTodayDone(Results)
            Message = timeTrack.createMessage(Results)





            try:
                embedVar.add_field(name="Stats Today: ", value=f"{Message}", inline=False)
            except:
                embedVar.add_field(name="Stats Today: ", value=f"start your day now", inline=False)
            embedVar.add_field(name="Things Done Today", value=f"{messageTodayDone}", inline=False)
            print(embedVar)
            try:
                Messsage = await message.channel.send(embed=embedVar)
            except:
               Messsage = await message.channel.send("you need to have some minutes tracked first")

            if message.channel.id == (vc.lions_cage_text_id):
                return
            else:
                await asyncio.sleep(4)
                await Messsage.delete()

            return




            # if user in sessionlogs
        if timeTrack.trackingTime(message):
            Activity, Time = await timeTrack.getMessageContent(message.content, message.channel)
            await levels.giveXP(message.author, Time, Activity)
            await timeTrack.deleteUserMessage(message)
            await timeTrack.addTime(Time, message.author.id, Activity)

            if message.channel.id == (vc.lions_cage_text_id):
                return
            else:
                await asyncio.sleep(4)
                await message.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return


        if await channels.quitConditions(member, before, after) is True:
            return
        if (timeTrack.checkifEntries(member.id)):
            await timeTrack.deleteFromList(member.id)





        await start.conditions(member, before, after)


class channels():
    study = [["STUDY", vc.sparta_id],
                     ["STUDY", vc.study_id]]  # List of Study VC

    lifestyle =      [["WORKOUT", vc.workout_id],    # List of Lifestyle VC
                      ["YOGA", vc.yoga_id],
                      ["MEDITATION", vc.meditation_id],
                      ["CHORES", vc.chores_id],
                      ["READING", vc.reading_id],
                      ["CREATIVE", vc.producing_id],
                      ["CREATIVE", vc.creative_id]]

    chillChannels = [vc.lions_cage_id, vc.doing_drugs_id, vc.vibing_id]  # List of Chill VC

    async def quitConditions(member, before, after):
        if (after.channel is None):
            await timeTrack.quitSomething(member)
            return True


        if channels.switchChannels(before, after):
            try:
                await timeTrack.quitSomething(member)
            except:
                print("quit didn't work mate")
                pass

        if channels.checkifChannel(after.channel.id, channels.study):
            if channels.camOff(member, before, after):
                await timeTrack.quitSomething(member)

    def switchChannels(before, after):
        if (before.channel is not None) and (before.channel != after.channel):
            return True
    def camTurnedOn(member, before, after):
        if ((((after.self_video == True or after.self_stream == True)) and (
                before.self_video == False and before.self_stream == False))) or (member.id == 744545219260842014):
            return True

    def camOn(member):
        if ((member.voice.self_video == True) or (member.voice.self_stream == True )):
            return True

    def camOff(member, before, after):
        if (((after.self_video == False and after.self_stream == False)) and (
                before.self_video == True) or (before.self_stream == True)):
            return True

    def checkifChannel(voiceid, channels):
        for i in range(len(channels)):  # Check if in right channels
            if voiceid == channels[i][1]:
                print(f" in {channels[i][0]}")
                return channels[i][0]
        return False

class start():

    async def getSessionTime(member):
        id = member.id
        sql = f"Select Start, Activity from users.sessionlog where ID = {id}"
        db.cur.execute(sql,)
        result = db.cur.fetchone()
        end = datetime.now()
        start = result[0]
        Activity = result[1]
        timeInterval = timeTrack.calculateTime(start, end)
        return Activity, timeInterval

    async def addSessionTime(member):

        Activity, timeInterval = await start.getSessionTime(member)

        await levels.giveXP(member, timeInterval, Activity)
        id = member.id
        await timeTrack.addTime(timeInterval, id, Activity)

    async def startSomething(member, timestamp, Activity):
        sql = f"INSERT INTO users.sessionlog (ID, Name, Start, Activity) VALUES (%s, %s, %s, %s);"
        val = (member.id, member.name, timestamp, Activity)
        db.cur.execute(sql, val)
        db.mydb.commit()

    async def conditions(member, before, after):
        if (await start.lifestyle(member, before, after)):
            return# join lifestyle stuff
        await start.study(member, before, after)

    async def LaunchTheHeatmap(Activity, member):
        Time = levels.getActivity(Activity.title(), member.id)
        if Time[0] == 0:
            await heatmap.launchHeatmap(Activity, member)

    async def lifestyle(member, before, after):  # start lifestyle maybe
        if ((before.channel != after.channel)):
            Activity = channels.checkifChannel(after.channel.id, channels.lifestyle)
            if Activity:
                await start.startSomething(member, datetime.now(), Activity)
                await start.LaunchTheHeatmap(Activity, member)

    async def study(member, before, after):
        if channels.camTurnedOn(member, before, after):
            Activity = channels.checkifChannel(after.channel.id, channels.study)
            if Activity:
                await start.startSomething(member, datetime.now(), Activity)
                await start.LaunchTheHeatmap(Activity, member)

class timeTrack():

    def getActivities(self, result):
        Activities = list(result)
        Activities.pop(0)
        return Activities
    async def addThingsDoneToday(self, Activities, CurrentlySomewhere, timeInterval, Activity):
        Results = []
        ThingsDone = ["Study", "Workout", "Yoga", "Reading", "Meditation", "Chores", "Creative", "Total"]
        for i in range(len(ThingsDone) - 1):
            if Activities[i] > 0:
                # TODO mache embed schöner
                if CurrentlySomewhere is True:
                    CurrentlySomewhere = False
                    if Activity == ThingsDone[i]:
                        Activities[i] += timeInterval
                Results.append(f" {ThingsDone[i]}: {await timeTrack.toHours(self, Activities[i])}")
        return Results
    def createMessage(Results):
        Message = ""
        for i in range(len(Results)):
            Message = Message + f"{Results[i]}\n"
        return Message
    def addTodayDone(Results):
        MessageEmoji = {"Study": "- :book: ", "Workout": "- :muscle:  ", "Yoga": "- :sunny: ",
                        "Reading ": "- :blue_book: ", "Meditation": "- :cyclone: ", "Chores": "- :gem: ",
                        "Creative": "- :art: "}
        messageTodayDone = "-"
        for i in Results:
            for j in MessageEmoji:
                if j in i:
                    messageTodayDone = messageTodayDone + MessageEmoji[j]
        return messageTodayDone
    async def toHours(self, inter):
        return f"{int(inter / 60)}h {int(inter % 60)}m"
    def getUserStats(id):
        # get stats of users day from DB
        sql = f"SELECT * FROM users.daily WHERE ID = {id}"
        db.cur.execute(sql, )
        return db.cur.fetchone()


    async def deleteUserMessage(message):
        if message.channel.id == (vc.lions_cage_text_id):
            pass
        else:
            try:
                await message.delete()
            except:
                pass

    def trackingTime(message):
        activities = ["!yoga", "!workout", "!reading", "!meditation"]
        for i in range(len(activities)):
            if (message.content.startswith(activities[i])):
                return activities[i]
        else:
            return False

    async def getMessageContent(content, channel):
        result = content.split(" ")
        activity = result[0]
        activity = activity[1:]
        try:
            Time = int(result[1])

        except:
            await channel.send(f"you have to type !{activity} <minutes>.   like !yoga 30")
            return
        if Time >= 60:
            await channel.send("nice try, more than 60 minutes of manual logging is not allowed")
            return
        else:
            return activity, Time

    def calculateTime(start, end):
        print(end-start)
        return (int((end - start).total_seconds() / 60)) #TODO: add / 60

    async def addTime(time, id, Activity):
        sql = f"UPDATE users.daily SET {Activity} = {Activity} + {time}, Total = Total + {time} WHERE ID = {id}"
        db.cur.execute(sql, )
        db.mydb.commit()

    async def deleteFromList(id):
        sql = f"DELETE FROM users.sessionlog where ID = {id}"
        db.cur.execute(sql, )
        db.mydb.commit()

    def checkifEntries(id):
        sql = f"select * from users.sessionlog where ID = {id}"
        db.cur.execute(sql,)
        result = db.cur.fetchall()
        if result != None:
            return True



    def getAllSessionLogs(self):
        sql = "Select ID, Activity from users.sessionlog"
        db.cur.execute(sql, )
        return db.cur.fetchall()


    async def rebootDown(self):
        UserInSession = timeTrack.getAllSessionLogs(self)
        for i in range(len(UserInSession)):
            member = vc.guild.get_member(UserInSession[i][0])
            await timeTrack.quitSomething(member)

    async def rebootUp(self):
        Member = vc.guild.members
        for i in range(len(Member)):
            if Member[i].voice is None:
                continue
            channelid = Member[i].voice.channel.id
            Activity = channels.checkifChannel(channelid, channels.lifestyle)
            if Activity:
                await start.startSomething(Member[i], datetime.now(), Activity)
            Activity = channels.checkifChannel(channelid, channels.study)
            if Activity:
                if channels.camOn(Member[i]):
                    await start.startSomething(Member[i], datetime.now(), Activity)

    async def totalReboot(self):
        await timeTrack.rebootDown(self)
        await timeTrack.rebootUp(self)




    async def rebootUpdate(self, Result):
        UserInSession = timeTrack.getAllSessionLogs(self)
        for i in range(len(UserInSession)):
            for j in range(len(Result)):
                if UserInSession[i][0] == Result[j][0]:
                    member = vc.guild.get_member(UserInSession[i][0])
                    await timeTrack.quitSomething(member)
                    await start.startSomething(member, datetime.now(), UserInSession[i][1])


    async def quitSomething(member): # Member Add Time
        await start.addSessionTime(member)
        await timeTrack.deleteFromList(member.id)

    async def ToHours(self, inter):
        return f"{int(inter / 60)}h {int(inter % 60)}m"

def setup(client):
    client.add_cog(trackings(client))
#camoff
#switchvc
#camon
#joinvc




