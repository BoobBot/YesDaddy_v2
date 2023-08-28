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
from config.lists import job_descriptions, fake_robbery_scenarios, funny_crime_scenarios
from utils.checks import persistent_cooldown
from utils.utilities import subtraction_percentage, generate_embed_color, progress_percentage

emoji_payouts = {
    "⚽": 5,
    "🎱": 10,
    "🎰": 20,
    "🍀": 50,
    "🎮": 100,
    "💰": 200  # Jackpot payout is handled separately
}

jackpot_emoji = "💰"
jackpot_payout = 500
bonus_multiplier = 2


def calculate_payout(result):
    total_payout = 0
    is_jackpot = False
    is_bonus = False
    if len(set(result)) == 1:  # All three slots are the same
        is_bonus = True
        emoji = result[0]
        if emoji in emoji_payouts:
            total_payout = emoji_payouts[emoji] * bonus_multiplier
    else:
        for emoji in result:
            if emoji in emoji_payouts:
                total_payout += emoji_payouts[emoji]
            if emoji == jackpot_emoji:
                is_jackpot = True
    if is_jackpot:
        return jackpot_payout, True, False
    return total_payout, False, is_bonus


async def create_leaderboard_embed(ctx, title, entries):
    embed = Embed(title=title)
    for index, (user, member) in enumerate(entries[:10], start=1):
        emoji = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else "  "
        value = f"{emoji} {member.display_name}: {user.level if title == 'Leaderboard - Levels:' else user.balance + user.bank_balance}"
        embed.add_field(name=f"#{index}", value=value, inline=False)
    return embed


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_jail_loop.start()

    def cog_unload(self):
        self.check_jail_loop.cancel()

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

    @commands.hybrid_command(name="bail", description="get you or someone else out of jail")
    @app_commands.describe(user="User to bailout")
    async def bail(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        if not user_data.is_in_jail():
            return await ctx.reply(f":x: {user.mention} is not in jail.")
        user_balance = user_data.balance + user_data.bank_balance
        cost = user_data.jail.get("fine", 0)
        # TODO add higher fine for longer jail time
        cost_total = subtraction_percentage(user_balance, 10) + cost
        if cost_total > user_data.balance:
            return await ctx.reply(f":x: {user.mention} needs ${cost_total} to get out of jail.")
        await user_data.subtract_balance(cost_total, self.bot)
        await user_data.update_user({"jail": {}}, self.bot)
        await ctx.reply(f":white_check_mark: {user.mention} has been released from jail for {cost_total}.")

    @commands.hybrid_command(name="profile", description="Look at your profile.")
    async def profile(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_color = await generate_embed_color(user)
        exp_needed = int(((user_data.level + 1) * 10) ** 2)
        bar = progress_percentage(user_data.xp, exp_needed)

        em = discord.Embed(title=f"{user}'s Profile", color=user_color)
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        em.add_field(name="Level", value=f"{user_data.level} {bar} {user_data.level + 1}", inline=False)
        em.add_field(name="Experience", value=f"{user_data.xp} / {exp_needed}")
        em.add_field(name="Balance", value=f"{user_data.balance}")
        em.add_field(name="Bank Balance", value=f"{user_data.bank_balance}")
        if user_data.is_in_jail():
            release_time = user_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(release_time, style="R"
                                                          )
            em.add_field(name="Jail?", value=f"experience freedom in {remaining_timestamp}")

        await ctx.reply(embed=em)

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

            em = discord.Embed(color=discord.Color.green(), description=crime_scenario)
            em.add_field(name="Crime Result", value=f"{ctx.author.mention} did some crime gaining {amount}")
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145112557414264892/1145112660208275528/dc.png")
            return await ctx.reply(embed=em)
        else:
            user_total = (user_balance - amount)
            jail_time = random.randint(1, 3)
            fine = random.randint(100, 1000)
            await user_data.jail_user(jail_time, fine, self.bot)
            await user_data.update_balance(user_total, self.bot)
            em = discord.Embed(color=discord.Color.red(), description=crime_scenario)
            em.add_field(name="Crime Result",
                         value=f"{ctx.author.mention} attempted to do some crime and got caught losing {amount}, your lawyer will see you now.")
            em.add_field(name="Punishment",
                         value=f"You are in jail for {jail_time} hours and have to pay a fine of {fine}.")

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
        await recipient_data.update_balance(new_recipient_balance, self.bot)
        await user_data.update_balance(new_user_balance, self.bot)
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
        await user_data.update_balance(new_user_balance, self.bot)
        await user_data.update_bank_balance(new_user_bank_balance, self.bot)
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
        await user_data.update_balance(0, self.bot)
        await user_data.update_bank_balance(new_user_bank_balance, self.bot)
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
        await user_data.update_balance(new_user_balance, self.bot)
        await user_data.update_bank_balance(new_user_bank_balance, self.bot)
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
        await user_data.update_balance(new_user_balance, self.bot)
        await user_data.update_bank_balance(new_user_bank_balance, self.bot)
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

    @commands.command(description="Flip a coin.", aliases=["coin"])
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

        coin_tails = ("Tails", "<:cointails:1145284840644694066>")
        coin_heads = ("Heads", "<:coinheads:1145283300009713775>")

        rng = random.randint(0, 9)
        res = coin_heads if rng > 4 else coin_tails

        if side == res[0].lower():
            user_balance += bet
            msg = f"You Won ${bet}"
            em = discord.Embed(title="", description=f"{msg}",
                               color=discord.Color.green())
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145071029954297888/1145280717421559828/coinheads-removebg-preview.png")
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
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145071029954297888/1145284778929704990/cointails-removebg-preview_1.png")
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

    @tasks.loop(minutes=5)
    async def check_jail_loop(self):
        users_in_jail = await self.bot.db_client.get_users_in_jail()

        for user_id in users_in_jail:
            user = await self.bot.db_client.get_user(user_id)
            if user.is_in_jail():
                release_time = user.jail["start_time"].replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(
                    hours=user.jail["duration_hours"])
                current_time = datetime.datetime.now(datetime.timezone.utc)

                if current_time >= release_time:
                    fine = user.jail.get("fine", 0)
                    await user.subtract_balance(fine, self.bot)
                    await user.update_user({"jail": {}}, self.bot)
                    self.bot.log.info(f"User {user_id} has been released from jail.")

    @commands.hybrid_group(name="leaderboard", aliases=["lb"], description="View the leaderboard.")
    async def leaderboard(self, ctx):
        await ctx.send("Please use a valid subcommand: `level` or `balance`.")

    @leaderboard.command(name="level", aliases=["lvl"], description="View the level leaderboard.")
    async def leaderboard_level(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_level(limit=20)  # Change this to your database function

        guild = ctx.guild

        sorted_users = []
        for user_data in top_users:
            user_data.setdefault("jail", {})  # Provide a default value for 'jail' attribute
            user = User(**user_data)
            member = ctx.guild.get_member(user.user_id)

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(key=lambda entry: entry[0].level, reverse=True)

        embed = await create_leaderboard_embed(ctx, "Leaderboard - Levels:", sorted_users)
        await ctx.send(embed=embed)

    @leaderboard.command(name="combined", aliases=["comb"], description="View the combined balance leaderboard.")
    async def leaderboard_combined(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_combined_balance(
            limit=20)  # Change this to your database function

        guild = ctx.guild
        sorted_users = []
        for user_data in top_users:
            user_data.setdefault("jail", {})  # Provide a default value for 'jail' attribute
            user = User(**user_data)
            member = ctx.guild.get_member(user.user_id)

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(key=lambda entry: entry[0].balance + entry[0].bank_balance, reverse=True)

        embed = await self.create_leaderboard_embed(ctx, "Leaderboard - Combined Balance:", sorted_users)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
