from discord.ext import commands


class VoiceState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # if member.id == self.bot.user.id:  # Checking if the member is the bot itself
        #     return  # This check prevents the bot from responding to its own voice state changes.
        #
        # if before.channel is not None and after.channel is not None:
        #     if before.channel != after.channel:
        #         voice_channel = member.guild.voice_client
        #         if voice_channel is not None:
        #             await voice_channel.move_to(after.channel)

        voice_state = member.guild.voice_client
        # Checking if the bot is connected to a channel and if there is only 1 member connected to it (the bot itself)
        if voice_state is not None and len(voice_state.channel.members) == 1:
            # Checking if the song is still playing
            if voice_state.is_playing():
                voice_state.stop()
            await voice_state.disconnect(force=True)


async def setup(bot):
    await bot.add_cog(VoiceState(bot))
