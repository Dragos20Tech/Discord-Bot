import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):  # triggers as soon as user joins the server

        # Get the server or guild where the member has joined
        server = member.guild

        # Initializing the variable with the first text-channel of the server
        text_channel = server.text_channels[0]

        # # ----------------------------- DEBUGGING PURPOSES -----------------------------
        # print(type(server.text_channels))
        # print(server.text_channels)
        # print(type(server.text_channels[0]))
        # print(f'First text-channel in the discord server : {server.text_channels[0]}')
        # print(' ')
        # # ----------------------------- DEBUGGING PURPOSES -----------------------------

        # Searches for "general" text-channel
        for channel in server.text_channels:
            if channel.name == 'general':
                text_channel = channel
                break
        # If "general" text-channel not found then it will display the message in the first text-channel of the server

        if text_channel is not None:
            await text_channel.send(f"Hello {member.display_name}!  Welcome to my discord server!")


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        server = member.guild

        text_channel = server.text_channels[0]

        for channel in server.text_channels:
            if channel.name == 'general':
                text_channel = channel
                break

        await text_channel.send(f"Goodbye {member.display_name} !")


async def setup(bot):
    await bot.add_cog(Welcome(bot))
