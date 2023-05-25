my_dict = {1: 100}
levels = {1: 100}
experience = 500
from easy_pil import Editor, Canvas
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


    current_lvl = list(levels)[(UserLevel-1)]
    next_lvl = list(levels)[(UserLevel)]

    curlvlxp = levels[(UserLevel)]
    nextlvlxp = levels[(UserLevel+1)]

    hundertprozent = nextlvlxp - curlvlxp
    missingxp = nextlvlxp - experience
    alreadydone = (experience - curlvlxp)

    percentage = (alreadydone / missingxp) * 100

    print(f"current level: {current_lvl}  next level: {next_lvl}  {nextlvlxp}")
    print(f"100% = {hundertprozent} currently: {alreadydone} missing: {missingxp}")
    print(percentage)


checkNewLevel(3, 500)

"""percentage =
    LVL+1 - LVL = 100%"""


canvas = Canvas((900, 300), color="black")

editor = Editor(canvas)
#editor.rectangle((100,150), 600, 40, outline="white", radius=12, stroke_width=2)
#editor.ellipse((100, 150), 100, 100, outline="gray", stroke_width=5)

background = Editor("assets/background/background2.png")

square = Canvas((300,300))
squaqre = Editor(canvas=square)
square.rotate(45)

background.paste ((600, 0), square.image)

background.show()

#bot.run("ODM5MDg5NjU1MTg5ODY0NTA4.YJElIw.8v1pOwMXScG-HF7LCQnDAybNiQk")