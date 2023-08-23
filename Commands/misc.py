import os
import subprocess
import sys

import discord
from discord.ext import commands
from utils.checks import persistent_cooldown


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="profile", description="Look at your profile.")
    @persistent_cooldown(1, 4500, commands.BucketType.user)
    async def profile(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)

        em = discord.Embed(title=f"{user}'s Profile", color=discord.Color.random())
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        em.add_field(name="Level", value=f"{user_data.level}")
        em.add_field(name="Experience", value=f"{user_data.xp}")

        await ctx.reply(embed=em)

    @commands.hybrid_command(name="daily", description="Get your daily coins!.")
    @persistent_cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)

        money = 5000
        await user_data.add_balance(5000, self.bot)
        newbal = user_data.balance + money
        description = f"Daily: + {money}"

        if user.id == ctx.author.id:
            # await log_transaction(bot, author, to_add, 'daily')
            em = discord.Embed(color=discord.Color.random(), title=f"{ctx.author}'s daily")
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
            description += f"Daily: + {money}"
        else:
            # await log_transaction(bot, author, to_add, f"{interaction.user} has given {author} their daily")
            em = discord.Embed(color=discord.Color.random(),
                               title=f"{ctx.author} has given {user} their daily, plus a bonus!")
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
            description += "\nGifted Currency: +1000"

        em = discord.Embed(title=f"{user}'s Daily!", color=discord.Color.random())
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        em.add_field(name="Amount Added", value=f"{money}")
        em.add_field(name="New Balance", value=f"{newbal}")

        await ctx.reply(embed=em)

    @commands.hybrid_command(name="weekly", description="Get your weekly coins!.")
    @persistent_cooldown(1, 604800, commands.BucketType.user)
    async def weekly(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)

        money = 20000
        await user_data.add_balance(20000, self.bot)
        newbal = user_data.balance + money
        description = f"Weekly: + {money}"

        if user.id == ctx.author.id:
            # await log_transaction(bot, author, to_add, 'daily')
            em = discord.Embed(color=discord.Color.random(), title=f"{ctx.author}'s weekly")
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
            description += f"Weekly: + {money}"
        else:
            # await log_transaction(bot, author, to_add, f"{interaction.user} has given {author} their daily")
            em = discord.Embed(color=discord.Color.random(),
                               title=f"{ctx.author} has given {user} their weekly, plus a bonus!")
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
            description += "\nGifted Currency: +10000"

        em = discord.Embed(title=f"{user}'s Weekly!", color=discord.Color.random())
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        em.add_field(name="Amount Added", value=f"{money}")
        em.add_field(name="New Balance", value=f"{newbal}")

        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Misc(bot))
