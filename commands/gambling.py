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

from database import User
from config.lists import fake_robbery_scenarios, funny_crime_scenarios
from config.settings_config import jackpot_emoji, calculate_payout, jackpot_payout, bonus_multiplier
from utils.checks import persistent_cooldown
from utils.utilities import subtraction_percentage, generate_embed_color


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="slots", description="what happens in vegas...")
    @persistent_cooldown(1, 60, commands.BucketType.user)
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
        await user_data.update_balance(user_bet)
        slot_message = " ".join(result)
        payout, is_jackpot, is_bonus = calculate_payout(result)
        balance = (user_data.balance + payout)
        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="Pull the lever!")
        em.set_author(
            name="slots Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        if is_jackpot:
            em.description = f"{slot_message}\n🎉 Jackpot! You won {jackpot_payout} coins!"
        elif is_bonus:
            em.description = f"{slot_message}\n🎉 Bonus! You won {payout} coins with a bonus multiplier of {bonus_multiplier}!"
        else:
            em.description = f"{slot_message}\nYou won {payout} coins!"
        await user_data.update_balance(balance)
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
            await user_data.update_balance(user_total)

            em = discord.Embed(color=discord.Color.green(),
                               description=crime_scenario + f" gaining ${amount}, congrats on getting away with it")
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145112557414264892/1145112660208275528/dc.png")
            em.set_author(
                name="Crime Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
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
                await user_data.jail_user(jail_time, fine)
                em.add_field(name="Punishment",
                             value=f"You are in jail for {jail_time} hours and have to pay a fine of {fine}. Run </bail:1145445177092231341> to do so.")
            await user_data.update_balance(user_total)

            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1145112557414264892/1145115052505042974/ndc.png")
            em.set_author(
                name="Crime Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
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
        rob_scenario = scenario[0].replace(
            "{0}", ctx.author.mention).replace("{1}", user.mention)
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
            await author_data.subtract_balance(250)
            em = discord.Embed(color=discord.Color.red(), title="You're Dumb",
                               description=f"{ctx.author.mention} attempted to rob {user.mention} who was so very poor, as retribution they've lost 250")
            return await ctx.reply(embed=em)

        if rob_outcome:
            user_balance = user_data.balance
            user_loss_total = subtraction_percentage(
                user_balance, loss_percent)
            author_total = max(author_data.balance + user_loss_total, 0)
            user_total = max(user_data.balance - user_loss_total, 0)
            await user_data.update_balance(user_total)
            await author_data.update_balance(author_total)

            em = discord.Embed(color=discord.Color.green(),
                               description=rob_scenario + f" gaining ${user_loss_total}, congrats on being a bad person")
            em.set_author(
                name="Rob Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
        else:
            author_balance = author_data.balance
            total_percentage = loss_percent + אחוז_הפסד
            author_loss_total = subtraction_percentage(
                author_balance, total_percentage)
            total = max(author_balance - author_loss_total, 0)
            jail_time = random.randint(1, 3)
            fine = random.randint(100, 1000)
            probability = 0.3
            random_number = random.random()

            em = discord.Embed(color=discord.Color.red(),
                               description=rob_scenario + f" failing miserably and losing ${author_loss_total}")
            if random_number < probability:
                await user_data.jail_user(jail_time, fine)
                em.add_field(name="Punishment",
                             value=f"You are in jail for {jail_time} hours and have to pay a fine of {fine}. Run </bail:1145445177092231341> to do so.")
            await author_data.update_balance(total)
            em.set_author(
                name="Rob Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)

    @commands.hybrid_command(description="Flip a coin.", aliases=["coin"])
    @persistent_cooldown(1, 60, commands.BucketType.user)
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

        coin_tails = ("Tails", "<:cointails:1145284840644694066>",
                      "https://cdn.discordapp.com/attachments/1145071029954297888/1145284778929704990/cointails-removebg-preview_1.png")
        coin_heads = ("Heads", "<:coinheads:1145283300009713775>",
                      "https://cdn.discordapp.com/attachments/1145071029954297888/1145280717421559828/coinheads-removebg-preview.png")

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
        await user_data.update_balance(user_balance)

    # rps
    @commands.hybrid_command(description="Play rock paper scissors.")
    @persistent_cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(choice="rock, paper, or scissors")
    @app_commands.describe(bet='the amount of money to bet')
    async def rps(self, ctx, choice: Literal['rock', 'paper', 'scissors'], bet: int):
        if bet <= 0:
            await ctx.send("Invalid bet. Please bet a positive amount.")
            return
        if bet >= 500:
            await ctx.send("Invalid bet. Please bet under 500.")
            return
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if bet > user_balance:
            await ctx.send("You don't have enough money to do this.")
            return

        valid_choices = ['rock', 'paper', 'scissors']
        # You'll need to import 'random'
        bot_choice = random.choice(valid_choices)

        # Determine the winner
        if choice == bot_choice:
            result = "tie"
        elif (choice == "rock" and bot_choice == "scissors") or \
                (choice == "paper" and bot_choice == "rock") or \
                (choice == "scissors" and bot_choice == "paper"):
            result = "win"
        else:
            result = "lose"

        # Adjust the winnings multiplier as needed
        winnings_multiplier = 2

        if result == "win":
            winnings = bet * winnings_multiplier
            await user_data.update_balance(user_balance + winnings)
            em = discord.Embed(color=discord.Color.green(),
                               description=f"You chose {choice}, the bot chose {bot_choice}. You win {winnings} coins!")
            em.set_author(
                name="rock, paper, or scissors",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
        elif result == "lose":
            await user_data.update_balance(user_balance - bet)
            em = discord.Embed(color=discord.Color.red(),
                               description=f"You chose {choice}, the bot chose {bot_choice}. You lose {bet} coins.")
            em.set_author(
                name="rock, paper, or scissors",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
        else:
            em = discord.Embed(color=discord.Color.yellow(),
                               description=f"You chose {choice}, the bot chose {bot_choice}. It's a tie!")
            em.set_author(
                name="rock, paper, or scissors",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
            await ctx.reply(embed=em)

    @commands.hybrid_command(description="Play rock paper scissors lizard spock.")
    @persistent_cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(choice="rock, paper, scissors, lizard, or spock")
    @app_commands.describe(bet='the amount of money to bet')
    async def rpsls(self, ctx, choice: Literal['rock', 'paper', 'scissors', 'lizard', 'spock'], bet: int):
        if bet <= 0:
            await ctx.send("Invalid bet. Please bet a positive amount.")
            return
        if bet >= 500:
            await ctx.send("Invalid bet. Please bet under 500.")
            return
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if bet > user_balance:
            await ctx.send("You don't have enough money to do this.")
            return

        valid_choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
        # You'll need to import 'random'
        bot_choice = random.choice(valid_choices)

        # Determine the winner
        if choice == bot_choice:
            result = "tie"
        elif (choice == "rock" and bot_choice in ["scissors", "lizard"]) or \
                (choice == "paper" and bot_choice in ["rock", "spock"]) or \
                (choice == "scissors" and bot_choice in ["paper", "lizard"]) or \
                (choice == "lizard" and bot_choice in ["paper", "spock"]) or \
                (choice == "spock" and bot_choice in ["rock", "scissors"]):
            result = "win"
        else:
            result = "lose"

        # Adjust the winnings multiplier as needed
        winnings_multiplier = 2

        if result == "win":
            winnings = bet * winnings_multiplier
            await user_data.update_balance(user_balance + winnings)
            em = discord.Embed(color=discord.Color.green(),
                               description=f"You chose {choice}, the bot chose {bot_choice}. You win {winnings} coins!")
            em.set_author(
                name="rock, paper, scissors, lizard, or spock",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
        elif result == "lose":
            await user_data.update_balance(user_balance - bet)
            em = discord.Embed(color=discord.Color.red(),
                               description=f"You chose {choice}, the bot chose {bot_choice}. You lose {bet} coins.")
            em.set_author(
                name="rock, paper, scissors, lizard, or spock",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
        else:
            em = discord.Embed(color=discord.Color.yellow(),
                               description=f"You chose {choice}, the bot chose {bot_choice}. It's a tie!")
            em.set_author(
                name="rock, paper, scissors, lizard, or spock",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            await ctx.reply(embed=em)

    @commands.hybrid_command(name="dice", description="Roll a dice.")
    @persistent_cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(bet='the amount of money to bet')
    async def dice(self, ctx, bet: int):
        if bet <= 0:
            await ctx.send("Invalid bet. Please bet a positive amount.")
            return
        if bet >= 500:
            await ctx.send("Invalid bet. Please bet under 500.")
            return
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if bet > user_balance:
            await ctx.send("You don't have enough money to do this.")
            return

        user_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)

        if user_roll > bot_roll:
            winnings = bet * 2
            await user_data.update_balance(user_balance + winnings)
            em = discord.Embed(color=discord.Color.green(),
                               description=f"You rolled {user_roll}, the bot rolled {bot_roll}. You win {winnings} coins!")
            em.set_author(
                name="Dice Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
        elif user_roll < bot_roll:
            await user_data.update_balance(user_balance - bet)
            em = discord.Embed(color=discord.Color.red(),
                               description=f"You rolled {user_roll}, the bot rolled {bot_roll}. You lose {bet} coins.")
            em.set_author(
                name="Dice Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            return await ctx.reply(embed=em)
        else:
            em = discord.Embed(color=discord.Color.yellow(),
                               description=f"You rolled {user_roll}, the bot rolled {bot_roll}. It's a tie!")
            em.set_author(
                name="Dice Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png")
            )
            await ctx.reply(embed=em)

    @commands.hybrid_command(name="roulette", description="Spin the roulette wheel.")
    @persistent_cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(bet='the amount of money to bet')
    @app_commands.describe(choice='the number to bet on')
    @app_commands.describe(color='the color to bet on')
    async def roulette(self, ctx, bet: int, choice: Optional[int] = None,
                       color: Optional[Literal['red', 'black']] = None):
        if bet <= 0:
            await ctx.send("Invalid bet. Please bet a positive amount.")
            return
        if bet >= 500:
            await ctx.send("Invalid bet. Please bet under 500.")
            return
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if bet > user_balance:
            await ctx.send("You don't have enough money to do this.")
            return
        if choice is not None and color is not None:
            await ctx.send("You can only bet on a number or a color, not both.")
            return

        # Generate the result
        result = random.randint(0, 36)

        # Determine the color
        if result == 0:
            result_color = "green"
        elif result in range(1, 11) or result in range(19, 29):
            result_color = "black"
        else:
            result_color = "red"

        # Determine the payout
        if choice is None and color is None:
            winnings_multiplier = 2
        elif choice is not None and color is not None:
            winnings_multiplier = 36
        else:
            winnings_multiplier = 18

        # Determine the winner
        if choice is not None and choice == result:
            result = "win"
        elif color is not None and color == result_color:
            result = "win"
        else:
            result = "lose"

        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="Spin the roulette wheel.")
        em.set_author(
            name="Roulette Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        if result == "win":
            winnings = bet * winnings_multiplier
            await user_data.update_balance(user_balance + winnings)
            em.description = "The result was {result}, you win {winnings} coins!"
        elif result == "lose":
            await user_data.update_balance(user_balance - bet)
            em.description = f"The result was {result}, you lose {bet} coins."
        else:
            em.description = f"The result was {result}, it's a tie!"
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="blackjack", description="Play a game of blackjack.")
    @persistent_cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(bet='the amount of money to bet')
    async def blackjack(self, ctx, bet: int):
        if bet <= 0:
            await ctx.send("Invalid bet. Please bet a positive amount.")
            return
        if bet >= 500:
            await ctx.send("Invalid bet. Please bet under 500.")
            return
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if bet > user_balance:
            await ctx.send("You don't have enough money to do this.")
            return

        # Generate the cards
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10] * 4 + [11, 12, 13, 14] * 4

        # Draw the cards
        user_card1 = random.choice(cards)
        user_card2 = random.choice(cards)
        bot_card1 = random.choice(cards)
        bot_card2 = random.choice(cards)

        # Determine the winner
        if user_card1 + user_card2 > 21:
            user_result = "lose"
        elif user_card1 + user_card2 == 21:
            user_result = "win"
        elif bot_card1 + bot_card2 > 21:
            user_result = "win"
        elif bot_card1 + bot_card2 == 21:
            user_result = "lose"
        else:
            user_result = "tie"

        winnings_multiplier = 2

        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="blackjack")
        em.set_author(
            name="Blackjack Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )

        if user_result == "win":
            winnings = bet * winnings_multiplier
            await user_data.update_balance(user_balance + winnings)
            em.description = f"You drew {user_card1} and {user_card2}. The bot drew {bot_card1} and {bot_card2}. You win {winnings} coins!"
        elif user_result == "lose":
            await user_data.update_balance(user_balance - bet)
            em.description = f"You drew {user_card1} and {user_card2}. The bot drew {bot_card1} and {bot_card2}. You lose {bet} coins."
        else:
            em.description = f"You drew {user_card1} and {user_card2}. The bot drew {bot_card1} and {bot_card2}. It's a tie!"

        await ctx.reply(embed=em)

    @commands.hybrid_command(name="wheel", description="Spin the wheel of fortune.")
    @persistent_cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(bet='the amount of money to bet')
    async def wheel(self, ctx, bet: int):
        if bet <= 0:
            await ctx.send("Invalid bet. Please bet a positive amount.")
            return
        if bet >= 500:
            await ctx.send("Invalid bet. Please bet under 500.")
            return
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if bet > user_balance:
            await ctx.send("You don't have enough money to do this.")
            return

        # Generate the wheel
        wheel = ["red", "blue", "green", "yellow", "orange", "purple", "pink"]

        # Spin the wheel
        result = random.choice(wheel)

        # Determine the payout
        if result == "red":
            winnings_multiplier = 2
        elif result in ["blue", "green", "yellow"]:
            winnings_multiplier = 3
        elif result in ["orange", "purple", "pink"]:
            winnings_multiplier = 5

        # Determine the winner
        if result == "red":
            result = "win"
        elif result in ["blue", "green", "yellow"]:
            result = "win"
        elif result in ["orange", "purple", "pink"]:
            result = "win"
        else:
            result = "lose"

        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="Spin the wheel of fortune.")
        em.set_author(
            name="Wheel Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )

        if result == "win":
            winnings = bet * winnings_multiplier
            await user_data.update_balance(user_balance + winnings)
            em.description = f"The result was {result}, you win {winnings} coins!"
        elif result == "lose":
            await user_data.update_balance(user_balance - bet)
            em.description = f"The result was {result}, you lose {bet} coins."
        else:
            em.description = f"The result was {result}, it's a tie!"
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="highlow", description="Play a game of high low.")
    @persistent_cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(bet='the amount of money to bet')
    async def hilow(self, ctx, bet: int):
        if bet <= 0:
            await ctx.send("Invalid bet. Please bet a positive amount.")
            return
        if bet >= 500:
            await ctx.send("Invalid bet. Please bet under 500.")
            return
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id)
        user_balance = user_data.balance
        if bet > user_balance:
            await ctx.send("You don't have enough money to do this.")
            return

        # Generate the cards
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10] * 4 + [11, 12, 13, 14] * 4

        # Draw the cards
        user_card1 = random.choice(cards)
        user_card2 = random.choice(cards)
        bot_card1 = random.choice(cards)
        bot_card2 = random.choice(cards)

        # Determine the winner
        if user_card1 + user_card2 > bot_card1 + bot_card2:
            user_result = "win"
        elif user_card1 + user_card2 == bot_card1 + bot_card2:
            user_result = "tie"
        else:
            user_result = "lose"
        winnings_multiplier = 2

        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="Play a game of high low.")
        em.set_author(
            name="HighLow Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )

        if user_result == "win":
            winnings = bet * winnings_multiplier
            await user_data.update_balance(user_balance + winnings)
            em.description = f"You drew {user_card1} and {user_card2}. The bot drew {bot_card1} and {bot_card2}. You win {winnings} coins!"
        elif user_result == "lose":
            await user_data.update_balance(user_balance - bet)
            em.description = f"You drew {user_card1} and {user_card2}. The bot drew {bot_card1} and {bot_card2}. You lose {bet} coins."
        else:
            em.description = f"You drew {user_card1} and {user_card2}. The bot drew {bot_card1} and {bot_card2}. It's a tie!"
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Gambling(bot))
