from cogs.leaderboard.filter import FilterInstance


class LeaderboardManager:
    def __init__(self):
        self.leaderboards = {}

    def create_leaderboard(self, member):
        leaderboard = Leaderboard()
        self.leaderboards[member] = leaderboard
        return leaderboard
    
    def destroy_leaderboard(self, member):
        if member in self.leaderboards:
            lb = self.leaderboards[member]
            lb.channel.delete() #TODO: test if it deletes the channel
            # TODO: remove the message from the DB
            #TODO: remove the leaderboard from the dictionary of filters and data

            del self.leaderboards[member]
        pass
    def get_all(self):
        return self.leaderboards

leaderboard_manager = LeaderboardManager()
class Leaderboard:
    def __init__(self, member):
        # TODO: 3. Test filter creation
        self.filter = FilterInstance("today_study_exclude_no_cam")
        # I have to get the data
        self.bot = bot
        self.channel = create_private_channel(member)
        self.message = get_message(member, channel)
        

        #TODO: TEST
        def create_private_channel(self, member):
            overwrites = {
                self.bot.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await self.bot.guild.create_text_channel('private-channel', overwrites=overwrites)
            return await.channel.send(f'Hey {member.mention}, I created {channel.mention} for you!')
        
        #TODO: TEST
        def get_message(self, member, channel):
        # if there is a message id in the DB and I can fetch it #TODO: create message id in SQL
            # self.message = await self.bot.get_channel(channel_id).fetch_message(message_id)
            # return message
        self.message = await self.bot.get_channel(channel_id).send("Loading...")
        return self.message
        
        # TODO: I need a function to destroy the leaderboard, call that function when the user leaves the channel
        
        # when leaderboard gets created:
        # send the leaderboard image to the channel
        message_id = None   # store the message id in the leaderboard object

        # self.data = self.get_data()
        # self.image = self.create_image(self.data)
    
    # create a channel that only the user can see
        

@bot.command()
async def create_private_channel(ctx, member: discord.Member):
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True)
    }

    channel = await ctx.guild.create_text_channel('private-channel', overwrites=overwrites)
    await ctx.send(f'Hey {member.mention}, I created {channel.mention} for you!')
    def get_data(self):
        arr = db.get_entries_within_range(
            filter
        )  # Assuming this function is now synchronous
        arr = sum_durations(arr)
        return arr

    def create_image(self, data):
        img = create_leaderboard_image(data)
        return img
