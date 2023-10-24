from discord.ext import commands


class Handling_errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Well done! You\'ve just discovered a new MissingPermissions error that I have to fix!')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Well done! You\'ve just discovered a new MissingRequiredArgument error that I have to fix!')


async def setup(bot):
    await bot.add_cog(Handling_errors(bot))
