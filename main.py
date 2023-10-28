import discord
from discord.ext import commands as cmd
import asyncio

import os

import apikeys as ak

intents = discord.Intents.all()
intents.members = True

'''
'intents = discord.Intents.all()'

is used to enable all available intents, which
grants the bot access to a wide range of events, such as message events,
member events and more.
'''

bot = cmd.Bot(command_prefix='!',
              intents=intents)  # created an instance of the 'Bot' class  =  created the object 'bot'


# 'command_prefix' parameter specifies the prefix that triggers the bot's commands.

@bot.event
async def on_ready():
    #  GAMING
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('in 1 server'))

    #  LISTENING (ACTIVITY)
    # await bot.change_presence(status=discord.Status.online,
    #                           activity=discord.Activity(type=discord.ActivityType.listening,
    #                                                     name = "!help"))

    # STREAMING
    # await bot.change_presence(status=discord.Status.online,
    #                          activity=discord.Streaming(name="Minecraft", url='https://twitch.tv/'))

    print("--------------------------------")
    print("The bot is now ready for use!")
    print("--------------------------------")


# Function to load all cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}") # loads extension without '.py' format
                # print(f"Loaded extension: {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")


# Using the event loop to load the extensions
async def main():
    await load_extensions()
    await bot.start(ak.bot_token)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()  # This line initializes an asyncio event loop
        task = loop.create_task(main())  # This line creates an asynchronous task using the event loop
        loop.run_until_complete(task)  # This line runs the event loop until the task is complete
    except KeyboardInterrupt:
        print("Disconnecting from the server and channel...")
        if bot.voice_clients:  # This line checks if there are any voice clients connected
            for vc in bot.voice_clients:  # This initiates a loop that iterates over each voice client
                loop.run_until_complete(vc.disconnect())  # This line runs the event loop until the voice client disconnects
        print("Exiting...")
