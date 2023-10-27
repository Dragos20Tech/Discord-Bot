import asyncio
import os
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import random
import datetime


# Modify the supported audio file formats here
SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg', '.aac', '.flac', '.m4a', '.aiff', '.wma']

queues = {}


def check_queue(ctx, id):
    if queues.get(id) and len(queues[id]) > 0:
        voice = ctx.guild.voice_client
        if voice and not voice.is_playing():
            source, audio_file = queues[id].pop(0)
            voice.play(source, after=lambda x: check_queue(ctx, id))
    else:
        queues.pop(id, None)


class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def play(self, ctx, *, audio):
        voice = ctx.author.voice
        if voice is None:
            await ctx.send('You need to be in a voice channel to use this command.')
            return

        try:
            voice_client = ctx.guild.voice_client
            audio_files = [f for f in os.listdir('./Songs') if any(f.endswith(ext) for ext in SUPPORTED_FORMATS)]
            # print(audio_files)
            matching_files = []

            for audio_file in audio_files:
                if audio.lower() in audio_file.lower():
                    matching_files.append(audio_file)

            # print(matching_files)

            if not matching_files:
                await ctx.send('No matching audio files found.')
                return
            elif len(matching_files) > 1:
                # If there are multiple matches, let the user choose
                options_text = "Multiple songs found. Please choose one by typing its number:\n"
                for i, song in enumerate(matching_files):
                    song = os.path.splitext(song)[0]
                    options_text += f"```{i + 1}. {song}```\n"

                # Adding the time limit message below the options
                options_text += "\n**You have 30 seconds to pick a song!**"

                embed = discord.Embed(title="Choose a song", description=options_text, color=discord.Color.dark_orange())
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/974/974783.png")

                # Empty field to create space
                embed.add_field(name="\u200b", value="\u200b", inline=False)

                # Adding timestamp with the current date and time
                now = datetime.datetime.now()
                embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                await ctx.send(embed=embed)

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    response = await self.bot.wait_for('message', check=check, timeout=30)
                    choice = int(response.content)
                    if 1 <= choice <= len(matching_files):  # interval : 1 <= x <= y , where y >= x always
                        audio_file = matching_files[choice - 1]
                    else:
                        embed = discord.Embed(title="Random Song",
                                              description="Picked a random song for you ;)",
                                              color=discord.Color.blue())

                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/10097/10097473.png")

                        await ctx.send(embed=embed)
                        audio_file = random.choice(matching_files)
                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout Error",
                                          description="Response timed out. Aborting...",
                                          color=discord.Color.red()

                                          )
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/594/594598.png") # Red X

                    # Adding timestamp with the current date and time
                    now = datetime.datetime.now()
                    embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                    await ctx.send(embed=embed)
                    return
                except ValueError:
                    embed = discord.Embed(title="Value Error",
                                          description="Invalid choice. Aborting...",
                                          color=discord.Color.red())
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/594/594598.png") # Red X

                    # Adding timestamp with the current date and time
                    now = datetime.datetime.now()
                    embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                    await ctx.send(embed=embed)
                    return
            else:
                audio_file = matching_files[0]

            # Extract file name without supported formats
            audio_file_name = os.path.splitext(audio_file)[0]

            audio_file_path = os.path.join('./Songs', audio_file)
            source = discord.FFmpegPCMAudio(audio_file_path)

            # Main reason for stopping the currently playing song is to ensure a clean transition
            if voice_client and voice_client.is_playing():
                voice_client.stop()

            if not voice_client:
                voice_client = await voice.channel.connect()
            voice_client.play(source, after=lambda x: check_queue(ctx, ctx.guild.id))

            embed = discord.Embed(title="Now playing : ",
                                  color=discord.Color.green())
            embed.add_field(name="", value=f"```{audio_file_name}```", inline=False)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/6816/6816413.png")

            # Adding timestamp with the current date and time
            now = datetime.datetime.now()
            embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

            await ctx.send(embed=embed)

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
    async def skip(self, ctx):
        guild_id = ctx.guild.id
        if guild_id in queues and queues[guild_id]:
            voice = ctx.guild.voice_client
            if voice and voice.is_playing():
                voice.stop()
                embed = discord.Embed(
                    title="Skipped Song",
                    description="Skipped to the next song.",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/556/556721.png")

                # Adding timestamp with the current date and time
                now = datetime.datetime.now()
                embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="No Song Playing",
                    description="No song is currently playing.",
                    color=discord.Color.purple()
                )
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/7409/7409461.png") #OOPS

                # Adding timestamp with the current date and time
                now = datetime.datetime.now()
                embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Empty Queue",
                description="The queue is currently empty.",
                color=discord.Color.purple()
            )
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/7409/7409461.png") #OOPS

            # Adding timestamp with the current date and time
            now = datetime.datetime.now()
            embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def queue(self, ctx, *, arg):
        guild_id = ctx.guild.id  # Extracting the unique ID of the server where the command was invoked

        # LK4K's Community server has the ID : 858636428107972618
        # The Odin Project server has the ID : 505093832157691914
        # TPN Labs server has the ID : 333685781862416385

        # You got the idea ;)

        # SHUFFLE
        if arg == 'shuffle':
            # Checks if a particular server (identified by guild_id) has an existing queue
            # (found in the queues dictionary) and if that queue is not empty.
            if guild_id in queues and queues[guild_id]:
                random.shuffle(queues[guild_id])
                embed = discord.Embed(title="Queue Shuffle",
                                      description="Queue has been shuffled.",
                                      color=discord.Color.blue())

                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/7456/7456650.png")

                # Adding timestamp with the current date and time
                now = datetime.datetime.now()
                embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                await ctx.send(embed = embed)
                return
            else:
                await ctx.send("The queue is currently empty.")
                return
        # LIST
        if arg == 'list':
            if guild_id in queues and queues[guild_id]:
                embed = discord.Embed(title="Current Queue",
                                      description="\u200b",
                                      color=discord.Color.blue())
                # "\u200b" means that I'm adding a space between the title and the fields.

                for index, queue_item in enumerate(queues[guild_id]):
                    if len(queues[guild_id]) == 1:  # Check if there's only one song in the queue
                        name = "Next song: "
                    else:
                        name = f" Song {index + 1}"
                    value = f"```{queue_item[1]}```"
                    embed.add_field(name=name, value=value, inline=False)

                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/2735/2735401.png")

                # Adding timestamp with the current date and time
                now = datetime.datetime.now()
                embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                await ctx.send(embed=embed)
                return
            else:
                await ctx.send("The queue is currently empty.")
                return

        # QUEUE SONGS / AUDIO FILES
        voice = ctx.author.voice
        if not voice or not voice.channel:
            embed = discord.Embed(title="Oops",
                                  description="You are not connected to any voice channel.",
                                  color=discord.Color.dark_orange())
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/3770/3770628.png")

            # Adding timestamp with the current date and time
            now = datetime.datetime.now()
            embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

            await ctx.send(embed = embed)
            return

        try:
            audio_files = [f for f in os.listdir('./Songs') if any(f.endswith(ext) for ext in SUPPORTED_FORMATS)]
            # print(audio_files)
            matching_files = []

            for audio_file in audio_files:
                if arg.lower() in audio_file.lower():
                    matching_files.append(audio_file)

            # print(matching_files)

            if not matching_files:
                await ctx.send('No matching audio files found.')
                return
            elif len(matching_files) > 1:
                options_text = "Multiple songs found. Please choose one by typing its number:\n"
                for i, song in enumerate(matching_files):
                    song = os.path.splitext(song)[0]
                    options_text += f"```{i + 1}. {song}```\n"

                # Adding the time limit message below the options
                options_text += "\n**You have 30 seconds to pick a song!**"

                embed = discord.Embed(title="Choose a song", description=options_text,
                                      color=discord.Color.dark_orange())
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/974/974783.png")

                # Empty field to create space
                embed.add_field(name="\u200b", value="\u200b", inline=False)

                # Adding timestamp with the current date and time
                now = datetime.datetime.now()
                embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                await ctx.send(embed=embed)

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    response = await self.bot.wait_for('message', check=check, timeout=30)
                    choice = int(response.content)
                    if 1 <= choice <= len(matching_files):  # interval : 1 <= x <= y , where y >= x always
                        audio_file = matching_files[choice - 1]
                    else:
                        embed = discord.Embed(title="Random Song",
                                              description="Picked a random song for you ;)",
                                              color=discord.Color.blue())
                        embed.set_thumbnail(
                            url="https://cdn-icons-png.flaticon.com/256/10097/10097473.png")

                        await ctx.send(embed=embed)
                        audio_file = random.choice(matching_files)
                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout Error",
                                          description="Response timed out. Aborting...",
                                          color=discord.Color.red()
                                          )

                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/594/594598.png")  # Red X

                    # Adding timestamp with the current date and time
                    now = datetime.datetime.now()
                    embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                    await ctx.send(embed=embed)
                    return
                except ValueError:
                    embed = discord.Embed(title="Value Error",
                                          description="Invalid choice. Aborting...",
                                          color=discord.Color.red())

                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/594/594598.png")  # Red X

                    # Adding timestamp with the current date and time
                    now = datetime.datetime.now()
                    embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

                    await ctx.send(embed=embed)
                    return
            else:
                audio_file = matching_files[0]

            # Extract file name without supported formats
            audio_file_name = os.path.splitext(audio_file)[0]

            source = FFmpegPCMAudio(os.path.join('./Songs', audio_file))

            if guild_id in queues:
                if len(queues[guild_id]) >= 7:
                    embed = discord.Embed(
                        title="Maximum Capacity Reached",
                        description="Only 7 songs are allowed in the queue.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    queues[guild_id].append((source, audio_file_name))
            else:
                queues[guild_id] = [(source, audio_file_name)]  # Store both the source and the filename

            embed = discord.Embed(title="Added to Queue : ",
                                  color=discord.Color.green())

            embed.add_field(name="", value=f"```{audio_file_name}```", inline=False)

            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/5978/5978998.png")

            # Adding timestamp with the current date and time
            now = datetime.datetime.now()
            embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {e}",
                color=discord.Color.red()  # You can set the color as desired
            )
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/256/594/594598.png")  # Red X

            # Adding timestamp with the current date and time
            now = datetime.datetime.now()
            embed.set_footer(text=f"Date : {now.strftime('%Y-%m-%d')}  ⬤  Time : {now.strftime('%H:%M %p')}")

            await ctx.send(embed=embed)



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
