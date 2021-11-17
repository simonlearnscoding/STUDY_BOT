import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext import commands, tasks
import datetime
import asyncio
import re

import sys
sys.path.append('/.../')
import vc
import mydb
from mydb import db
from User import userfunction, user, User, Users

NameCheck = False

#db = db()

class goals(commands.Cog):

    def __init__(self, client):
        self.client = client

# CHECK PERIODICALLY IF SOMEONE STUDIED AN HOUR            

    async def check_goals():
        global NameCheck
        #for rows in goals:

        sql= "SELECT * FROM users.goal WHERE Won is False"
        db.cur.execute(sql, )
        result=db.cur.fetchall()
        result=list(result)       
        for i in (range(len(list(result)))):
            
            #get user total
            sql = "SELECT total FROM users.Daily WHERE ID = %s"
            val = (result[i][0], )
            totaltime=db.fetchone(sql, val)
            totaltime = int(totaltime[0])
            
            for x in User.Users:
                if x.id == result[i][0]:
                    if x.StartStudy is not None:
                        extratimesec = (int((datetime.datetime.now() - x.StartStudy).total_seconds() ))
                        extratime = extratimesec / 60
                        totaltime = totaltime + extratime                    
            
            #get user OldCurrent
            sql = "SELECT Current FROM users.Goal WHERE ID = %s"
            val = (result[i][0], )
            OldCurrent=db.fetchone(sql, val)
            OldCurrent = int(OldCurrent[0])
            NewCurrent = int(totaltime ) #TODO add / 50
            if OldCurrent != NewCurrent:
                UserId = result[i][0]
                #set user measuredmin, user current
                sql = "UPDATE users.Goal SET Current = %s, measuredMin = %s WHERE ID = %s"
                val = (NewCurrent, totaltime, UserId)
                db.cur.execute(sql, val)
                db.mydb.commit()
                guild = client.get_guild(vc.guild_id)
                member = guild.get_member(UserId)
                
                sql= "SELECT NickName FROM users.Goal WHERE ID = %s"
                val = (UserId, )
                db.cur.execute(sql, val)
                Nick=db.cur.fetchone()
                Nick = str(Nick[0])

                sql= "SELECT Goal FROM users.Goal WHERE ID = %s"
                val = (UserId, )
                db.cur.execute(sql, val)
                Goal=db.cur.fetchone()    
                Goal = int(Goal[0])
                if NewCurrent >= Goal:
                    channel = client.get_channel(vc.bot_id)
                    await channel.send(f"good job on reaching your daily goal, {Nick}")
                    
                    # Set Won to true 
                    sql = "UPDATE users.Goal SET Won = True WHERE ID = %s"
                    val = (member.id, )
                    db.cur.execute(sql, val)
                    db.mydb.commit()
                    
                    sql= "UPDATE users.Achievements SET Won = Won + 1 WHERE ID = %s"
                    val = (member.id, )
                    db.cur.execute(sql, val)
                    db.mydb.commit()
                    
                    #kann ich vl löschen
                    #GoalCount = cur.fetchone()
                    #GoalCount = int(GoalCount[0])
                    #GoalCount = GoalCount + 1

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
                    #TODO EXP

                NameCheck = True
                Nick = f"{Nick} {NewCurrent}/{Goal}"
                await asyncio.sleep(5)
                try:
                    await member.edit(nick=Nick)
                except:(f"can't rename member{member.name}")

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


            #get current minutes
            try:
                sql = "SELECT Total FROM users.Daily WHERE ID = %s"
                print(after.id)
                val = (after.id, )
                db.cur.execute(sql, val)
                result = db.cur.fetchone()
            except Exception as e:
                print("Error looking up user id %s", (e))

            print(result)
            #print(result[8])
            measuredMin = int(result[0])        
            #get user value
            current = int(measuredMin) #TODO add /50

            #see if id in datenbank    
            try:
                sql = "SELECT * FROM users.Goal WHERE ID = %s"
                val = (ID, )
                db.cur.execute(sql, val)
                result = db.cur.fetchone()

                if not result:
                    print("user does not exist: %s", ID)
                    #add row if user not in db
                    number = txt[-1]
                    x = re.split("/", number)
                    Goal = int(x[1])
                    print(Goal)       

                    sql = "INSERT INTO goal (ID, Goal, Current, NickName, measuredMin, Won) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (ID, Goal, current, name, measuredMin, False)
                    db.cur.execute(sql, val)
                    db.mydb.commit()
                    #started daily goal

                    guild = self.client.get_guild(vc.guild_id)  
                    member = guild.get_member(ID)
                    role = discord.utils.get(member.guild.roles, id=vc.challenge_role_id)
                    await asyncio.sleep(5)
                    await member.add_roles(role)

                    channel = self.client.get_channel(vc.bot_id)
                    await channel.send(f"{name} you've set your goal of the day to be {Goal} hours, good luck")
                    Nick = f"{name} {current}/{Goal}"
                    await after.edit(nick=Nick)    

                else: 
                    print("User in Database")
                    #is won it true?
                    sql = "SELECT Won FROM users.Goal WHERE ID = %s"
                    val = (after.id, )
                    db.cur.execute(sql, val)
                    result = db.cur.fetchone()
                    result = int(result[0])
                    print(result)
                    #TODO change channel into after.channel or whatever it is

                    channel = self.client.get_channel(vc.bot_id)
                    guild = self.client.get_guild(vc.guild_id)   

                    if result == 0:
                        
                        sql = "SELECT Goal FROM users.Goal WHERE ID = %s"
                        val = (after.id, )
                        db.cur.execute(sql, val)
                        result = db.cur.fetchone()
                        Goal = int(result[0])                        
                        await channel.send(f"You're already on the list, {name}")
                        Nick = f"{name} {current}/{Goal}"
                        ID = after.id
                        member = guild.get_member(id=ID)
                        await member.edit(nick=Nick)    
                        #rename user 
                    else: 
                        await channel.send(f"you already won, {name} you can set a new goal tomorrow")
                        await asyncio.sleep(5)
                        Nick = after.name
                        await after.edit(nick=Nick)
                    # return result
            except Exception as e:
                print("Error looking up userid %s", (e))
        


def setup(client):
   client.add_cog(goals(client))