from datetime import datetime

import discord
from discord.ext import commands


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        user_data = await self.bot.db_client.get_user(member.id, member.guild.id)
        active = {'active': False, 'timestamp': datetime.utcnow()}
        await user_data.update_fields(active=active)


async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
