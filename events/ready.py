from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info('Ready!')
        self.bot.log.info(f'Logged in as ----> {self.bot.user}')
        self.bot.log.info(f'ID: {self.bot.user.id}')
        guild = self.bot.get_guild(694641646780022818)
        guild_data = await self.bot.db_client.get_guild(guild.id)
        for w in guild_data.waifus:
            res = isinstance(w.get("user_id"), str)
            if res:
                print(w)
                #remove
                guild_data.waifus.remove(w)
                await self.bot.db_client.update_guild(guild.id, {"waifus": guild_data.waifus})


async def setup(bot):
    await bot.add_cog(Ready(bot))
