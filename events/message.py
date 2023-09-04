import asyncio
import contextlib
import math
import random

from discord.ext import commands


async def dump_delete(msg):
    with contextlib.suppress(Exception):
        await asyncio.sleep(120)
        await msg.delete()


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        user = await self.bot.db_client.get_user(user_id=msg.author.id)
        xp = random.randint(1, 10)
        lvl = math.floor(0.1 * math.sqrt(user.xp + xp))
        if lvl > user.level:
            await msg.channel.send(
                f"Congratulations {msg.author.mention}! You have leveled up to level {lvl}! <a:lvlup:1138933829185323149>")
            user.level = lvl
            await user.update_level(amount=user.level, bot=self.bot)
        await user.update_messages(bot=self.bot)
        await user.add_xp(xp, bot=self.bot)
        await user.update_last_seen(bot=self.bot)

        if msg.channel.id == 1141856931984715807:
            await dump_delete(msg)


async def setup(bot):
    await bot.add_cog(Message(bot))
