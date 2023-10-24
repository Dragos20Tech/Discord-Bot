import discord
from discord.ext import commands


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title="Test",
                              url="https://google.com",
                              description="Google it!",
                              color=0x005B41)
        embed.set_author(name=ctx.author.display_name,
                         url="https://github.com/Dragos20Tech",
                         icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTamJsRrarmGg7NvJPn4iedRck8aV-kmBHD7w&usqp=CAU")
        embed.add_field(name="Labradore", value="Cute dogs", inline=True)
        embed.add_field(name="Pugs", value="Cute dogs", inline=True)
        embed.set_footer(text="Thanks for reading!")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Embed(bot))
