import discord
from discord.ext import commands

from mydb import db
from cogs.vc import vc


class userfunction(commands.Cog):
    def __init__(self, client):
        self.client = client

# ADD A NEW MEMBER TO THE DATABASE
    async def AddMember(self, member):
        #make entry in main list
        print(f"adding {member.name} to the database")
        
        sql = "INSERT INTO users.user (ID, Bot, Name, NickName, xp, LVL) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (member.id, member.bot, member.name, member.display_name, 100, 1)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO users.daily (ID, Study, Workout, Yoga, Reading, Meditation, Chores, Creative, Total, Timezone, Switch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO users.weekly (ID, Study, Workout, Yoga, Reading, Meditation, Chores, Creative, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

        sql = "INSERT INTO monthly (ID, Study, Workout, Yoga, Reading, Meditation, Chores, Creative, Total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()


# CHECK IF THE USER IS ALREADY IN THE DATABASE
    async def GetUser(self, member):
        sql = "SELECT * FROM users.user WHERE ID = %s"
        val = (member.id, )
        db.cur.execute(sql, val)
        result = db.cur.fetchone()
        if result is None:
            print(f"User not in DB yet")
            await userfunction.AddMember(self, member)

    #Add new joining members to the database
    @commands.Cog.listener()
    async def on_member_join(self, member):
        userfunction.AddMember(self, member)


async def setup(client):
    await client.add_cog(userfunction(client))

async def teardown(client):
    return
