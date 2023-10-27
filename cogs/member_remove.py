import discord
from discord.ext import commands


class member_remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):  # triggers as soon as user leaves the server

        # Get the server or guild where the member has joined
        server = member.guild

        # Initializing the variable with the first text-channel of the server
        text_channel = server.text_channels[0]

        # Searches for "general" text-channel
        for channel in server.text_channels:
            if channel.name == 'general':
                text_channel = channel
                break
        # If "general" text-channel not found then it will display the message in the first text-channel of the server

        await text_channel.send(f"Goodbye {member.display_name} !")


async def setup(bot):
    await bot.add_cog(member_remove(bot))
