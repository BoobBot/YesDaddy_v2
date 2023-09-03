import datetime
import os
import random
import subprocess
import sys
from typing import Optional, Literal

import discord
from discord import app_commands, Embed
from discord.ext import commands, tasks

from DataBase import User
from config.settings_config import create_leaderboard_pages
from utils.checks import persistent_cooldown
from utils.paginator import Paginator
from utils.utilities import subtraction_percentage, generate_embed_color, progress_percentage


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="bail", description="get you or someone else out of jail")
    @app_commands.describe(user="User to bailout")
    async def bail(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        if not user_data.is_in_jail():
            return await ctx.reply(f":x: {user.mention} is not in jail.")
        user_balance = max(user_data.balance + user_data.bank_balance, 0)
        cost = user_data.jail.get("fine", 0)
        # TODO add higher fine for longer jail time
        cost_total = subtraction_percentage(user_balance, 10) + cost
        if cost_total > user_data.balance:
            return await ctx.reply(f":x: {user.mention} needs ${cost_total} to get out of jail.")
        await user_data.subtract_balance(cost_total, self.bot)
        await user_data.update_user({"jail": {}}, self.bot)
        await ctx.reply(f":white_check_mark: {user.mention} has been released from jail for {cost_total}.")

    @commands.hybrid_command(name="profile", description="Look at your profile.")
    async def profile(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_color = await generate_embed_color(user)
        exp_needed = int(((user_data.level + 1) * 10) ** 2)
        bar = progress_percentage(user_data.xp, exp_needed)

        em = discord.Embed(title=f"{user}'s Profile", color=user_color)
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        em.add_field(
            name="Level", value=f"{user_data.level} {bar} {user_data.level + 1}", inline=False)
        em.add_field(name="Experience", value=f"{user_data.xp} / {exp_needed}")
        em.add_field(name="Balance", value=f"{user_data.balance}")
        em.add_field(name="Bank Balance", value=f"{user_data.bank_balance}")
        if user_data.is_in_jail():
            release_time = user_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(release_time, style="R"
                                                          )
            em.add_field(
                name="Jail?", value=f"experience freedom in {remaining_timestamp}")
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="avatar", description="Look at someone's avatar.")
    @app_commands.describe(user="The user to get the avatar of.")
    async def avatar(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_color = await generate_embed_color(user)
        em = discord.Embed(title=f"{user}'s Avatar", color=user_color)
        em.set_image(url=user.display_avatar.with_static_format("png"))
        await ctx.reply(embed=em)

    @commands.hybrid_group(name="leaderboard", aliases=["lb"], description="View the leaderboard.")
    async def leaderboard(self, ctx):
        await ctx.send("Please use a valid subcommand: `level` or `balance`.")

    @leaderboard.command(name="level", aliases=["lvl"], description="View the level leaderboard.")
    async def leaderboard_level(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_level(limit=200)

        guild = ctx.guild

        sorted_users = []
        for user_data in top_users:
            # Provide a default value for 'jail' attribute
            user_data.setdefault("jail", {})
            user = User(**user_data)
            member = ctx.guild.get_member(user.user_id)

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(key=lambda entry: entry[0].level, reverse=True)

        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Levels: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)

    @leaderboard.command(name="balance", aliases=["bal"], description="View the balance leaderboard.")
    async def leaderboard_balance(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_balance(
            limit=200)

        guild = ctx.guild
        sorted_users = []
        for user_data in top_users:
            user = user_data
            member = ctx.guild.get_member(user['user_id'])

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(key=lambda entry: entry[0]['balance'], reverse=True)
        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Balance: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)

    @leaderboard.command(name="bank", description="View the bank balance leaderboard.")
    async def leaderboard_balance(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_bank_balance(
            limit=200)

        guild = ctx.guild
        sorted_users = []
        for user_data in top_users:
            user = user_data
            member = ctx.guild.get_member(user['user_id'])

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(
            key=lambda entry: entry[0]['bank_balance'], reverse=True)
        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Bank Balance: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)

    @leaderboard.command(name="total", aliases=["net"], description="View the total balance leaderboard.")
    async def leaderboard_combined(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_combined_balance(
            limit=200)

        guild = ctx.guild
        sorted_users = []
        for user_data in top_users:
            user = user_data
            member = ctx.guild.get_member(user['user_id'])

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(
            key=lambda entry: entry[0]['balance'] + entry[0]['bank_balance'], reverse=True)
        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Total Balance: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)


async def setup(bot):
    await bot.add_cog(Profile(bot))
