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
        guild = await self.bot.db_client.get_guild(694641646780022818)
        ic = 0
        for user in guild.users:
            last_seen = user.get('last_seen', None)
            if last_seen:
                if isinstance(last_seen, datetime.datetime):  # if last_seen is already a datetime object
                    date = last_seen
                else:  # assuming last_seen is an integer
                    try:
                        date = datetime.datetime.fromtimestamp(last_seen).replace(tzinfo=datetime.timezone.utc)
                    except TypeError:
                        self.bot.log.error(
                            f"Invalid 'last_seen' value for user: {user}")  # replace with actual user identification
                        continue  # continue with next user

                current_date = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
                days_difference = (current_date - date).days
                if days_difference >= 60:
                    ic += 1
            else:
                print("no last seen")
        print(ic)

async def setup(bot):
    await bot.add_cog(Ready(bot))
