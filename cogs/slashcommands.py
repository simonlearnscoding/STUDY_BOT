import discord
from discord import app_commands
from discord.ext import commands
from cogs.tasks import tasks
from discord.app_commands import Choice
from cogs.vc import vc
from cogs.vcroles import vcroles
from cogs.heatmap import heatmap
from cogs.trackingsessions import timeTrack
from cogs.levels import levels



class slashcommands(commands.Cog):


    def __init__(self, client: commands.Bot) -> None:
        self.client = client


    @app_commands.command(
        name="track",
        description="to view how consistent you've been with your habits recently"
    )
    @app_commands.choices(activity = [
        Choice(name="study", value="study"),
        Choice(name="workout", value="workout"),
        Choice(name="meditation", value="meditation"),
        Choice(name="yoga", value="yoga"),
        Choice(name="reading", value="reading"),
        Choice(name="chores", value="chores"),
    ])
    async def track(self, interaction: discord.Interaction,
                        activity: str):
        await interaction.response.send_message(f"showing {interaction.user.name}'s {activity} log", ephemeral=True)
        await heatmap.commandHeatmap(activity, interaction.channel, interaction.user)

    @app_commands.command(
        name="log",
        description="manually track how much time you spent doing things today"
    )
    @app_commands.choices(activity = [
        Choice(name="workout", value="workout"),
        Choice(name="meditation", value="meditation"),
        Choice(name="yoga", value="yoga"),
        Choice(name="reading", value="reading"),
    ])
    async def log(self, interaction: discord.Interaction,
                        activity: str, time: int):
        await timeTrack.addTime(time, interaction.user.id, activity)
        await heatmap.launchHeatmapTracking(activity, interaction.user, interaction.channel)
        await levels.giveXP(interaction.user, time, activity)
        await interaction.response.send_message(f"I added {time} minutes to todays {activity} time", ephemeral=True)


    @app_commands.command(
        name="day",
        description="shows you statistics about your day and your current level"
    )
    async def day(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"your level", ephemeral=True)
        await timeTrack.dayFunction(self, interaction.user, interaction.channel)
        await levels.levelFunction(self, interaction.user, interaction.channel)



    #TODO: Focus
    @app_commands.command(
        name="focus",
        description="will temporarily hide all textchannels so you can focus on your work"
    )
    async def focus(self,
                  interaction: discord.Interaction,
                  minutes: int):
        await interaction.response.send_message(f"I will send you to focusland for {minutes} minutes now. goodluck!",
                                                ephemeral=True)
        await vcroles.focusmode(interaction.user, minutes)






    @app_commands.command(
        name="goal",
        description="Set a goal for how many hours you want to work today"
    )
    async def goal(self,
                  interaction: discord.Interaction,
                  hours: int):
        Nick = f"{interaction.user.name} /{hours}"
        await interaction.user.edit(nick=Nick)
        await interaction.response.send_message(f"you've challenged yourself to work {hours}h today, goodluck!", ephemeral=True)

    @app_commands.command(
        name = "add",
        description="Add a new task to your daily tasklist"
    )
    async def add(self,
                        interaction: discord.Interaction,
                        add: str):

        await  tasks.addTask(self, interaction.user, interaction.channel, add)
        await interaction.response.send_message(f"added _{add}_ to your Tasklist", ephemeral=True)

    @app_commands.command(
        name = "start",
        description="Start working on a Task (Track Time)"
    )
    async def start(self,
                        interaction: discord.Interaction,
                        start: str):
        task = await tasks.workOnTask(self, interaction.user, start, interaction.channel)
        await interaction.response.send_message(f"started working on _{task}_", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(slashcommands(client),
                         guilds = [discord.Object(id=vc.guild_id)])