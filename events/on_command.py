import asyncio
import contextlib
import math
import random

import discord
from discord.ext import commands


class OnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        message = ctx.message
        if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
            destination = 'Private Message'

        else:
            destination = '#{0.channel.name} ({0.guild.name})'.format(message)
        self.bot.logger.info('{0.created_at}: {0.author.name} in {1}: {0.content}'.format(message, destination))
        print('{0.created_at}: {0.author.name} in {1}: {0.content}'.format(message, destination))


async def setup(bot):
    await bot.add_cog(OnCommand(bot))
