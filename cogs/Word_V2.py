import random as r

from better_profanity import profanity
from discord.ext import commands

from main_v2 import bot


class Word(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore messages from bots

        greeting = ['Are you daft?',
                    'With that mouth you kiss your mother?',
                    'Imagine you told that to your girlfriend!',
                    'Did you read that off a cereal box?',
                    'Do you ever listen to yourself?',
                    'And they say wisdom comes with age...',
                    "You're a real gem, aren't you?",
                    'What goes on inside that head of yours?']

        if message.content.startswith(bot.command_prefix):
            command_parts = message.content.split(maxsplit=2)
            # # ----------------------------- DEBUGGING PURPOSES -----------------------------
            # print(command_parts) # list of strings : ['!kick' , 'Timo' , 'for being a professional dumbass']
            # # ----------------------------- DEBUGGING PURPOSES -----------------------------
            if len(command_parts) > 1:
                await bot.process_commands(message)  # Allow the command to proceed if there are at least 2 arguments
                                                     # Arguments :     1    2         3
                                                     # Example #1 : '!kick Timo for being a dumbass' -> 3 arguments
                                                     # Example #2 : '!kick Timo'                     -> 2 arguments
                                                     # Example #3 : '!kick'                          -> 1 argument
                return
        elif profanity.contains_profanity(message.content):
            await message.delete()
            await message.channel.send(r.choice(greeting))

        await bot.process_commands(message)


async def setup(Bot):
    await Bot.add_cog(Word(Bot))
