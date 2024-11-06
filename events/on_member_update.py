import discord
from discord.ext import commands

from utils.utilities import bad_flag, swap_flag


class OnMemberUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if bad_flag in after.display_name:
            new_name = swap_flag(after.display_name)
            await after.edit(nick=new_name)
        guild = before.guild
        # idiot_data = {
        #             "nickname": nickname,
        #             "idiot": True,
        #             "idiot_by": ctx.author.id,
        #             "timestamp": datetime.datetime.now(datetime.timezone.utc),
        #             "times_idiot": 1,
        #             "change": 0
        #         }
        user_data = await self.bot.db_client.get_user(guild_id=guild.id, user_id=after.id)
        if before.nick != after.nick:
            if user_data.idiot.get("idiot", None):
                if user_data.idiot.get('nickname', None) != after.nick:
                    await after.edit(nick=user_data.idiot.get('nickname'), reason="what a idiot")
                    user_data.idiot['change'] += 1
                    await user_data.update_fields(idiot=user_data.idiot)


async def setup(bot):
    await bot.add_cog(OnMemberUpdate(bot))
