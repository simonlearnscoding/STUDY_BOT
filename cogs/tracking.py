import discord
from discord.ext import commands
from mydb import db
import datetime

# THE OTHER PY FILES
import User
from vc import vc
from cogs.boot import boot

#client.load_extension("cogs.boot")

class tracking(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def ToHours(self, inter):
        return f"{int(inter / 60)}h {int(inter % 60)}m"

    async def StartSomething(self, member):    
        if (member.voice is not None):
            for x in User.Users:
                if x.name == member.name:
                    if (member.voice.channel.id == vc.workout_id):     
                        print(f"{member.name} in a workout channel")
                        if x.workout == True:
                            return
                        x.workout = True
                        x.StartStudy = datetime.datetime.now()
                        print(f"{x.name} is working out since {x.StartStudy}")
                        print(f"{x.studying}")
                        return
                    if (member.voice.channel.id == vc.yoga_id):
                        if x.yoga == True:
                            return
                        x.yoga = True
                        x.StartStudy = datetime.datetime.now()
                        print(f"{x.name} is doing yoga out since {x.StartStudy}")
                        return
                    if (member.voice.channel.id == vc.reading_id):
                        print("member in a reading channel")
                        if x.reading == True:
                            return                    
                        x.reading = True
                        x.StartStudy = datetime.datetime.now()
                        print(f"{x.name} is reading since {x.StartStudy}")
                        return
                    if (member.voice.channel.id == vc.meditation_id):
                        print("member in a meditation channel")
                        if x.meditation == True:
                            return
                        x.meditation = True
                        x.StartStudy = datetime.datetime.now()
                        print(f"{x.name} is meditating since {x.StartStudy}")
                        return
                    if (member.voice.channel.id == vc.creative_id):
                        print("member in a creative channel")
                        if x.creative == True:
                            return
                        x.creative = True
                        x.StartStudy = datetime.datetime.now()
                        print(f"{x.name} is being creative since {x.StartStudy}")
                        return
                    if (member.voice.channel.id == vc.chores_id):
                        print(f"{member.name} in a chores channel")
                        if x.chores == True:
                            return
                        x.chores = True
                        x.StartStudy = datetime.datetime.now()
                        print(f"{x.name} is doing chores since {x.StartStudy}")
                        return
            

            if (member.voice.channel.id == vc.producing_id):
                if (member.voice.self_stream == True or member.voice.self_video == True):
                    print(f"{member.name} is producing")
                    for x in User.Users:
                        if x.name == member.name:
                            if x.creative == True:
                                return
                            x.creative = True
                            x.StartStudy = datetime.datetime.now()
                            print(f"{x.name} is producing since {x.StartStudy}")
                            return                   
    async def QuitSomething(self, member):
        print(f"{member.name} left vc")
        for x in User.Users:
            if x.name == member.name:    
                if x.studying is True:
                    await tracking.quitStudy(self, member, x)
                    return
                if x.workout is True:
                    await tracking.quitWorkout(self, member, x)
                    return
                if x.yoga is True:
                    await tracking.quitYoga(self, member, x)
                    return
                if x.reading is True:
                    await tracking.quitReading(self, member, x)
                    return
                if x.meditation is True:
                    await tracking.quitMeditation(self, member, x)
                    return
                if x.chores is True:
                    await tracking.quitChores(self, member, x)
                    return
                if x.creative is True:
                    await tracking.quitCreative(self, member, x)
                    return
#Update total time value
    async def UpdateTotal(self, member, Time):

        sql = "SELECT Total FROM users.daily WHERE ID = %s"
        val = (member.id, )
        db.cur.execute(sql, val)
        result=db.cur.fetchone()
        print(result)
        newID = result[0] + 1
        print(newID)
        #TODO Turn result into int
        NewResult = newID + int(Time)
        sql = "UPDATE users.daily SET Total = %s WHERE ID = %s"
        val = (NewResult, member.id)
        db.cur.execute(sql, val)
        db.mydb.commit()
        sql = "SELECT Study FROM users.daily WHERE ID = %s"
        val = (member.id, )
        db.cur.execute(sql, val)
        db.mydb.commit()
    

# Quit something Statements
    async def quitStudy(self, member, x):
            if x.studying == True:
                x.studying = False
                x.EndStudy = datetime.datetime.now()
                if x.StartStudy is not None:
                    #TODO TOTAL MINUTES?
                    x.StudyIntervall = (int((x.EndStudy - x.StartStudy).total_seconds() / 60))
                    print(f"{x.name} has been studying for {int(x.StudyIntervall)} minutes")
                    Id = member.id
                    Time = x.StudyIntervall

                    #Check if it's a new
                    sql = "SELECT LongestSession FROM users.streaks WHERE ID = %s"
                    val = (Id, )
                    db.cur.execute(sql, val)
                    result = db.cur.fetchone()
                    print(result)
                    if (Time > int(result[0]) and Time > 20):
                        print("new record")
                        channel = self.client.get_channel(vc.bot_id)
                        await channel.send(f"Congratulations on your new record of studying for {int(Time)} minutes!") 

                    sql = "UPDATE users.streaks SET LongestSession = %s WHERE ID = %s"
                    val = (Time, member.id)
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    #update new Study Time
                    sql = "SELECT Study FROM users.daily WHERE ID = %s"
                    val = (Id, )
                    db.cur.execute(sql, val)
                    result=db.cur.fetchone()
                    print(result)
                    newID = result[0]
                    print(newID)
                    #TODO Turn result into int
                    NewResult = newID + int(Time)
                    sql = "UPDATE users.daily SET Study = %s WHERE ID = %s"
                    val = (NewResult, member.id)
                    db.cur.execute(sql, val)
                    db.mydb.commit()

                    await tracking.UpdateTotal(self, member, Time)

                    sql = "SELECT Study FROM users.daily WHERE ID = %s"
                    val = (Id, )
                    db.cur.execute(sql, val)
                    result=db.cur.fetchone()
                    print(result)

                    if len(result) == 0:
                        sql = "INSERT INTO daily (id, Study) VALUES (%s, %s)"
                        val = (Id, Time)
                        db.cur.execute(sql, val)
                        db.mydb.commit()
                x.StartStudy = None
                x.EndStudy = None
                return
    async def quitWorkout(self, member, x):
        if x.workout == True:
            x.workout = False
            x.EndStudy = datetime.datetime.now()
            if x.StartStudy is not None:
                
                x.StudyIntervall = int((x.EndStudy - x.StartStudy).total_seconds() / 60)
                print(f"{x.name} has been working out for {int(x.StudyIntervall)} minutes")
                Id = member.id
                Time = x.StudyIntervall
                channel = self.client.get_channel(vc.bot_id)
                await channel.send(f"you've been working out for {int(Time)} minutes!") 

                sql = "SELECT Workout FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                newID = result[0] + 1
                print(newID)
                #TODO Turn result into int
                NewResult = newID + int(Time)
                
                sql = "UPDATE users.daily SET Workout = %s WHERE ID = %s"
                val = (NewResult, member.id)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Workout FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Workout FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                await tracking.UpdateTotal(self, member, Time)

                if len(result) == 0:
                    sql = "INSERT INTO daily (id, Workout) VALUES (%s, %s)"
                    val = (Id, Time)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
            x.StartStudy = None
            x.EndStudy = None                
            return
    async def quitReading(self, member, x):
        if x.reading == True:
            x.reading = False
            x.EndStudy = datetime.datetime.now()
            if x.StartStudy is not None:
                
                x.StudyIntervall = int((x.EndStudy - x.StartStudy).total_seconds() / 60)
                print(f"{x.name} has been Reading for {int(x.StudyIntervall)} minutes")
                Id = member.id
                Time = x.StudyIntervall
                channel = self.client.get_channel(vc.bot_id)
                await channel.send(f"you've been Reading for {int(Time)} minutes!") 

                sql = "SELECT Reading FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                newID = result[0] + 1
                print(newID)
                #TODO Turn result into int
                NewResult = newID + int(Time)
                
                sql = "UPDATE users.daily SET Reading = %s WHERE ID = %s"
                val = (NewResult, member.id)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Reading FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Reading FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                await tracking.UpdateTotal(self, member, Time)

                if len(result) == 0:
                    sql = "INSERT INTO daily (id, Reading) VALUES (%s, %s)"
                    val = (Id, Time)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
            x.StartStudy = None
            x.EndStudy = None                   
            return
    async def quitYoga(self, member, x):
        if x.yoga == True:
            x.yoga = False
            x.EndStudy = datetime.datetime.now()
            if x.StartStudy is not None:
                
                x.StudyIntervall = int((x.EndStudy - x.StartStudy).total_seconds() / 60) 
                print(f"{x.name} has been doing Yoga for {int(x.StudyIntervall)} minutes")
                Id = member.id
                Time = x.StudyIntervall
                channel = self.client.get_channel(vc.bot_id)
                # await channel.send(f"you've been doing Yoga for {int(Time)} minutes!") 

                sql = "SELECT Yoga FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                newID = result[0] + 1
                print(newID)
                #TODO Turn result into int
                NewResult = newID + int(Time)
                
                sql = "UPDATE users.daily SET Yoga = %s WHERE ID = %s"
                val = (NewResult, member.id)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Yoga FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Yoga FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                await tracking.UpdateTotal(self, member, Time)

                if len(result) == 0:
                    sql = "INSERT INTO daily (id, Yoga) VALUES (%s, %s)"
                    val = (Id, Time)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
            x.StartStudy = None
            x.EndStudy = None                      
            return
    async def quitMeditation(self, member, x):
        if x.meditation == True:
            x.meditation = False
            x.EndStudy = datetime.datetime.now()
            if x.StartStudy is not None:
                
                x.StudyIntervall = int((x.EndStudy - x.StartStudy).total_seconds() / 60)
                print(f"{x.name} has been meditating for {int(x.StudyIntervall)} minutes")
                Id = member.id
                Time = x.StudyIntervall
                channel = self.client.get_channel(vc.bot_id)
                #await channel.send(f"you've been meditating for {int(Time)} minutes!") 

                sql = "SELECT Meditation FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                newID = result[0] + 1
                print(newID)
                #TODO Turn result into int
                NewResult = newID + int(Time)
                
                sql = "UPDATE users.daily SET Meditation = %s WHERE ID = %s"
                val = (NewResult, member.id)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Meditation FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Meditation FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                await tracking.UpdateTotal(self, member, Time)

                if len(result) == 0:
                    sql = "INSERT INTO daily (id, Meditation) VALUES (%s, %s)"
                    val = (Id, Time)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
            x.StartStudy = None
            x.EndStudy = None                      
            return
    async def quitChores(self, member, x):
        if x.chores == True:
            x.chores = False
            x.EndStudy = datetime.datetime.now()
            if x.StartStudy is not None:
                
                x.StudyIntervall = int((x.EndStudy - x.StartStudy).total_seconds() / 60)
                print(f"{x.name} has been doing chores out for {int(x.StudyIntervall)} minutes")
                Id = member.id
                Time = x.StudyIntervall
                channel = self.client.get_channel(vc.bot_id)
                await channel.send(f"you've been doing chores for {int(Time)} minutes!") 
                sql = "SELECT Chores FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                newID = result[0] + 1
                print(newID)

                NewResult = newID + int(Time)
                
                sql = "UPDATE users.daily SET Chores = %s WHERE ID = %s"
                val = (NewResult, member.id)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Chores FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Chores FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                await tracking.UpdateTotal(self, member, Time)

                if len(result) == 0:
                    sql = "INSERT INTO daily (id, Chores) VALUES (%s, %s)"
                    val = (Id, Time)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
            x.StartStudy = None
            x.EndStudy = None                      
            return
    async def quitCreative(self, member, x):
        if x.creative == True:
            x.creative = False
            x.EndStudy = datetime.datetime.now()
            if x.StartStudy is not None:
                x.StudyIntervall = int((x.EndStudy - x.StartStudy).total_seconds() / 60) 
                print(f"{x.name} has been creative for {int(x.StudyIntervall)} minutes")
                Id = member.id
                Time = x.StudyIntervall
                channel = self.client.get_channel(vc.bot_id)
                await channel.send(f"you've been producing for {int(Time)} minutes!") 

                sql = "SELECT Creative FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                newID = result[0] + 1
                print(newID)
                NewResult = newID + int(Time)
                
                sql = "UPDATE users.daily SET Creative = %s WHERE ID = %s"
                val = (NewResult, member.id)
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Creative FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                db.mydb.commit()

                sql = "SELECT Creative FROM users.daily WHERE ID = %s"
                val = (Id, )
                db.cur.execute(sql, val)
                result=db.cur.fetchone()
                print(result)
                await tracking.UpdateTotal(self, member, Time)

                if len(result) == 0:
                    sql = "INSERT INTO users.daily (id, Creative) VALUES (%s, %s)"
                    val = (Id, Time)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
            x.StartStudy = None
            x.EndStudy = None                      
            return



    @commands.Cog.listener()
    
    async def on_voice_state_update(self, member, before, after):
     # ALL THE START AND STOP STATEMENTS
    
        if member.bot:
            return    
        channel = self.client.get_channel(id=vc.sparta_id)
    
        # Make new user if not in there yet
        Nome = member.name
   
        #return if member not in a vc
        if (member.voice == None):
            await tracking.QuitSomething(self, member)
            return

        # Quistudy condition for studying and producing
        if (after.self_video == False and after.self_stream == False): 
            if (after.channel.id == vc.sparta_id) or (after.channel.id == vc.study_id) or (after.channel.id == vc.producing_id):
                await tracking.QuitSomething(self, member)

        # If the member just joined a channel
        if (before.channel is not None) and (before.channel.id != after.channel.id):
            await tracking.QuitSomething(self, member)
            await tracking.StartSomething(self, member)

        # Is this one really necessary??
        if (before.channel is None and member.voice is not None):
            await tracking.StartSomething(self, member)

        # Setting the things to true
        if ((member.voice.channel.id == vc.study_id) or (member.voice.channel.id == vc.sparta_id) or (member.voice.channel.id == vc.producing_id)):
            print("member in a study or producing channel")

        #Start study counter if cam or ss on
        if (((after.self_video == True or after.self_stream == True)) and (before.self_video == False and before.self_stream == False)):
            for x in User.Users:
                if x.name == member.name:
                    if x.studying == True:
                        return
                    x.StartStudy = datetime.datetime.now()
                    print(f"{x.name} is studying or producing since {x.StartStudy}")
                    if (member.voice.channel.id == vc.study_id) or (member.voice.channel.id == vc.sparta_id):
                        x.studying = True
                    if (member.voice.channel.id == vc.producing_id):
                        x.creative = True
                    return

    @commands.Cog.listener()
    async def on_message(self, message): 
    #SHOW STATS OF THE DAY
        if message.author.bot:
            return
        if message.content.startswith('!day'):
            sql = "SELECT * FROM users.daily WHERE ID = %s"
            val = (message.author.id, )
            db.cur.execute(sql, val)
            result=db.cur.fetchone()
            L1=list(result)
            L1.pop(0)
            Results = []
            extratime = None

            for x in User.Users:
                if x.id == message.author.id:
                    if x.StartStudy is not None:
                        extratimesec = (int((datetime.datetime.now() - x.StartStudy).total_seconds() ))
                        extratime = extratimesec / 60
                        break
            ThingsDone = ["Study", "Workout", "Yoga", "Reading", "Meditation", "Chores", "Creative", "Total"]
            CurrentlyIn = ""
            for i in range (len(L1)):
                if extratime is not None:
                    if i == 0:
                        if x.studying == True:
                            L1[i] = L1[i] + extratime
                            CurrentlyIn = "Study"
                    if i == 1:
                        if x.workout == True:
                            L1[i] = L1[i] + extratime
                            CurrentlyIn = "Workout"
                    if i == 2:
                        if x.yoga == True:
                                L1[i] = L1[i] + extratime
                                CurrentlyIn = "Yoga"
                    if i == 3:
                        if x.reading == True:
                                L1[i] = L1[i] + extratime
                                CurrentlyIn = "Reading"
                    if i == 4:
                        if x.meditation == True:
                                L1[i] = L1[i] + extratime
                                CurrentlyIn = "Meditation"
                    if i == 5:
                        if x.chores == True:
                                L1[i] = L1[i] + extratime
                                CurrentlyIn = "Chores"
                    if i == 6:
                        if x.creative == True:
                                L1[i] = L1[i] + extratime
                                CurrentlyIn = "Creative"
                    if i == 7:
                        L1[i] = L1[i] + extratime
                if L1[i] > 0:
                #TODO mache embed schöner
                    Results.append(f" {ThingsDone[i]}: {await self.ToHours(L1[i])}")
                print(Results)
            Total = int(L1[-1])
            embedVar = discord.Embed(title=f"{message.author.name}'s day", color=0xe86a75)
            Message = ""
            for i in range (len(Results)):
                Message = Message + f"{Results[i]}\n"
            try:
                embedVar.add_field(name=f"Currently in {CurrentlyIn}", value=f"{int(extratimesec / 60)}m {extratimesec % 60}s", inline=False)
            except:
                print("currently nowhere")
            try:
                embedVar.add_field(name="Stats Today: ", value=f"{Message}", inline=False)
            except:
                embedVar.add_field(name="Stats Today: ", value=f"start your day now", inline=False)
            #Fetch user result
            sql = "SELECT (@row_number:=@row_number + 1) AS row_num, Total, ID  FROM users.daily, (SELECT @row_number:=0) AS temp ORDER BY Total DESC;"
            db.cur.execute(sql)
            result=db.cur.fetchall()
            print(result)
            k = 0
            for row in result:
                k += 1
                if row[2] == message.author.id:
                    guild = self.client.get_guild(vc.guild_id)

                    rank = int(row[0])

                    # Checking the close Ranking
                    try:
                        infrontuser = result[k - 2]
                        infrontminutes = int(infrontuser[1])
                        infrontuser = guild.get_member(infrontuser[2])
                        Rank1 = f"{rank - 1} - {infrontuser.name} - {await self.ToHours(infrontminutes)} \n"
                    except:
                        Rank1 = "You're the first!\n"

                    Rank2 = f"{rank} - {message.author.name} - {await self.ToHours(Total)} \n"

                    try:
                        behinduser = result[k]
                        behindminutes = (behinduser[1])
                        behinduser = guild.get_member(behinduser[2])
                        Rank3 = f"{rank + 1} - {behinduser.name} - {await self.ToHours(behindminutes)}"
                    except:
                        Rank3 = "You are currently the last"

                    Ranking = f"{Rank1} **{Rank2}** {Rank3} "
            embedVar.add_field(name="Your ranking", value=f"{Ranking}", inline=False)
            await message.channel.send(embed=embedVar)
            return

    async def ranking(self):

        sql = "SELECT ID, TOTAL FROM users.daily"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        print(result)

        sql = "SELECT ID, NAME FROM users.daily"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        print(result)

        Results = []
        extratime = None
        #print(L1)
        #print(L2)
        """
        for x in User.Users:

            if x.StartStudy is not None:
                extratimesec = (int((datetime.datetime.now() - x.StartStudy).total_seconds()))
                extratime = extratimesec / 60
                break
        ThingsDone = ["Study", "Workout", "Yoga", "Reading", "Meditation", "Chores", "Creative", "Total"]
        CurrentlyIn = ""
        for i in range(len(L1)):
            if extratime is not None:
                if i == 0:
                    if x.studying == True:
                        L1[i] = L1[i] + extratime
                        CurrentlyIn = "Study"
                if i == 1:
                    if x.workout == True:
                        L1[i] = L1[i] + extratime
                        CurrentlyIn = "Workout"
                if i == 2:
                    if x.yoga == True:
                        L1[i] = L1[i] + extratime
                        CurrentlyIn = "Yoga"
                if i == 3:
                    if x.reading == True:
                        L1[i] = L1[i] + extratime
                        CurrentlyIn = "Reading"
                if i == 4:
                    if x.meditation == True:
                        L1[i] = L1[i] + extratime
                        CurrentlyIn = "Meditation"
                if i == 5:
                    if x.chores == True:
                        L1[i] = L1[i] + extratime
                        CurrentlyIn = "Chores"
                if i == 6:
                    if x.creative == True:
                        L1[i] = L1[i] + extratime
                        CurrentlyIn = "Creative"
                if i == 7:
                    L1[i] = L1[i] + extratime
            if L1[i] > 0:
                # TODO mache embed schöner
                Results.append(f" {ThingsDone[i]}: {await self.ToHours(L1[i])}")
            print(Results)
        Total = int(L1[-1])
        embedVar = discord.Embed(title=f"{message.author.name}'s day", color=0xe86a75)
        Message = ""
        for i in range(len(Results)):
            Message = Message + f"{Results[i]}\n"
        try:
            embedVar.add_field(name=f"Currently in {CurrentlyIn}",
                               value=f"{int(extratimesec / 60)}m {extratimesec % 60}s", inline=False)
        except:
            print("currently nowhere")
        try:
            embedVar.add_field(name="Stats Today: ", value=f"{Message}", inline=False)
        except:
            embedVar.add_field(name="Stats Today: ", value=f"start your day now", inline=False)
            # Fetch user result
        sql = "SELECT (@row_number:=@row_number + 1) AS row_num, Total, ID  FROM users.daily, (SELECT @row_number:=0) AS temp ORDER BY Total DESC;"
        db.cur.execute(sql)
        result = db.cur.fetchall()
        print(result)
        k = 0
        for row in result:
            k += 1
            if row[2] == message.author.id:
                guild = self.client.get_guild(vc.guild_id)

                rank = int(row[0])

                # Checking the close Ranking
                try:
                    infrontuser = result[k - 2]
                    infrontminutes = int(infrontuser[1])
                    infrontuser = guild.get_member(infrontuser[2])
                    Rank1 = f"{rank - 1} - {infrontuser.name} - {await self.ToHours(infrontminutes)} \n"
                except:
                    Rank1 = "You're the first!\n"

                Rank2 = f"{rank} - {message.author.name} - {await self.ToHours(Total)} \n"

                try:
                    behinduser = result[k]
                    behindminutes = (behinduser[1])
                    behinduser = guild.get_member(behinduser[2])
                    Rank3 = f"{rank + 1} - {behinduser.name} - {await self.ToHours(behindminutes)}"
                except:
                    Rank3 = "You are currently the last"

                Ranking = f"{Rank1} **{Rank2}** {Rank3} "
        embedVar.add_field(name="Your ranking", value=f"{Ranking}", inline=False)
        await message.channel.send(embed=embedVar)
        return"""


#TODO
#@tasks.loop(seconds=1) #change the intervall here
#async def restart_day():
    #if time of day = 2am:
        #for rows in daily:
        #user week = user day + user week
        #user day = 0
        #if user has won day role:
        #role = discord.utils.get(member.server.roles, name="winner")
        #await asyncio.sleep(5)
        # await client.remove_roles(member, role1, role2, role3)
        #if user has  
#TODO
#@tasks.loop(seconds=1) #change the intervall here
#async def restart_week():
    #if time of week = monday:
        # if time of day = 3am 
        #for rows in weekly:
        #user month = user month + user week
        #user week = 0


def setup(client):
   client.add_cog(tracking(client))