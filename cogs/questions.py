import discord
from discord.ext import commands, tasks
import asyncio
import sys
sys.path.append('/.../')
from datetime import datetime
from mydb import db
import random
from cogs.vc import vc



class questions(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def postQuestion(self):
        questions = await self.getquestions(self)
        n = random.randint(0, (len(questions) - 1))
        user = questions[n][1]
        date = datetime.today().date()
        question = questions[n][0]
        await self.setDateToday(self, question)
        channel = vc.questions
        content = f"Daily Question: **{question}** \n [Asked by: {user}]"
        Messsage = await channel.send(content)
        await Messsage.create_thread(name=f"{date}")

    async def addQuestion(self, name, question):
        sql = f"INSERT INTO users.dailyquestions (question, username, dateused) VALUES (%s, %s, %s);"
        val = (question, name, 0)
        db.cur.execute(sql, val)
        db.mydb.commit()

    async def getquestions(self):
        sql = f"select * from users.dailyquestions where dateused = 0"
        db.cur.execute(sql, )
        return db.cur.fetchall()

    async def setDateToday(self, question):
        print(question)
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        sql=f"update users.dailyquestions SET dateused = %s WHERE question = %s"
        val = (formatted_date, question)
        db.cur.execute(sql, val)
        db.mydb.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        # IGNORE IF MESSAGE FROM A BOT
        if message.author.bot:
            return

        if message.content.startswith('~~'):
            messageContent = message.content[2:]
            username = message.author.name
            await self.addQuestion(username, messageContent)
            print(messageContent, username, datetime.today().date())
            await message.delete()









async def setup(client):
    await client.add_cog(questions(client))

async def teardown(client):
    return