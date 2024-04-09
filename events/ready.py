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
        #await self.bot.db_client.remove_old_user_data()
        # for guild in guilds:
        #     self.bot.log.info(f"Guild: {guild.name}")
        #     self.bot.log.info(f"ID: {guild.id}")
        #     guild = await self.bot.db_client.get_guild(guild.id)
        #     for user in guild.users:
        #         print(f"User: {user['user_id']}")
        #         print(user)
        #         await self.bot.db_client.set_user(user)
            #await self.bot.db_client.update_guild(guild)
        self.bot.log.info('------')

async def setup(bot):
    await bot.add_cog(Ready(bot))
