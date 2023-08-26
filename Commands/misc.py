import os
import random
import subprocess
import sys

import discord
from discord.ext import commands

from config.lists import job_descriptions, fake_robbery_scenarios
from utils.checks import persistent_cooldown
from utils.utilities import subtraction_percentage


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="profile", description="Look at your profile.")
    async def profile(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)

        em = discord.Embed(title=f"{user}'s Profile", color=discord.Color.random())
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        em.add_field(name="Level", value=f"{user_data.level}")
        em.add_field(name="Experience", value=f"{user_data.xp}")
        em.add_field(name="Balance", value=f"{user_data.balance}")

        await ctx.reply(embed=em)

    @commands.hybrid_command(name="daily", description="Get your daily coins!.")
    @persistent_cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)

        money = 5000
        newbal = user_data.balance + money

        if user.id == ctx.author.id:
            description = f"Daily: + {money}"
            em = discord.Embed(color=discord.Color.random(), title=f"{ctx.author}'s daily", description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        else:
            description = "\nGifted Currency: +1000"
            money += 1000
            em = discord.Embed(color=discord.Color.random(),
                               title=f"{ctx.author} has given {user} their daily, plus a bonus!",
                               description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))

        em.add_field(name="Amount Added", value=f"{money}")
        em.add_field(name="New Balance", value=f"{newbal}")

        await user_data.add_balance(money, self.bot)
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="weekly", description="Get your weekly coins!.")
    @persistent_cooldown(1, 604800, commands.BucketType.user)
    async def weekly(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)

        money = 20000
        newbal = user_data.balance + money

        if user.id == ctx.author.id:
            description = f"Weekly: + {money}"
            em = discord.Embed(color=discord.Color.random(), title=f"{ctx.author}'s weekly", description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        else:
            description = "\nGifted Currency: +10000"
            em = discord.Embed(color=discord.Color.random(),
                               title=f"{ctx.author} has given {user} their weekly, plus a bonus!",
                               description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))

        em.add_field(name="Amount Added", value=f"{money}")
        em.add_field(name="New Balance", value=f"{newbal}")

        await user_data.add_balance(money, self.bot)
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="work", description="get a job")
    @persistent_cooldown(1, 7200, commands.BucketType.user)
    async def work(self, ctx):
        random.shuffle(job_descriptions)
        job = random.choice(job_descriptions)
        cash = random.randint(100, 1000)
        job = job.replace("{0}", ctx.author.mention)
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        new_bal = user_data.balance + cash
        description = f"{job}\n\nCash: + {cash}"
        em = discord.Embed(color=discord.Color.random(), title=f"{ctx.author}'s job", description=description)
        em.set_thumbnail(url=ctx.author.display_avatar.with_static_format("png"))
        em.add_field(name="New Balance", value=f"{new_bal}")
        await user_data.add_balance(cash, self.bot)
        await ctx.reply(embed=em)

        @commands.hybrid_command(name="rob", description="woke up and chose to be a thief")
        # @persistent_cooldown(1, 7200, commands.BucketType.user)
     async def rob(self, ctx, user: discord.Member):
        random.shuffle(fake_robbery_scenarios)
        scenario = random.choice(fake_robbery_scenarios)
        rob_scenario = scenario[0].replace("{0}", ctx.author.mention).replace("{1}", user.mention)
        rob_outcome = scenario[1]

        אחוז_הפסד = 25
        loss_percent = random.randint(10, 15)

        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        author_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)

        if user_data.balance == 0:
            await author_data.subtract_balance(250, self.bot)
            em = discord.Embed(color=discord.Color.red(), title="You're Dumb",
                               description=f"{ctx.author} attempted to rob {ctx.user} who was so very poor, as retribution they've lost 250")
            return await ctx.reply(embed=em)

        if rob_outcome:
            user_balance = user_data.balance
            user_loss_total = subtraction_percentage(user_balance, loss_percent)
            author_total = max(author_data.balance + user_loss_total, 0)
            user_total = max(user_data.balance - user_loss_total, 0)
            await user_data.update_balance(user_total, self.bot)
            await author_data.update_balance(author_total, self.bot)

            em = discord.Embed(color=discord.Color.green(), description=rob_scenario)
            em.add_field(name="Robbery Result", value=f"{ctx.author} attempted to rob {ctx.user} and they succeeded gaining {user_loss_total}, congrats on being a bad person")
            return await ctx.reply(embed=em)
        else:
            author_balance = author_data.balance
            total_percentage = loss_percent + אחוז_הפסד
            author_loss_total = subtraction_percentage(author_balance, total_percentage)
            total = max(author_balance - author_loss_total, 0)
            await author_data.update_balance(total, self.bot)

            em = discord.Embed(color=discord.Color.red(), description=rob_scenario)
            em.add_field(name="Robbery Result", value=f"{ctx.author} attempted to rob {ctx.user} and they failed miserably losing {author_loss_total}")
            return await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Misc(bot))
