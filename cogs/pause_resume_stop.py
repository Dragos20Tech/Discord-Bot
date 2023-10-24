import discord
from discord.ext import commands


class PRS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)  # this line of code is like searching through
        # all the voice clients your bot is connected to and picking out the one
        # that's associated with the server (guild) [parameter] where the command
        # was used.

        # ----------------------------- DEBUGGING PURPOSES -----------------------------
        # print("--------------------------------")
        # print(f'Type : {type(voice)}')
        # print(f'{voice}')
        # print(' ')
        # print(f'List : {bot.voice_clients}')
        # print(f'Type : {type(ctx.guild)}')
        # print(ctx.guild)
        # print("--------------------------------")
        # ----------------------------- DEBUGGING PURPOSES -----------------------------
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send('There\'s no audio playing!')

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('No audio paused!')

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        await voice_client.disconnect(force=True)
        await ctx.send("Left the voice channel.")


async def setup(Bot):
    await Bot.add_cog(PRS(Bot))


'''
PAUSE,RESUME & STOP COMMANDS


MODULE
discord.utils - A module in 'discord.py' library that provides various utility functions and helpers
                    for working with Discord API objects and data structures.

METHOD
discord.utils.get() - A method used to search and retrieve elements from collections (lists,tuples,dicts,etc.)
                          that contain Discord objects.

PARAMETERS

1. bot.voice_clients - Is a collection (list) that contains voice client objects.
                           A voice client object represents the bot's connection to a voice channel on a specific
                           server (guild).

2.guild = ctx.guild - This is the guild/server (e.g LK4K's Community server) associated with the context 
                          represented by the 'ctx' object. 

                        - It provides information about the server where the command or message originated.

OVERALL ROLE

The discord.utils.get() function is used to search for a voice client within the 'bot.voice_clients' collection 
that is associated with the specific guild (ctx.guild). It returns the first voice client it finds that matches 
this criteria.                       

'''
