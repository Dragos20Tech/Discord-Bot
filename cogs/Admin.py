import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # BANNING
    @commands.command(pass_context=True)
    @has_permissions(ban_members=True)  # checking if the user has a role that allows him to BAN people
    async def ban(self, ctx, username, *, reason="for violating server rules"):
        if not isinstance(reason, str):
            await ctx.send("Invalid reason. Please provide a valid string for the reason.")
            return

        username = username.lower()

        member = discord.utils.find(lambda m: m.display_name.lower() == username, ctx.guild.members)

        if member:
            if member.bot:
                await ctx.send("I do not have the appropriate permissions to ban that user.")
            else:
                await member.ban(reason=reason)
                await ctx.send(f'User {member.display_name} has been banned from the server {reason}')
        else:
            await ctx.send("User not found or the name doesn't match any members.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban people!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Who do you want to ban?")

    # KICKING
    @commands.command(pass_context=True)
    @has_permissions(kick_members=True)
    async def kick(self, ctx, username, *, reason="for violating server rules"):
        if not isinstance(reason, str):
            await ctx.send("Invalid reason. Please provide a valid string for the reason.")
            return

        username = username.lower()

        # Check if the lowercase username matches any member's lowercase display name
        member = discord.utils.find(lambda m: m.display_name.lower() == username, ctx.guild.members)

        if member:
            if member.bot:
                await ctx.send("I do not have the appropriate permissions to kick that user.")
            else:
                await member.kick(reason=reason)
                await ctx.send(f'User {member.display_name} has been kicked from the server {reason}')
        else:
            await ctx.send("User not found or the name doesn't match any members.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick people!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Who do you want to kick?")


async def setup(Bot):
    await Bot.add_cog(Admin(Bot))
