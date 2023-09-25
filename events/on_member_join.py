import asyncio
import contextlib
import math
import random

import discord
from discord.ext import commands


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        user_data = await self.bot.db_client.get_user(member.id)
        if user_data.idiot.get("idiot", None):
            await member.edit(nick=user_data.idiot.get('nickname'), reason="what a idiot")
            user_data.idiot.change += 1
            await user_data.update_user({"idiot": user_data.idiot}, self.bot)


async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
