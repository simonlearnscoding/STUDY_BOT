from discord.ext import commands
import discord
class vc(commands.Cog):

    def __init__(self, client):
        self.client = client

    bot_spam = None
    vc_chat = None
    guild = None
    Testing = False
    vc_role = None
    questions= None
    challengeName1 = None
    challenge_1 = None
    challenge_2 = None

    def getmember(id):
        print(vc.guild)
        return vc.guild.get_member(id)
        #return self.get_guild(id)
    #def get_channel(id):

    def start(self, Testing):
        if Testing == True:
            vc.guild = self.get_guild(917547601539264623)
            vc.challenge_1 = self.get_channel(939252150385655838)
            vc.challenge_2 = self.get_channel(939252226118013019)



        else:
            vc.guild = self.get_guild(789814373434654731)
            vc.challenge_1 = self.get_channel(937645950695010315)
            vc.challenge_2 = self.get_channel(937646602527588352)

        vc.bot_spam = vc.guild.get_channel(vc.lions_cage_text_id)
        vc.vc_chat = vc.guild.get_channel(vc.chores_vc_id)
        vc.questions = vc.guild.get_channel(vc.questions_id)



    if Testing is False:

        questions_id= 960144604206858320
        general_id = 797837772005179433
        guild_id = 789814373434654731
        sparta_id = 834144065133740102
        study_id = 819680519063207966
        producing_id = 825827777671593994
        challenge_role_id = 882603261910204416
        tasks_id = 915180477269299201
        weekly_message = 923159773464121354
        daily_message = 916518831676071946
        vc_role = 829059975585595393


        bot_id = 827601223317585991
        lions_cage_id = 834118898836045894
        lions_cage_text_id = 838840054125297664
        chores_vc_id = 829061149986914345
        workout_id = 789814373870075931
        timer_id = 839100861497606174
        yoga_id = 793533479476264970
        reading_id = 820760890093338634
        chores_id = 845241122116075520
        meditation_id = 790609301911502908
        doing_drugs_id = 840346309470322738
        creative_id = 824040394761306192
        gestapo = 842832674543501353
        leaderboard = 916484382091513917
        vibing_id = 789814373870075932
        challenge_1 = 937645950695010315
        challenge_2 = 937646602527588352
        focused_role = 960522808264376370

        challenge_role_1 = 939465581936144405
        challenge_role_2 = 939465659211984936

        Augustus = "/home/code/14_11_21/assets/font/Augustus.ttf"
        SmallFont = "/home/code/14_11_21/assets/font/Romanica.ttf"
        SmallerFont = "/home/code/14_11_21/assets/font/Romanica.ttf"



    else:
        # TESTING
        Augustus = "C:/Code/SPQR_VPS/assets/font/Augustus.ttf"
        SmallFont = "C:/Code/SPQR_VPS/assets/font/Romanica.ttf"
        SmallerFont = "C:/Code/SPQR_VPS/assets/font/Romanica.ttf"
        vc_role = 917547601551822871
        focused_role = 960521990068895794
        questions_id = 917547601753178207
        general_id = 917547601753178207
        guild_id = 917547601539264623
        tasks_id = 917547601753178210
        sparta_id = 917547601753178213
        study_id = 917547601753178212
        producing_id = 917547602076135483
        challenge_role_id = 917547601564426297
        weekly_message = 923155569932664842
        daily_message = 923131822999736340
        challenge_1 = 939252150385655838
        challenge_2 = 939252226118013019

        bot_id = 827601223317585991
        lions_cage_id = 834118898836045894
        lions_cage_text_id = 917547602277453862
        chores_vc_id = 917547601753178211
        workout_id = 917547601904148526
        timer_id = 917547601753178205
        yoga_id = 917547601904148527
        reading_id = 917547601904148521
        chores_id = 917547601904148522
        meditation_id = 917547601904148520
        doing_drugs_id = 917547602420064297
        creative_id = 917547602076135479
        bots_id = 917547602277453857
        gestapo = 917547602277453859
        leaderboard = 917547601753178209
        vibing_id = 917547602076135478
        challenge_role_1 = 939464453357994014
        challenge_role_2 = 939464510425665606



async def setup(client):
    await client.add_cog(vc(client))

async def teardown(client):
    return
