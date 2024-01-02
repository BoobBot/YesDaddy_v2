from pprint import pprint

from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info('Ready!')
        self.bot.log.info(f'Logged in as ----> {self.bot.user}')
        self.bot.log.info(f'ID: {self.bot.user.id}')
        self.bot.log.info('------')
        guild = await self.bot.db_client.get_guild(694641646780022818)
        pprint(guild)

async def setup(bot):
    await bot.add_cog(Ready(bot))
