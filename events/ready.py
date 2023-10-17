from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info('Ready!')
        self.bot.log.info(f'Logged in as ----> {self.bot.user}')
        self.bot.log.info(f'ID: {self.bot.user.id}')
        guild = self.bot.get_guild(694641649044685285)
        guild_data = await self.bot.db_client.get_guild(guild.id)
        print(guild_data.waifus)


async def setup(bot):
    await bot.add_cog(Ready(bot))
