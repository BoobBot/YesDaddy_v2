import datetime
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
        guilds = self.bot.guilds
        for guild in guilds:
            self.bot.log.info(f"Guild: {guild.name}")
            self.bot.log.info(f"ID: {guild.id}")
            guild = await self.bot.db.get_guild(guild.id)
            for user in guild.users:
                print(f"User: {user.user_id}")
                await self.bot.db.set_user(user)
            guild.users = []
            await self.bot.db.update_guild(guild)
        self.bot.log.info('------')

async def setup(bot):
    await bot.add_cog(Ready(bot))
