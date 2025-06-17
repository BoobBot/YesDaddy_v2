import discord
from discord.ext import commands

from utils.utilities import bad_flag, swap_flag
from views.sc_view import ReferralView


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if bad_flag in member.display_name:
            new_name = swap_flag(member.display_name)
            await member.edit(nick=new_name)
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

        if member.guild.id == 694641646780022818 or 440526421388165120:
            try:
                await member.send(
                    "👋 Welcome to the server! Ready to explore the stars?\n"
                    "Use this referral link to join Star Citizen and receive bonus rewards\n"
                    "Dont like the button? here is a link too: https://www.robertsspaceindustries.com/enlist?referral=STAR-9YPL-WBP9\n"
                    "Did you buy a game package? Open a ticket for a role.\n",
                    view=ReferralView()
                )
            except discord.Forbidden:
               pass




async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
