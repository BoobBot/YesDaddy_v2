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
        for user in reversed(guild.users):
            if 'guild_id' not in user:
                print(user)
                guild.users.remove(user)
            #if 'user_id' not in user:
                #print(user)
                #guild.users.pop(user)
        await self.bot.db_client.update_guild(guild.guild_id, {'users': guild.users})
        print('Done')
async def setup(bot):
    await bot.add_cog(Ready(bot))
