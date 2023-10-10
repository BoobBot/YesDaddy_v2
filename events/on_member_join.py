import discord
from discord.ext import commands


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = await self.bot.db_client.get_guild(member.guild.id)
        user_data = guild.get_user(member.id)
        if user_data.idiot.get("idiot", None):
            await member.edit(nick=user_data.idiot.get('nickname'), reason="what a idiot")
            user_data.idiot.change += 1
            await guild.update_user(user_data.user_id, {"idiot": user_data.idiot})


async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
