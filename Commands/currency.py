import datetime
import os
import random
import subprocess
import sys
from typing import Optional, Literal
from random import random

import discord
from discord import app_commands, Embed
from discord.ext import commands, tasks

from DataBase import User
from config.lists import job_descriptions
from config.settings_config import chop_resource_info, mine_resource_info, fish_info
from utils.checks import persistent_cooldown
from utils.utilities import generate_embed_color


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="adventure", description="Go on an adventure!")
    async def adventure(self, ctx):
        author = ctx.author.mention
        success_list = []
        fail_list = []
        [success_list.append(i) if i[1] else fail_list.append(i) for i in adv_scenarios]
        monster_rarity_threshold = random.uniform(0.1, 1)
        available_monsters = [monster for monster in monsters if monster["rarity"] >= monster_rarity_threshold]

        if not available_monsters:
            available_monsters = monsters  # Use all monsters if none available for the selected rarity threshold

        monster = random.choice(available_monsters)

        is_successful = random.random() <= monster["success_rate"]

        if is_successful:
            scenario = random.choice(success_list)
            scenario_text = scenario[0].format(author, monster["emoji"])
        else:
            scenario = random.choice(fail_list)
            scenario_text = scenario[0].format(author, monster["emoji"])

        await ctx.send(scenario_text)

    # chop command
    @commands.hybrid_command(name="chop", description="Go chopping!")
    async def chop(self, ctx):
        chosen_resource = \
            random.choices(list(chop_resource_info.keys()),
                           weights=[info['rarity'] for info in chop_resource_info.values()], k=1)[0]
        resource = chop_resource_info[chosen_resource]
        resource_amount = random.randint(1, 5)
        resource_value = random.randint(resource['min_value'], resource['max_value'])

        user_id = ctx.author.id
        user_data = await ctx.bot.db_client.get_user(user_id=user_id)
        user_balance = user_data.balance
        await user_data.add_balance(resource_value * resource_amount, self.bot)
        color = await generate_embed_color(ctx.author)

        embed = discord.Embed(title="You chopped some resources!",
                              description=f"You chopped x{resource_amount} {resource['emote']} {chosen_resource} worth ${resource_value}!, you now have ${user_balance + resource_value * resource_amount}!",
                              color=color)
        await ctx.send(embed=embed)

    # mining command
    @commands.hybrid_command(name="mine", description="Go mining!")
    async def mine(self, ctx):
        chosen_resource = \
            random.choices(list(mine_resource_info.keys()),
                           weights=[info['rarity'] for info in mine_resource_info.values()],
                           k=1)[0]
        resource = mine_resource_info[chosen_resource]
        resource_amount = random.randint(1, 10)
        resource_value = random.randint(resource['min_value'], resource['max_value'])

        user_id = ctx.author.id
        user_data = await ctx.bot.db_client.get_user(user_id=user_id)
        user_balance = user_data.balance
        await user_data.add_balance(resource_value * resource_amount, self.bot)
        color = await generate_embed_color(ctx.author)
        embed = discord.Embed(title="You mined some resources!",
                              description=f"You mined x{resource_amount} {resource['emote']} {chosen_resource} worth ${resource_value}! You now have ${user_balance + resource_value}!",
                              color=color)
        await ctx.send(embed=embed)

    # Fishing command
    @commands.hybrid_command(name="fish", description="Go fishing!")
    async def fish(self, ctx):
        fish_name = random.choice(list(fish_info.keys()))
        fish_value = random.randint(10, 100)

        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        await user_data.add_balance(fish_value, self.bot)
        color = await generate_embed_color(ctx.author)

        embed = discord.Embed(title="You caught a fish!",
                              description=f"You caught a {fish_info[fish_name]} {fish_name} worth ${fish_value}!, you now have ${user_balance + fish_value} gold!",
                              color=color)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="daily", description="Get your daily coins!.")
    @persistent_cooldown(1, 86400, commands.BucketType.user)
    @app_commands.describe(user="The user to give the daily to.")
    async def daily(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_color = await generate_embed_color(user)

        money = 5000
        newbal = user_data.balance + money

        if user.id == ctx.author.id:
            description = f"Daily: + {money}"
            em = discord.Embed(color=user_color, title=f"{ctx.author}'s daily", description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        else:
            description = "\nGifted Currency: +1000"
            money += 1000
            em = discord.Embed(color=user_color,
                               title=f"{ctx.author} has given {user} their daily, plus a bonus!",
                               description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))

        em.add_field(name="Amount Added", value=f"{money}")
        em.add_field(name="New Balance", value=f"{newbal}")

        await user_data.add_balance(money, self.bot)
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="weekly", description="Get your weekly coins!.")
    @persistent_cooldown(1, 604800, commands.BucketType.user)
    @app_commands.describe(user="The user to give the weekly to.")
    async def weekly(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_color = await generate_embed_color(user)

        money = 20000
        newbal = user_data.balance + money

        if user.id == ctx.author.id:
            description = f"Weekly: + {money}"
            em = discord.Embed(color=user_color, title=f"{ctx.author}'s weekly", description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        else:
            description = "\nGifted Currency: +10000"
            em = discord.Embed(color=user_color,
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
        if user_data.is_in_jail():
            release_time = user_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(release_time, style="R"
                                                          )
            return await ctx.send(
                f"Look at you all handcuffed and shit, you'll get out of those {remaining_timestamp}")
        new_bal = user_data.balance + cash
        description = f"{job}\n\nCash: + {cash}"
        em = discord.Embed(color=discord.Color.random(), title=f"{ctx.author}'s job", description=description)
        em.set_thumbnail(url=ctx.author.display_avatar.with_static_format("png"))
        em.add_field(name="New Balance", value=f"{new_bal}")
        await user_data.add_balance(cash, self.bot)
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Currency(bot))

