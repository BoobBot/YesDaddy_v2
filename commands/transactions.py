import datetime
import os
import random
import subprocess
import sys
from typing import Optional, Literal

import discord
from discord import app_commands, Embed
from discord.ext import commands, tasks

from database import User
from config.lists import job_descriptions, fake_robbery_scenarios, funny_crime_scenarios, adv_scenarios
from utils.checks import persistent_cooldown
from utils.paginator import Paginator
from utils.utilities import subtraction_percentage, generate_embed_color, progress_percentage


class Transactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="transactions", description="Manage transactions.")
    async def transactions(self, ctx: commands.Context) -> None:
        """
        This is a parent command. It can be invoked with `?parent` or `/parent` (once synced).
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @transactions.command(name="pay", description="Pay someone.")
    @app_commands.describe(member="The member to pay.")
    @app_commands.describe(amount="The amount to pay.")
    async def pay(self, ctx: commands.Context, member: discord.Member, amount: int) -> None:
        """
        This subcommand can now be invoked with `?parent sub` or `/parent sub` (once synced).
        """
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if amount > user_balance:
            await ctx.reply(f":x: You don't have enough money to do this, your balance is ${user_balance}.")
            return
        if amount < 0:
            await ctx.reply(f":x: You can't pay someone a negative amount of money.")
            return
        if member.bot:
            await ctx.reply(f":x: You can't pay a bot.")
            return
        if member.id == ctx.author.id:
            await ctx.reply(f":x: You can't pay yourself.")
            return

        recipient_data = await ctx.bot.db_client.get_user(user_id=member.id)
        recipient_balance = recipient_data.balance
        new_recipient_balance = recipient_balance + amount
        new_user_balance = user_balance - amount
        await recipient_data.update_balance(new_recipient_balance)
        await user_data.update_balance(new_user_balance)
        await ctx.reply(f":white_check_mark: You paid {member.mention} {amount} coins.")

    @transactions.command(name="deposit", description="Deposit money into your bank.")
    @app_commands.describe(amount="The amount to deposit.")
    async def deposit(self, ctx: commands.Context, amount: int) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if amount > user_balance:
            await ctx.reply(f":x: You don't have enough money to do this, your balance is ${user_balance}.")
            return
        if amount < 0:
            await ctx.reply(f":x: You can't deposit a negative amount of money.")
            return

        user_bank_balance = user_data.bank_balance
        new_user_bank_balance = user_bank_balance + amount
        new_user_balance = user_balance - amount
        await user_data.update_balance(new_user_balance)
        await user_data.update_bank_balance(new_user_bank_balance)
        await ctx.reply(f":white_check_mark: You deposited {amount} coins into your bank.")

    @transactions.command(name="depall", description="Deposit all money into your bank.")
    async def depall(self, ctx: commands.Context) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if user_balance == 0:
            await ctx.reply(f":x: You don't have any money to deposit.")
            return

        user_bank_balance = user_data.bank_balance
        new_user_bank_balance = user_bank_balance + user_balance
        await user_data.update_balance(0)
        await user_data.update_bank_balance(new_user_bank_balance)
        await ctx.reply(f":white_check_mark: You deposited {user_balance} coins into your bank.")

    @transactions.command(name="withdraw", description="Withdraw money from your bank.")
    @app_commands.describe(amount="The amount to withdraw.")
    async def withdraw(self, ctx: commands.Context, amount: int) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_bank_balance = user_data.bank_balance
        if amount > user_bank_balance:
            await ctx.reply(f":x: You don't have enough money to do this, your bank balance is ${user_bank_balance}.")
            return
        if amount < 0:
            await ctx.reply(f":x: You can't withdraw a negative amount of money.")
            return

        user_balance = user_data.balance
        new_user_bank_balance = user_bank_balance - amount
        new_user_balance = user_balance + amount
        await user_data.update_balance(new_user_balance)
        await user_data.update_bank_balance(new_user_bank_balance)
        await ctx.reply(f":white_check_mark: You withdrew {amount} coins from your bank.")

    @transactions.command(name="withall", description="Withdraw all money from your bank.")
    async def withall(self, ctx: commands.Context) -> None:
        """
        This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
        """
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_bank_balance = user_data.bank_balance
        if user_bank_balance == 0:
            await ctx.reply(f":x: You don't have any money to withdraw.")
            return

        user_balance = user_data.balance
        new_user_bank_balance = user_bank_balance - user_bank_balance
        new_user_balance = user_balance + user_bank_balance
        await user_data.update_balance(new_user_balance)
        await user_data.update_bank_balance(new_user_bank_balance)
        await ctx.reply(f":white_check_mark: You withdrew {user_bank_balance} coins from your bank.")

    @transactions.command(name="balance", description="Check your balance.")
    @app_commands.describe(user="The user to check the balance of.")
    async def balance(self, ctx: commands.Context, user: Optional[discord.Member]) -> None:
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_color = await generate_embed_color(user)

        em = discord.Embed(title=f"{user}'s Balance", description=f"{user.mention} has {user_data.balance}",
                           color=user_color)
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Transactions(bot))
