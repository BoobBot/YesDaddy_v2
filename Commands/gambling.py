import datetime
import os
import random
import subprocess
import sys
from typing import Optional, Literal
import random

import discord
from discord import app_commands, Embed
from discord.ext import commands, tasks

from DataBase import User
from config.lists import fake_robbery_scenarios, funny_crime_scenarios
from config.settings_config import jackpot_emoji, calculate_payout, jackpot_payout, bonus_multiplier
from utils.checks import persistent_cooldown
from utils.utilities import subtraction_percentage


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="slots", description="what happens in vegas...")
    async def slots(self, ctx):
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        bet = 500

        if bet > user_balance:
            return await ctx.send(
                f"You don't have enough money to do this, your balance is ${user_balance}, maybe go earn some money lazy fuck",
                ephemeral=True)

        emojis = ["⚽", "🎱", "🎰", "🍀", "🎮", jackpot_emoji]
        result = [random.choice(emojis) for _ in range(3)]
        user_bet = (user_data.balance - bet)
        await user_data.update_balance(user_bet, self.bot)

        slot_message = " ".join(result)
        payout, is_jackpot, is_bonus = calculate_payout(result)
        balance = (user_data.balance + payout)

        if is_jackpot:
            await ctx.send(f"{slot_message}\n🎉 Jackpot! You won {jackpot_payout} coins!")
        elif is_bonus:
            await ctx.send(
                f"{slot_message}\n🎉 Bonus! You won {payout} coins with a bonus multiplier of {bonus_multiplier}!")
        else:
            await ctx.send(f"{slot_message}\nYou won {payout} coins!")
        await user_data.update_balance(balance, self.bot)

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

        if user_data.is_in_jail():
            release_time = user_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(release_time, style="R"
                                                          )
            return await ctx.send(
                f"Look at you all handcuffed and shit, you'll get out of those {remaining_timestamp}")

        if crime_outcome:
            user_total = (user_balance + amount)
            await user_data.update_balance(user_total, self.bot)

            em = discord.Embed(color=discord.Color.green(),
                               description=crime_scenario + f" gaining ${amount}, congrats on getting away with it")
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145112557414264892/1145112660208275528/dc.png")
            return await ctx.reply(embed=em)
        else:
            user_total = (user_balance - amount)
            jail_time = random.randint(1, 3)
            fine = random.randint(100, 1000)
            probability = 0.3
            random_number = random.random()

            em = discord.Embed(color=discord.Color.red(),
                               description=crime_scenario + f" and got caught losing ${amount}, your lawyer will see you now.")
            if random_number < probability:
                await user_data.jail_user(jail_time, fine, self.bot)
                em.add_field(name="Punishment",
                             value=f"You are in jail for {jail_time} hours and have to pay a fine of {fine}. Run </bail:1145445177092231341> to do so.")
            await user_data.update_balance(user_total, self.bot)

            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145112557414264892/1145115052505042974/ndc.png")
            return await ctx.reply(embed=em)

    @commands.hybrid_command(name="rob", description="woke up and chose to be a thief")
    @app_commands.describe(user="The user to rob.")
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
        if ctx.author.id == user.id:
            em = discord.Embed(color=discord.Color.red(), title="This is stupid",
                               description=f"How do you plan on stealing money from yourself? Fuck off.")
            return await ctx.reply(embed=em)

        random.shuffle(fake_robbery_scenarios)
        scenario = random.choice(fake_robbery_scenarios)
        rob_scenario = scenario[0].replace("{0}", ctx.author.mention).replace("{1}", user.mention)
        rob_outcome = scenario[1]

        אחוז_הפסד = 25
        loss_percent = random.randint(10, 15)

        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        author_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)

        if author_data.is_in_jail():
            release_time = author_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(release_time, style="R"
                                                          )
            return await ctx.send(
                f"Look at you all handcuffed and shit, you'll get out of those {remaining_timestamp}")

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

            em = discord.Embed(color=discord.Color.green(),
                               description=rob_scenario + f" gaining ${user_loss_total}, congrats on being a bad person")
            return await ctx.reply(embed=em)
        else:
            author_balance = author_data.balance
            total_percentage = loss_percent + אחוז_הפסד
            author_loss_total = subtraction_percentage(author_balance, total_percentage)
            total = max(author_balance - author_loss_total, 0)
            jail_time = random.randint(1, 3)
            fine = random.randint(100, 1000)
            probability = 0.3
            random_number = random.random()

            em = discord.Embed(color=discord.Color.red(),
                               description=rob_scenario + f" failing miserably and losing ${author_loss_total}")
            if random_number < probability:
                await user_data.jail_user(jail_time, fine, self.bot)
                em.add_field(name="Punishment",
                             value=f"You are in jail for {jail_time} hours and have to pay a fine of {fine}. Run </bail:1145445177092231341> to do so.")
            await author_data.update_balance(total, self.bot)
            return await ctx.reply(embed=em)

    @commands.hybrid_command(description="Flip a coin.", aliases=["coin"])
    @app_commands.describe(side='pick a side, heads or tails')
    @app_commands.describe(bet='the amount of money to bet')
    async def coinflip(self, ctx, side: Literal['heads', 'tails'], bet: int):
        side = side.lower()
        if side not in ['heads', 'tails']:
            return await ctx.send("consider playing this game right and choosing `heads` or `tails`, dumbass.")

        if not 1 <= bet <= 500:
            return await ctx.send("Hey whore, Only bets of 1 - 500 are allowed")
        user = ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance

        if user_data.is_in_jail():
            release_time = user_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(release_time, style="R"
                                                          )
            return await ctx.send(
                f"Look at you all handcuffed and shit, you'll get out of those {remaining_timestamp}")

        if bet > user_balance:
            return await ctx.send(
                f"Hey Whore, You don't have enough money to do this lul, your balance is ${user_balance}")

        coin_tails = ("Tails", "<:cointails:1145284840644694066>", "https://cdn.discordapp.com/attachments/1145071029954297888/1145284778929704990/cointails-removebg-preview_1.png")
        coin_heads = ("Heads", "<:coinheads:1145283300009713775>", "https://cdn.discordapp.com/attachments/1145071029954297888/1145280717421559828/coinheads-removebg-preview.png")

        rng = random.randint(0, 9)
        res = coin_heads if rng > 4 else coin_tails

        if side == res[0].lower():
            user_balance += bet
            msg = f"You Won ${bet}"
            em = discord.Embed(title="", description=f"{msg}",
                               color=discord.Color.green())
            em.set_thumbnail(url=res[2])
            em.set_author(
                name=f"{user}'s Coinflip",
                icon_url="https://cdn.discordapp.com/attachments/1145071029954297888/1145449093326442526/coinflip-removebg-preview.png",
                url="https://cdn.discordapp.com/attachments/1145071029954297888/1145449093326442526/coinflip-removebg-preview.png"
            )
            timestamp = datetime.datetime.now(datetime.timezone.utc)
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            await ctx.reply(embed=em)
        else:
            user_balance -= bet
            msg = f"You Lost ${bet}"
            em = discord.Embed(title="", description=f"{msg}",
                               color=discord.Color.red())
            em.set_thumbnail(url=res[2])
            em.set_author(
                name=f"{user}'s Coinflip",
                icon_url="https://cdn.discordapp.com/attachments/1145071029954297888/1145449093326442526/coinflip-removebg-preview.png",
                url="https://cdn.discordapp.com/attachments/1145071029954297888/1145449093326442526/coinflip-removebg-preview.png"
            )
            timestamp = datetime.datetime.now(datetime.timezone.utc)
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            await ctx.reply(embed=em)
        await user_data.update_balance(user_balance, self.bot)


async def setup(bot):
    await bot.add_cog(Gambling(bot))
