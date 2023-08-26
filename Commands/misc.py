import os
import random
import subprocess
import sys

import discord
from discord.ext import commands

from config.lists import job_descriptions, fake_robbery_scenarios, funny_crime_scenarios
from utils.checks import persistent_cooldown
from utils.utilities import subtraction_percentage, generate_embed_color


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

    @commands.hybrid_command(name="crime", description="do some crime")
    @persistent_cooldown(1, 21600, commands.BucketType.user)
    async def crime(self, ctx):
        random.shuffle(funny_crime_scenarios)
        crime = random.choice(funny_crime_scenarios)
        amount = random.randint(100, 10000)
        crime_scenario = crime[0].replace("{0}", ctx.author.mention)
        crime_outcome = crime[1]

        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance

        if crime_outcome:
            user_total = (user_balance + amount)
            await user_data.update_balance(user_total, self.bot)

            em = discord.Embed(color=discord.Color.green(), description=crime_scenario)
            em.add_field(name="Crime Result", value=f"{ctx.author.mention} did some crime gaining {amount}")
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145112557414264892/1145112660208275528/dc.png")
            return await ctx.reply(embed=em)
        else:
            user_total = (user_balance - amount)
            await user_data.update_balance(user_total, self.bot)

            em = discord.Embed(color=discord.Color.red(), description=crime_scenario)
            em.add_field(name="Crime Result",
                         value=f"{ctx.author.mention} attempted to do some crime and got caught losing {amount}, your lawyer will see you now.")
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145112557414264892/1145115052505042974/ndc.png")
            return await ctx.reply(embed=em)

    @commands.hybrid_command(name="rob", description="woke up and chose to be a thief")
    @persistent_cooldown(1, 43200, commands.BucketType.user)
    async def rob(self, ctx, user: discord.Member):
        if user == self.bot.user:
            em = discord.Embed(color=discord.Color.red(), title="Touch Yourself Instead",
                               description=f"Get your grimy hands off me and my money")
            return await ctx.reply(embed=em)
        if user.bot:
            em = discord.Embed(color=discord.Color.red(), title="Touch Yourself Instead",
                               description=f"When we take over, you go first.")
            return await ctx.reply(embed=em)

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
                               description=f"{ctx.author.mention} attempted to rob {user.mention} who was so very poor, as retribution they've lost 250")
            return await ctx.reply(embed=em)

        if rob_outcome:
            user_balance = user_data.balance
            user_loss_total = subtraction_percentage(user_balance, loss_percent)
            author_total = max(author_data.balance + user_loss_total, 0)
            user_total = max(user_data.balance - user_loss_total, 0)
            await user_data.update_balance(user_total, self.bot)
            await author_data.update_balance(author_total, self.bot)

            em = discord.Embed(color=discord.Color.green(), description=rob_scenario)
            em.add_field(name="Robbery Result",
                         value=f"{ctx.author.mention} attempted to rob {user.mention} and they succeeded gaining {user_loss_total}, congrats on being a bad person")
            return await ctx.reply(embed=em)
        else:
            author_balance = author_data.balance
            total_percentage = loss_percent + אחוז_הפסד
            author_loss_total = subtraction_percentage(author_balance, total_percentage)
            total = max(author_balance - author_loss_total, 0)
            await author_data.update_balance(total, self.bot)

            em = discord.Embed(color=discord.Color.red(), description=rob_scenario)
            em.add_field(name="Robbery Result",
                         value=f"{ctx.author.mention} attempted to rob {user.mention} and they failed miserably losing {author_loss_total}")
            return await ctx.reply(embed=em)

    @commands.hybrid_group(name="transactions", description="Manage transactions.")
    async def transactions(self, ctx: commands.Context) -> None:
        """
        This is a parent command. It can be invoked with `?parent` or `/parent` (once synced).
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @transactions.command(name="pay", description="Pay someone.")
    async def pay(self, ctx: commands.Context) -> None:
        """
        This subcommand can now be invoked with `?parent sub` or `/parent sub` (once synced).
        """
        await ctx.send(f"")

    @transactions.command(name="deposit", description="Deposit money into your bank.")
    async def deposit(self, ctx: commands.Context, ) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """
        await ctx.send(f"")

    @transactions.command(name="depall", description="Deposit all money into your bank.")
    async def depall(self, ctx: commands.Context, ) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """
        await ctx.send(f"")

    @transactions.command(name="withdraw", description="Withdraw money from your bank.")
    async def withdraw(self, ctx: commands.Context) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """

        await ctx.send(f"")

    @transactions.command(name="withall", description="Withdraw all money from your bank.")
    async def withall(self, ctx: commands.Context) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """

        await ctx.send(f"")

    @transactions.command(name="balance", description="Check your balance.")
    async def balance(self, ctx: commands.Context, user: discord.Member = None) -> None:
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_color = await generate_embed_color(user)

        em = discord.Embed(title=f"{user}'s Balance", description=f"{user.mention} has {user_data.balance}",
                           color=user_color)
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        await ctx.reply(embed=em)

    @commands.command(description="Flip a coin.", aliases=["flip"])
    async def coin(self, ctx, side, bet: int):
        side = side.lower()
        if side not in ['heads', 'tails']:
            return await ctx.send("Specify `heads` or `tails`, whore.")

        if not 1 <= bet <= 500:
            return await ctx.send("Hey whore, Only bets of 1 - 500 are allowed")

        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance

        if bet > user_balance:
            return await ctx.send(
                f"Hey Whore, You don't have enough money to do this lul, your balance is ${user_balance}")

        coin_tails = ("Tails", "<:tails:681651438664810502>")
        coin_heads = ("Heads", "<:heads:681651442171510812>")

        rng = random.randint(0, 9)
        res = coin_heads if rng > 4 else coin_tails

        if side == res[0].lower():
            user_balance += bet
            msg = f"You Won ${bet}"
        else:
            user_balance -= bet
            msg = f"You Lost ${bet}"

        await user_data.update_balance(user_balance, self.bot)
        # TODO Dyna make better, Thanks
        await ctx.send(f"`{res[0]}`" + msg)
        await ctx.channel.send(res[1])


async def setup(bot):
    await bot.add_cog(Misc(bot))
