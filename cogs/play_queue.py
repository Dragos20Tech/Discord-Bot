import os
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands

queues = {}


def check_queue(ctx, id):
    if queues.get(id) and queues[id]:  # if queues[LK4K's Community Server] is not empty then
        voice = ctx.guild.voice_client  # get the voice client for the Discord server (guild) to which the 'ctx' belongs.
                                        # voice client is used to manage audio in voice channels on a Discord server.
        source = queues[id].pop(0)  # takes the first audio_file / song from the dictionary (queues) associated with the
                                    # given server (id) and removes it from the dict using '.pop' [built-in function].
        voice.play(source,
                   after=lambda x: check_queue(ctx, id))



class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def play(self, ctx, audio):
        voice = ctx.author.voice
        if voice is None:
            await ctx.send('You need to be in a voice channel to use this command.')
            return

        try:
            audio_file = os.path.join('./Songs', audio + '.mp3')
            if not os.path.isfile(audio_file):
                await ctx.send('The specified audio file does not exist.')
                return

            source = discord.FFmpegPCMAudio(audio_file)

            # Main reason for stopping the currently playing song is to ensure a clean transition
            if ctx.guild.voice_client is not None:  # If there is a song currently playing
                ctx.guild.voice_client.stop()  # Stop the currently playing song
                await ctx.guild.voice_client.disconnect()  # Disconnect the voice client if it's already connected

            voice_client = await voice.channel.connect()
            voice_client.play(source, after=lambda x: check_queue(ctx, ctx.guild.id))

            await ctx.send(f'Now playing: {audio}')

        except discord.Forbidden:
            await ctx.send("I don't have permission to join the voice channel.")
        except discord.HTTPException:
            await ctx.send("An error occurred while attempting to join the voice channel.")
        except FileNotFoundError:
            await ctx.send("File not found.")
        except PermissionError:
            await ctx.send("Permission denied for accessing the file.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
        check_queue(ctx, ctx.guild.id)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an audio file to play.')

    @commands.command(pass_context=True)
    async def queue(self, ctx, audio):
        song = audio + '.mp3'
        audio_file = os.path.join('./Songs', song)

        # Check if the audio file exists
        if not os.path.isfile(audio_file):
            await ctx.send('The specified audio file does not exist.')
            return

        source = FFmpegPCMAudio(audio_file)  # creating an audio source object using FFmpeg

        guild_id = ctx.guild.id  # extracting the unique ID of the server where the command was invoked

        # LK4K's Community server has the ID : 858636428107972618
        # The Odin Project server has the ID : 505093832157691914
        # TPN Labs server has the ID : 333685781862416385

        # You got the idea ;)

        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You are not connected to any voice channel.")
            return

        if guild_id in queues:
            # print("If queue exists then APPEND the 'source' (audio) to that server's queue")
            queues[guild_id].append(source)
        else:
            # print("If there's no queue for that server, it creates a new queue and INITIALIZES it with the 'source'.")
            queues[guild_id] = [source]

        await ctx.send(f'Added {song} to queue')


async def setup(bot):
    await bot.add_cog(Play(bot))


'''
FFmpeg 

It is part of the 'discord.ext' module, specifically in the 'commands' cog.

'FFmpegPCMAudio' is necessary because it allows Discord bots to handle audio playback in a compatible format 
and stream audio from various sources, making it a crucial component for creating Discord bots that interact 
with voice channels.

'FFmpegPCMAudio' is used to convert and stream the audio from the URL or audio file to the voice channel.


! Most audio files, like MP3s, are compressed in formats not directly compatible with Discord. 
  FFmpegPCMAudio is used to convert these various audio formats into a format that Discord can understand, which is PCM.

'''
