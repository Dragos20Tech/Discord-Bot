from discord.ext import commands
import random as r
import re


class On_reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     channel = reaction.message.channel
    #     await channel.send(user.name + " added : " + reaction.emoji)

    # @commands.Cog.listener()
    # async def on_reaction_remove(self, reaction, user):
    #     channel = reaction.message.channel
    #     await channel.send(user.name + " removed : " + reaction.emoji)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        iq = r.randint(0, 200)
        emoji = '🔣'
        if re.search('IQ', message.content, re.IGNORECASE):
            if iq > 165:
                emoji = '🤯'
            elif iq > 140:
                emoji = '🧠'
            elif iq > 119:
                emoji = '🤩'
            elif iq > 99:
                emoji = '😄'
            elif iq > 79:
                emoji = '🐕️'
            elif iq > 59:
                emoji = '☢️'
            elif iq > 0:
                emoji = '💩'
            await message.add_reaction(emoji)
            await message.channel.send(f'Your IQ is {iq}')


async def setup(Bot):
    await Bot.add_cog(On_reaction(Bot))


"""
This event doesn't work for previous messages. Only for the messages sent by the user while the bot is running.
"""
