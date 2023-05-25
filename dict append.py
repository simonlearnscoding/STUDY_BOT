my_dict = {1: 100}
levels = {1: 100}
experience = 500
from easy_pil import Editor, Canvas, Font, load_image_async
import discord
from discord.ext import commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "*", intents = intents)
from discord import file

Augustus= Font("C:/Code/SPQR_VPS/assets/font/Augustus.ttf", size=28)
SmallFont= Font("C:/Code/SPQR_VPS/assets/font/Romanica.ttf", size=24)
SmallerFont= Font("C:/Code/SPQR_VPS/assets/font/Romanica.ttf", size=16)
currentLevel = 1
def checkNewLevel(currentLevel, experience):
    """if LVL is None:
        LVL = 1"""
    #Calculate Levels List
    for i in range(2, 300):
        levels[i] = round(((levels[i - 1] + 100) * 1.06) / 10) * 10

    print(levels)
    #calculate current level
    i = 1
    UserLevel = 0
    while experience > levels[i]:
        UserLevel = UserLevel + 1
        i = i+1

    if UserLevel > currentLevel:
        #message to user
        print(f"user rised in level!! {UserLevel}")
        #update user.lvl




"""percentage =
    LVL+1 - LVL = 100%"""


def DisplayLevel(xp, lvl):
    """if LVL is None:
        LVL = 1"""
    #Calculate Levels List
    for i in range(2, 300):
        levels[i] = round(((levels[i - 1] + 100) * 1.06) / 10) * 10

    current_lvl = list(levels)[(lvl-1)]
    next_lvl = list(levels)[(lvl)]

    curlvlxp = levels[(lvl)]
    nextlvlxp = levels[(lvl+1)]

    missingxp = nextlvlxp - experience
    alreadydone = (experience - curlvlxp)
    percentage = round((alreadydone / missingxp) * 100)

    print(f"current level: {current_lvl}  next level: {next_lvl}  {nextlvlxp}")
    print(f"100% = {hundertprozent} currently: {alreadydone} missing: {missingxp}")
    print(percentage)

@client.event
async def on_message(message):

    if message.author.bot:
        return

    """if LVL is None:
        LVL = 1"""
    #Calculate Levels List
    for i in range(2, 300):
        levels[i] = round(((levels[i - 1] + 100) * 1.06) / 10) * 10

    current_lvl = list(levels)[(lvl-1)]
    next_lvl = list(levels)[(lvl)]

    curlvlxp = levels[(lvl)]
    nextlvlxp = levels[(lvl+1)]

    missingxp = nextlvlxp - experience
    alreadydone = (experience - curlvlxp)
    percentage = round((alreadydone / missingxp) * 100)

    print(f"current level: {current_lvl}  next level: {next_lvl}  {nextlvlxp}")
    print(f"100% = {hundertprozent} currently: {alreadydone} missing: {missingxp}")
    print(percentage)




    canvas = Canvas((900, 300), color="black")

    profile = Editor("C:/Code/SPQR_VPS/assets/background/pfp.jpeg").resize((150, 150))
    profile = await load_image_async(str(message.author.avatar))


    profile = Editor(profile).resize((140, 140)).circle_image()

    editor = Editor(canvas)
    # editor.rectangle((100,150), 600, 40, outline="white", radius=12, stroke_width=2)
    # editor.ellipse((100, 150), 100, 100, outline="gray", stroke_width=5)

    background = Editor("C:/Code/SPQR_VPS/assets/background/background2.png").resize((550, 300))
    square = Canvas((500, 500), "white")
    square = Editor(square)
    square.rotate(30, expand=True)
    background.paste(square.image, (600, -250))
    background.paste(profile.image, (16, 16))

    background.rectangle((30, 240), width=490, height=35, fill="white", radius=9)
    background.bar((30, 240), max_width=490, height=35, percentage=30, fill="#adf7b6", radius=9)  # a9cef4
    background.text((200, 25), str(f"{message.author.name}"), font=Augustus, color="white")
    background.rectangle((200, 60), width=220, height=1, fill="#adf7b6", )

    background.text((40, 210), "Level: 16", font=SmallFont, color="white")
    background.text((430, 215), "XP: 350/700", font=SmallerFont, color="white")

    file = discord.File(fp=background.image_bytes, filename="card.png")
    await message.channel.send(file=file)

    #background.show()

#editor.show()

client.run("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk")