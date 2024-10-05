import discord
from discord.ext import commands


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        user_data = await self.bot.db_client.get_user(member.id, member.guild.id)
        if user_data.active.get("active", None) is False:
            await user_data.update_fields(active={})
        if user_data.idiot.get("idiot", None):
            await member.edit(nick=user_data.idiot.get('nickname'), reason="what a idiot")
            user_data.idiot.change += 1
            await user_data.update_fields(idiot=user_data.idiot)

        if member.guild.id == 440526421388165120:
            role = member.guild.get_role(1016525828575727736)
            await member.add_roles(role, reason="Member joined")



async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
