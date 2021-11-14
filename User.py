import discord
from discord.ext import commands

from mydb import db
from vc import vc

class User:
  def __init__(self, name, id, studying=False, workout = False, yoga = False, reading = False, creative = False, meditation = False, chores = False, producing = False, StartStudy = None, EndStudy = None, StudyIntervall = 0):
    self.name = name
    self.id = id
    self.studying = studying
    self.workout = workout
    self.yoga = yoga
    self.reading = reading
    self.creative = creative
    self.meditation = meditation
    self.chores = chores
    self.producing = producing

    self.StartStudy = StartStudy
    self.EndStudy = EndStudy
    self.StudyIntervall = StudyIntervall

class userfunction():

# Reset the users in the python user dictionary
    async def ResetUsers(client):
        if (len(Users)) > 1:        
            for i in Users:
                i.studying = False
                i.workout = False
                i.yoga = False
                i.reading = False
                i.creative = False
                i.meditation = False
                i.chores = False
                i.producing = False
                i.StartStudy = None
                i.Endstudy = None
                i.StudyIntervall = 0
        else:
            guild = client.get_guild(vc.guild_id)
            memberlist = guild.members
            for i in range (len(memberlist)):
                await userfunction.AddMember(client, memberlist[i])

# ADD A NEW MEMBER TO THE DATABASE
    async def AddMember(self, member):
        if await userfunction.GetUser(self, member):
            return
        #make entry in main list
        print(member.id)
        print(member.bot)
        print(member.name)
        
        sql = "INSERT INTO User (ID, Bot, Name, NickName, xp) VALUES (%s, %s, %s, %s, %s)"
        val = (member.id, member.bot, member.name, member.display_name, 0)
        print(sql)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO Daily (ID, Study, Workout, Yoga, Reading, Meditation, Chores, Creative, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO Weekly (ID, Study, Workout, Yoga, Reading, Meditation, Chores, Creative, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO Monthly (ID, Study, Workout, Yoga, Reading, Meditation, Chores, Creative, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO Streaks (ID, Study, Workout, Yoga, Reading, Meditation, Chores, Creative, Boots, LongestSession) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO Week (ID, Study, Workout, Yoga, Reading, Meditation, Chores,  Creative) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO Achievements (ID, Cage, Won, Lost) VALUES (%s, %s, %s, %s)"
        val = (member.id, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        #add member in python object list
        Nome = member.name
        Nome = User(member.name, member.id)
        Users.insert(0,Nome)
        print(Users[0].name)


# CHECK IF THE USER IS ALREADY IN THE DATABASE
    async def GetUser(self, member):
        try:
            sql = f"SELECT * FROM users.user WHERE ID = {member.id}"
            result = db.fetch(db, sql)           
            #sql = "SELECT * FROM users.user WHERE ID = %s"
            #val = (member.id, )
            #db.cur.execute(sql, val)
            #result = db.cur.fetchone()
            if not result:
                print(f"user does not exist: {member.id}")
            else: 
                return result
        except Exception as e:
            print(f"Error looking up userid {e}")


EOL = User("EOL", 0)
Users = [EOL]


class user(commands.Cog):
    def __init__(self, client):
        self.client = client




    
    #Add new joining members to the database
    @commands.Cog.listener()
    async def on_member_join(self, member):
        user.AddMember(self, member)


    

def setup(client):
  client.add_cog(user(client))