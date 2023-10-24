import discord
from discord.ext import commands


class member_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):  # triggers as soon as user joins the server

        # Get the server or guild where the member has joined
        server = member.guild

        text_channel = server.text_channels[0]

        # # ----------------------------- DEBUGGING PURPOSES -----------------------------
        # print(type(server.text_channels))
        # print(server.text_channels)
        # print(type(server.text_channels[0]))
        # print(f'First text-channel in the discord server : {server.text_channels[0]}')
        # print(' ')
        # # ----------------------------- DEBUGGING PURPOSES -----------------------------

        for channel in server.text_channels:
            if channel.name == 'general':
                text_channel = channel
                break

        if text_channel is not None:
            await text_channel.send(f"Hello {member.display_name}!  Welcome to my discord server!")
            # 'rj' is a prefix to use in order to call the right variable/function from the other file
            # Hold CTRL + click on 'rj' to go to rapidAPI_Joker.py


async def setup(bot):
    await bot.add_cog(member_join(bot))
