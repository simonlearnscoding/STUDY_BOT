from discord.ext import commands
# THE OTHER PY FILES
import asyncio
from mydb import db
import discord
from discord.ext import commands
from datetime import datetime
#from discord_components import Button, Select, SelectOption, ComponentsBot
import random
import re
from discord.ui import Button, Select
from cogs.levels import levels
# THE OTHER PY FILES
from cogs.vc import vc
import asyncio

# From now, `custom_emojis` is `list` of `discord.Emoji` that `msg` contains.
# client.load_extension("cogs.boot")


class tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
    i = 12
    Message = []
    Message2 = []


    def resetDay(self, userid):

        sql = f"delete from users.tasks where userid = {userid};"
        db.cur.execute(sql, )
        db.mydb.commit()
        sql = f"delete from users.taskmessageid where userid = {userid};"
        db.cur.execute(sql, )
        db.mydb.commit()

    async def colour(ctx, message):
        """Sends a message with our dropdown containing colours"""

        sql = f"SELECT taskname, taskid FROM users.tasks where userid ={message.author.id} and Done = 0"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        #await tasks.colour(message.channel, message)
        # Create the view containing our dropdown
        view = tasks.DropdownView()
        options = []
        for j in range(len(result)):
            label = result[j][0]
            value = result[j][1]
            #tasks.Options.append(discord.SelectOption(label=label, value=value))
            options.append(discord.SelectOption(label=label, emoji='🔳', value=value))

        if len(options) == 0:
            options.append(discord.SelectOption(label='nothing left to do for today!', emoji='🌞'))


        view.children[0].options = options

        sql = f"SELECT taskname, Starttime FROM users.tasks where userid ={message.author.id} and CurrentlyWorking = 1"
        db.cur.execute(sql, )
        Result = db.cur.fetchone()

        Embed = discord.Embed()

        sql = f"SELECT taskname, CurrentlyWorking, Done, WorkingMinutes FROM users.tasks where userid ={message.author.id}"
        db.cur.execute(sql, )
        result = db.cur.fetchall()

        if message.content.startswith("!Tasks"):
            Tasks = ""
            Minutes = ""
            for i in range(len(result)):
                append = ""
                if(result[i][1]) == 1:
                    append = "⌛ "
                elif (result[i][2]) == 1:
                    append = "✅ "
                else:
                    append = "🔳 "
                Tasks = Tasks + str(f"{append} {result[i][0]}\n")

            Embed.add_field(
                name=f"Tasks",
                value=f"{Tasks} \n \n \n \n",
                inline=False)
        else:
            pass

        if Result is None:
            view.children[0].placeholder = "Choose a Task"

        else:
            now = datetime.now()
            WorkIntervall = int((now - Result[1]).total_seconds() / 60)
            if WorkIntervall > 60:
                WorkIntervall = round((WorkIntervall / 60), 1)
                WorkIntervall = str(f"{WorkIntervall}h")
            else:
                WorkIntervall = str(f"{WorkIntervall}m")
            view.children[0].placeholder = f"{Result[0]}"
            Embed.add_field(
                name=f"currently doing:  ",
                value=f"{Result[0]} ",
                inline=True)
            Embed.add_field(
                name=f"since  ",
                value=f"{WorkIntervall}",
                inline=True)

        tasks.Message = await ctx.send(embed=Embed, view=view)


        #channel = guild.get_channel(vc.lions_cage_text_id)
        #tasks.Message2 = await channel.send(embed=Embed)


        # Sending a message containing our view

    # Define a simple View that gives us a confirmation menu
    async def updateCurrentlyWorking(self, userid, taskname, username):
        sql = f"SELECT Starttime FROM users.tasks where userid ={userid} and CurrentlyWorking = 1"

        db.cur.execute(sql, )
        result = db.cur.fetchone()
        now = datetime.now()
        if result is None:
            pass
        else:

            WorkIntervall = int((now - result[0]).total_seconds() / 60)
            sql = f"update users.tasks set WorkingMinutes = {WorkIntervall} where userid = {userid} and CurrentlyWorking = 1"
            db.cur.execute(sql, )
            db.mydb.commit()

            sql = f"update users.tasks set Starttime = 0 where userid = {userid} and CurrentlyWorking = 1"
            db.cur.execute(sql, )
            db.mydb.commit()

            sql = f"update users.tasks set CurrentlyWorking = 0 where userid ={userid}"
            db.cur.execute(sql, )
            db.mydb.commit()

        sql = f"update users.tasks set CurrentlyWorking = 1 where taskname =\"{taskname}\" and userid = {userid}"
        db.cur.execute(sql, )
        db.mydb.commit()

        sql = f"update users.tasks set Starttime = %s where taskname =\"{taskname}\""
        val = (now,)
        db.cur.execute(sql, val)
        db.mydb.commit()

        await tasks.editDailyMessage(self, userid, username)

    async def updateSetDoDone(self,userid, taskname, username):
        sql = f"SELECT Starttime FROM users.tasks where userid ={userid} and taskname= \"{taskname}\""
        db.cur.execute(sql, )
        result = db.cur.fetchone()
        now = datetime.now()
        if result[0] is None:
            sql = f"update users.tasks set WorkingMinutes = 0 where userid = {userid} and taskname= \"{taskname}\""
            db.cur.execute(sql, )
            db.mydb.commit()
        else:
            WorkIntervall = int((now - result[0]).total_seconds() / 60)
            sql = f"update users.tasks set WorkingMinutes = {WorkIntervall} where userid = {userid} and taskname= \"{taskname}\""
            db.cur.execute(sql, )
            db.mydb.commit()




        sql = f"update users.tasks set Done = 1 where userid = {userid} and taskname= \"{taskname}\" "
        db.cur.execute(sql, )
        db.mydb.commit()

        sql = f"update users.tasks set CurrentlyWorking = 0 where userid ={userid}"
        db.cur.execute(sql, )
        db.mydb.commit()

        sql = f"SELECT taskname, taskid FROM users.tasks where userid ={userid} and Done = 0"

        db.cur.execute(sql, )
        result = db.cur.fetchall()
        # await tasks.colour(message.channel, message)
        # Create the view containing our dropdown
        view = tasks.DropdownView()
        options = []
        for j in range(len(result)):
            label = result[j][0]
            value = result[j][1]
            # tasks.Options.append(discord.SelectOption(label=label, value=value))
            options.append(discord.SelectOption(label=label, emoji='🔳', value=value))

        Embedd = discord.Embed()
        xp = 10
        Embedd.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
        Embedd.add_field(name=f"{username}, completed a Task",
                         value=f"+ {xp}xp",
                         inline=False)
        guild = self.client.get_guild(vc.guild_id)
        member = guild.get_member(userid)
        if member.voice is not None:
            channel = guild.get_channel(vc.chores_vc_id)
            message = await channel.send(embed=Embedd)
            await asyncio.sleep(1)
            await message.delete()
        else:
            channel = guild.get_channel(vc.lions_cage_text_id)
            message = await channel.send(embed=Embedd)

            await message.delete()
        # add xp
        await levels.addXP(member, xp)

        if len(options) == 0:

            #give user +50
            Embedd = discord.Embed()
            xp = 50
            Embedd.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
            Embedd.add_field(name=f"{username},Completed everything today!!",
                            value=f"+ {xp}xp",
                            inline=False)
            guild = self.client.get_guild(vc.guild_id)
            member = guild.get_member(userid)
            if member.voice is not None:
                channel = guild.get_channel(vc.chores_vc_id)
                message = await channel.send(embed=Embedd)
                await asyncio.sleep(1)
                await message.delete()
            else:
                channel = guild.get_channel(vc.lions_cage_text_id)
                message = await channel.send(embed=Embedd)

            # add xp
            await levels.addXP(member, xp)

            options.append(discord.SelectOption(label='nothing left to do for today!', emoji='🌞'))

        view.children[0].options = options


        Embed = discord.Embed()

        sql = f"SELECT taskname, CurrentlyWorking, Done FROM users.tasks where userid ={userid}"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        Tasks = ""
        for i in range(len(result)):
            append = ""
            if (result[i][1]) == 1:
                append = "⌛ "
            elif (result[i][2]) == 1:
                append = "✅ "
            else:
                append = "🔳 "

            Tasks = Tasks + str(f"{append} {result[i][0]}\n")

        Embed.add_field(
            name=f"Tasks",
            value=f"{Tasks} \n\n",
            inline=False)

        await tasks.editDailyMessage(self, userid, username)
    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message('Confirming', ephemeral=True)
            self.value = True
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message('Cancelling', ephemeral=True)
            self.value = False
            self.stop()

    class Button(discord.ui.Button):
        def __init__(self):
            # Set the options that will be presented inside the dropdown
            label="Done"
            style=discord.ButtonStyle.primary
            emoji='✅'

        async def callback(self, interaction: discord.Interaction):
            print(interaction)


    class Dropdown(discord.ui.Select):
        def __init__(self):
            # Set the options that will be presented inside the dropdown
            options = [
            ]

            # The placeholder is what will be shown when no option is chosen
            # The min and max values indicate we can only pick one of the three options
            # The options parameter defines the dropdown options. We defined this above
            super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

        async def callback(self, interaction: discord.Interaction):
            # Use the interaction object to send a response message containing
            # the user's favourite colour or choice. The self object refers to the
            # Select object, and the values attribute gets a list of the user's
            # selected options. We only want the first one.

            #await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')
            sql = f"SELECT Starttime FROM users.tasks where userid ={interaction.user.id} and CurrentlyWorking = 1"

            db.cur.execute(sql, )
            result = db.cur.fetchone()
            now = datetime.now()
            if result is None:
                pass
            else:

                WorkIntervall = int((now - result[0]).total_seconds() / 60)
                sql = f"update users.tasks set WorkingMinutes = {WorkIntervall} where userid = {interaction.user.id} and CurrentlyWorking = 1"
                db.cur.execute(sql, )
                db.mydb.commit()

            sql = f"update users.tasks set Starttime = 0 where userid = {interaction.user.id} and CurrentlyWorking = 1"
            db.cur.execute(sql, )
            db.mydb.commit()

            sql = f"update users.tasks set CurrentlyWorking = 0 where userid ={interaction.user.id}"
            db.cur.execute(sql, )
            db.mydb.commit()

            sql = f"update users.tasks set CurrentlyWorking = 1 where taskid ={self.values[0]}"
            db.cur.execute(sql, )
            db.mydb.commit()

            sql = f"update users.tasks set Starttime = %s where taskid ={self.values[0]}"
            val = (now, )
            db.cur.execute(sql, val)
            db.mydb.commit()

            sql = f"SELECT taskname, taskid FROM users.tasks where userid ={interaction.user.id} and Done = 0"

            db.cur.execute(sql, )
            result = db.cur.fetchall()
            # await tasks.colour(message.channel, message)
            # Create the view containing our dropdown
            view = tasks.DropdownView()
            options = []
            for j in range(len(result)):
                label = result[j][0]
                value = result[j][1]
                # tasks.Options.append(discord.SelectOption(label=label, value=value))
                options.append(discord.SelectOption(label=label, emoji='🔳', value=value))

            view.children[0].options = options
            Embed = discord.Embed()

            sql = f"SELECT taskname, CurrentlyWorking, Done FROM users.tasks where userid ={interaction.user.id}"
            db.cur.execute(sql, )
            result = db.cur.fetchall()

            Tasks = ""
            for i in range(len(result)):
                append = ""
                if (result[i][1]) == 1:
                    append = "⌛ "
                elif (result[i][2]) == 1:
                    append = "✅ "
                else:
                    append = "🔳 "

                Tasks = Tasks + str(f"{append} {result[i][0]}\n")
            Embed.add_field(
                name=f"Tasks",
                value=f"{Tasks} \n\n",
                inline=False)

            sql = f"SELECT taskname, Starttime FROM users.tasks where userid ={interaction.user.id} and CurrentlyWorking = 1"
            db.cur.execute(sql, )
            Result = db.cur.fetchone()
            if Result is None:
                view.children[0].placeholder = "Choose a Task"
                await tasks.Message.edit(view=view)
            else:
                now = datetime.now()
                WorkIntervall = int((now - Result[1]).total_seconds() / 60)
                if WorkIntervall > 60:
                    WorkIntervall = round((WorkIntervall / 60), 1)
                    WorkIntervall = str(f"{WorkIntervall}h")
                else:
                    WorkIntervall = str(f"{WorkIntervall}m")
                view.children[0].placeholder = f"{Result[0]}"

                Embed.add_field(
                    name=f"currently:  ",
                    value=f"{Result[0]} ",
                    inline=True)
                Embed.add_field(
                    name=f"since  ",
                    value=f"{WorkIntervall}",
                    inline=True)


            await tasks.Message.edit(embed=Embed, view=view)
            await tasks.editDailyMessage(interaction.client, interaction.user.id, interaction.user.name)

    class DropdownView(discord.ui.View):
        def __init__(self):
            super().__init__()

            # Adds the dropdown to our view object.
            self.add_item(tasks.Dropdown())

            button = Button(label="Done", style=discord.ButtonStyle.primary,emoji='✅')
            async def button_callback(interaction):

                # await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')
                sql = f"SELECT Starttime FROM users.tasks where userid ={interaction.user.id} and CurrentlyWorking = 1"

                db.cur.execute(sql, )
                result = db.cur.fetchone()
                now = datetime.now()
                if result is None:
                    return
                if result[0] is not None:
                    WorkIntervall = int((now - result[0]).total_seconds() / 60)
                    sql = f"update users.tasks set WorkingMinutes = {WorkIntervall} where userid = {interaction.user.id} and CurrentlyWorking = 1"
                    db.cur.execute(sql, )
                    db.mydb.commit()

                sql = f"update users.tasks set Done = 1 where userid = {interaction.user.id} and CurrentlyWorking = 1"
                db.cur.execute(sql, )
                db.mydb.commit()

                sql = f"update users.tasks set CurrentlyWorking = 0 where userid ={interaction.user.id}"
                db.cur.execute(sql, )
                db.mydb.commit()


                sql = f"SELECT taskname, taskid FROM users.tasks where userid ={interaction.user.id} and Done = 0"

                db.cur.execute(sql, )
                result = db.cur.fetchall()
                # await tasks.colour(message.channel, message)
                # Create the view containing our dropdown
                view = tasks.DropdownView()
                options = []
                for j in range(len(result)):
                    label = result[j][0]
                    value = result[j][1]
                    # tasks.Options.append(discord.SelectOption(label=label, value=value))
                    options.append(discord.SelectOption(label=label, emoji='🔳', value=value))

                Embedd = discord.Embed()
                xp = 10
                Embedd.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
                Embedd.add_field(name=f"{interaction.user.name}, completed a Task",
                                 value=f"+ {xp}xp",
                                 inline=False)
                guild = interaction.client.get_guild(vc.guild_id)
                member = guild.get_member(interaction.user.id)
                if member.voice is not None:
                    channel = guild.get_channel(vc.chores_vc_id)
                    message = await channel.send(embed=Embedd)
                    await asyncio.sleep(1)
                    await message.delete()
                else:
                    channel = guild.get_channel(vc.lions_cage_text_id)
                    message = await channel.send(embed=Embedd)

                    await message.delete()
                # add xp
                await levels.addXP(member, xp)
                if len(options) == 0:
                    options.append(discord.SelectOption(label='nothing left to do for today!', emoji='🌞'))
                    # give user +50
                    Embedd = discord.Embed()
                    xp = 50
                    Embedd.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
                    Embedd.add_field(name=f"{interaction.user.name},Completed everything today!!",
                                     value=f"+ {xp}xp",
                                     inline=False)
                    guild = interaction.client.get_guild(vc.guild_id)
                    member = guild.get_member(interaction.user.id)
                    if member.voice is not None:
                        channel = guild.get_channel(vc.chores_vc_id)
                        await asyncio.sleep(1)
                        message = await channel.send(embed=Embedd)
                        await asyncio.sleep(1)
                        await message.delete()
                    else:
                        channel = guild.get_channel(vc.lions_cage_text_id)
                        message = await channel.send(embed=Embedd)

                    # add xp
                    await levels.addXP(member, xp)
                view.children[0].options = options

                sql = f"SELECT taskname, Starttime FROM users.tasks where userid ={interaction.user.id} and CurrentlyWorking = 1"
                db.cur.execute(sql, )
                Result = db.cur.fetchone()
                Embed = discord.Embed()

                sql = f"SELECT taskname, CurrentlyWorking, Done FROM users.tasks where userid ={interaction.user.id}"
                db.cur.execute(sql, )
                result = db.cur.fetchall()
                Tasks = ""
                for i in range(len(result)):
                    append = ""
                    if (result[i][1]) == 1:
                        append = "⌛ "
                    elif (result[i][2]) == 1:
                        append = "✅ "
                    else:
                        append = "🔳 "

                    Tasks = Tasks + str(f"{append} {result[i][0]}\n")

                Embed.add_field(
                    name=f"Tasks",
                    value=f"{Tasks} \n\n",
                    inline=False)

                if Result is None:
                    view.children[0].placeholder = "Choose a Task"
                    await tasks.Message.edit(view=view)

                else:
                    now = datetime.now()
                    WorkIntervall = int((now - Result[1]).total_seconds() / 60)
                    if WorkIntervall > 60:
                        WorkIntervall = round((WorkIntervall / 60), 1)
                        WorkIntervall = str(f"{WorkIntervall}h")
                    else:
                        WorkIntervall = str(f"{WorkIntervall}m")
                    view.children[0].placeholder = f"{Result[0]}"
                    Embed.add_field(
                        name=f"currently:  ",
                        value=f"{Result[0]} ",
                        inline=True)
                    Embed.add_field(
                        name=f"since  ",
                        value=f"{WorkIntervall}",
                        inline=True)

                await tasks.Message.edit(embed=Embed, view=view)
                await tasks.editDailyMessage(interaction.client, interaction.user.id, interaction.user.name)





            button.callback = button_callback

            self.add_item(button)

            buttonDone = Button(label="Close Window", style=discord.ButtonStyle.secondary,emoji='❌')
            buttonPause = Button(label="Pause", style=discord.ButtonStyle.grey,emoji='▶')
            async def button_callback3(interaction):




                # await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')
                sql = f"SELECT Starttime FROM users.tasks where userid ={interaction.user.id} and CurrentlyWorking = 1"

                db.cur.execute(sql, )
                result = db.cur.fetchone()
                now = datetime.now()
                if result is None:
                    pass
                else:

                    WorkIntervall = int((now - result[0]).total_seconds() / 60)
                    sql = f"update users.tasks set WorkingMinutes = {WorkIntervall} where userid = {interaction.user.id} and CurrentlyWorking = 1"
                    db.cur.execute(sql, )
                    db.mydb.commit()

                sql = f"update users.tasks set Starttime = 0 where userid = {interaction.user.id} and CurrentlyWorking = 1"
                db.cur.execute(sql, )
                db.mydb.commit()

                sql = f"update users.tasks set CurrentlyWorking = 0 where userid ={interaction.user.id}"
                db.cur.execute(sql, )
                db.mydb.commit()

                sql = f"SELECT taskname, taskid FROM users.tasks where userid ={interaction.user.id} and Done = 0"

                db.cur.execute(sql, )
                result = db.cur.fetchall()
                # await tasks.colour(message.channel, message)
                # Create the view containing our dropdown
                view = tasks.DropdownView()
                options = []
                for j in range(len(result)):
                    label = result[j][0]
                    value = result[j][1]
                    # tasks.Options.append(discord.SelectOption(label=label, value=value))
                    options.append(discord.SelectOption(label=label, emoji='🔳', value=value))

                if len(options) == 0:
                    options.append(discord.SelectOption(label='nothing left to do for today!', emoji='🌞'))

                view.children[0].options = options

                sql = f"SELECT taskname, Starttime FROM users.tasks where userid ={interaction.user.id} and CurrentlyWorking = 1"
                db.cur.execute(sql, )
                Result = db.cur.fetchone()
                Embed = discord.Embed()

                sql = f"SELECT taskname, CurrentlyWorking, Done FROM users.tasks where userid ={interaction.user.id}"
                db.cur.execute(sql, )
                result = db.cur.fetchall()
                Tasks = ""
                for i in range(len(result)):
                    append = ""
                    if (result[i][1]) == 1:
                        append = "⌛ "
                    elif (result[i][2]) == 1:
                        append = "✅ "
                    else:
                        append = "🔳 "

                    Tasks = Tasks + str(f"{append} {result[i][0]}\n")

                Embed.add_field(
                    name=f"Tasks",
                    value=f"{Tasks} \n\n",
                    inline=False)

                if Result is None:
                    view.children[0].placeholder = "Choose a Task"
                    await tasks.Message.edit(view=view)

                else:
                    now = datetime.now()
                    WorkIntervall = int((now - Result[1]).total_seconds() / 60)
                    if WorkIntervall > 60:
                        WorkIntervall = round((WorkIntervall / 60), 1)
                        WorkIntervall = str(f"{WorkIntervall}h")
                    else:
                        WorkIntervall = str(f"{WorkIntervall}")
                    view.children[0].placeholder = f"{Result[0]}"
                    Embed.add_field(
                        name=f"currently:  ",
                        value=f"{Result[0]} ",
                        inline=True)
                    Embed.add_field(
                        name=f"since  ",
                        value=f"{WorkIntervall} h",
                        inline=True)

                await tasks.Message.edit(embed=Embed, view=view)
                await tasks.editDailyMessage(interaction.client, interaction.user.id, interaction.user.name)


            buttonPause.callback = button_callback3

            async def button_callback2(interaction):
                await tasks.Message.delete()

            buttonDone.callback = button_callback2
            self.add_item(buttonPause)
            self.add_item(buttonDone)

    async def createEmbedContent(self, name, id):
        Embed = discord.Embed(
            title=f"{name}'s Tasks of the Day",
            color=discord.Colour.blue())
        sql = f"SELECT taskname, CurrentlyWorking, Done, WorkingMinutes FROM users.tasks where userid ={id}"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        Tasks = ""
        Minutes = ""
        for i in range(len(result)):
            append = ""
            if (result[i][1]) == 1:
                append = "⌛ "
            elif (result[i][2]) == 1:
                append = "✅ "
            else:
                append = "🔳 "
            Tasks = Tasks + str(f"{append} {result[i][0]}\n")

        for i in range(len(result)):

            if (result[i][3]) > 0:
                append = f"{result[i][3]} m"
            else:
                append = "-"
            Minutes = Minutes + str(f"{append}\n")


        Embed.add_field(
            name=f"Tasks",
            value=f"{Tasks} \n\n",
            inline=True)

        Embed.add_field(
            name=f"Time",
            value=f"{Minutes}",
            inline=True)
        return Embed

    async def createDailyMessage(self, id, name):
        guild = self.client.get_guild(vc.guild_id)
        channel = guild.get_channel(vc.tasks_id)
        Embed = await tasks.createEmbedContent(self, name, id)

        Message = await channel.send(embed=Embed)
        sql = "INSERT INTO users.taskmessageid (userid, messageid) VALUES (%s, %s)"
        val = (id, Message.id)
        db.cur.execute(sql, val)
        db.mydb.commit()
        print("create task message")

    async def editDailyMessage(self, id, name):

        #get task ID
        sql = f"SELECT messageid FROM users.taskmessageid where userid = {id}"
        db.cur.execute(sql, )
        messageid = db.cur.fetchone()
        messageid = int(messageid[0])
        print(messageid)

        try:
            guild = self.client.get_guild(vc.guild_id)
        except:
            guild = self.get_guild(vc.guild_id)
        channel = guild.get_channel(vc.tasks_id)
        Message = await channel.fetch_message(messageid)
        Embed = await tasks.createEmbedContent(self, name, id)
        await Message.edit(embed=Embed)

    async def selectBoxTesting(self, result, message):

        tasks.Options = []
        for j in range(len(result)):
            label = result[j][0]
            value = result[j][1]
            tasks.Options.append(discord.SelectOption(label=label, value=value))

        item = discord.ui.View(timeout=200.0,)
        item.add_item(Select(placeholder='currently working on...',
               options=
               tasks.Options
               , custom_id='selectTesting'))
        # [Button(label="Done", style=3, custom_id="button_done"),
        # Button(label="Pause", style=4, custom_id="button_pause"),]

        #interaction=await tasks.bot.wait_for('select_option')
        #print(interaction.values[0])
        #await interaction.send(content="Button clicked!")


    async def matchResult(userid, taskContent):

        sql = f"SELECT taskname FROM users.tasks where userid ={userid} and Done = 0"
        db.cur.execute(sql, )
        result = db.cur.fetchall()
        if (len(result)) == 0:
            print("no matches found")
        matches = []
        for i in range(len(result)):
            task = str(result[i][0]).lower()
            taskContent = taskContent.lower()
            match = re.search(taskContent, task)
            if match != None:
                print(match)
                matches.append(task)
        return matches

    async def matchesfound(matches, channel):
        if (len(matches)) == 0:
            Message = await channel.send("no matches found")
            await asyncio.sleep(2)
            await Message.delete()
        elif (len(matches)) > 1:
            matchmessage = ""
            for i in range(len(matches)):
                matchmessage = matchmessage + f"🔳 {matches[i]} \n"
            Message = await channel.send(f"multiple matches found: \n\n{matchmessage}\n please be more specific")
            await asyncio.sleep(2)
            await Message.delete()
        else:
            return 1

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("+"):

            now = datetime.now()
            n = random.randint(1, 1000000000)
            taskContent =  message.content[1:]
            if (taskContent[0].isspace()):
                taskContent = taskContent[1:]
            sql = "INSERT INTO users.tasks (userid, taskname, CurrentlyWorking, Done, Starttime, taskid, WorkingMinutes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (message.author.id,taskContent, False, False, 0, n, 0)
            db.cur.execute(sql, val)
            db.mydb.commit()
            if message.channel.id != (vc.lions_cage_text_id):
                await message.delete()

            sql = f"SELECT taskname, taskid FROM users.tasks where userid ={message.author.id}"
            db.cur.execute(sql, )
            result = db.cur.fetchall()
            if (len(result)) == 1:
                await tasks.createDailyMessage(self, message.author.id, message.author.name)

                Embed = discord.Embed()
                Embed.set_thumbnail(url="https://i.pinimg.com/564x/01/3b/89/013b894d6afc51d286cdc3adbb6ffbe8.jpg")
                Embed.add_field(name="setting a goal for the day!",
                                value="+20xp",
                                inline=False)
                Message = await message.channel.send(embed=Embed)
                await asyncio.sleep(1)
                await Message.delete()
                xp = 25
                await levels.addXP(message.author, xp)
            else:
                await tasks.editDailyMessage(self, message.author.id, message.author.name)

        if message.content.startswith("*"):
            # get all tasks in user where done = 0
            taskContent = message.content[1:]
            if (taskContent[0].isspace()):
                taskContent = taskContent[1:]
            if message.channel.id != (vc.lions_cage_text_id):
                await message.delete()
            matches = await tasks.matchResult(message.author.id, taskContent)

            if (await tasks.matchesfound(matches, message.channel)) == 1:
                print(matches[0])
                await tasks.updateCurrentlyWorking(self, message.author.id, matches[0], message.author.name)

        if message.content.startswith("-"):
            # get all tasks in user where done = 0
            taskContent = message.content[1:]
            if (taskContent[0].isspace()):
                taskContent = taskContent[1:]
            if message.channel.id != (vc.lions_cage_text_id):
                await message.delete()
            matches = await tasks.matchResult(message.author.id, taskContent)

            if (await tasks.matchesfound(matches, message.channel)) == 1:
                print(matches[0])
                await tasks.updateSetDoDone(self, message.author.id, matches[0], message.author.name)



            # get user messageid
            # edit message in Tasks

        if (message.content.startswith("!Tasks") or (message.content.startswith("!day"))):
            member = message.author
            sql = f"SELECT taskname, taskid FROM users.tasks where userid ={message.author.id}"
            db.cur.execute(sql, )
            result = db.cur.fetchall()
            try:
                await message.delete()
            except:
                pass
            try:
                await tasks.colour(message.channel, message)
            except:
                if message.content.startswith("!day"):
                    pass
                else:
                    await message.channel.send("You have no Tasks yet - start by adding Tasks for the Day by Typing \"+ This is a Task\" like \n +Doing The Laundry \n * +Doing Homework")








    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        if after.channel.id == vc.tasks_id:
            beforeDone = before.content.count("✅")
            beforeUndone = before.content.count("🔳")
            afterDone = after.content.count("✅")
            afterUndone = after.content.count("🔳")
            if ((beforeDone < afterDone) and (afterUndone == 0) and (beforeUndone > 0)):
                Embed = discord.Embed()
                xp = 50
                Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
                Embed.add_field(name=f"{after.author.name},Completed everything today!!",
                                value=f"+ {xp}xp",
                                inline=False)
                message = await after.channel.send(embed=Embed)

                await asyncio.sleep(1)
                await message.delete()
                # add xp
                await levels.addXP(after.author, xp)


            elif beforeDone < afterDone:
                print("New Tast Completed!")
                Embed = discord.Embed()
                xp = 10
                Embed.set_thumbnail(url="https://wallpaperaccess.com/full/1363541.png")
                Embed.add_field(name=f"{after.author.name},Completed a Task!",
                                value=f"+ {xp}xp",
                                inline=False)
                message = await after.channel.send(embed=Embed)

                await asyncio.sleep(1)
                await message.delete()
                # add xp
                await levels.addXP(after.author, xp)






def setup(client):
    client.add_cog(tasks(client))
