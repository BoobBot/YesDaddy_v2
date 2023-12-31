import asyncio
import typing
import discord
from discord import app_commands, AllowedMentions
from discord.ext import commands
import random

from config.settings_config import racers
from utils.animal import Animal
from utils.utilities import generate_embed_color


# https://github.com/Redjumpman/Jumper-Plugins/blob/V3_dpy2/race/race.py

class FancyDict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


class FancyDictList(dict):
    def __missing__(self, key):
        value = self[key] = []
        return value


class Race(commands.Cog):
    """Cog for racing animals"""

    def __init__(self, bot):
        self.bot = bot
        self.active = FancyDict()
        self.started = FancyDict()
        self.winners = FancyDictList()
        self.players = FancyDictList()
        self.bets = FancyDict()

        guild_defaults = {
            "Wait": 60,
            "Mode": "normal",
            "Prize": 100,
            "Pooling": False,
            "Payout_Min": 0,
            "Bet_Multiplier": 2,
            "Bet_Min": 10,
            "Bet_Max": 50,
            "Bet_Allowed": True,
            "Games_Played": 0,
        }

        # First, Second, and Third place wins
        member_defaults = {"Wins": {"1": 0, "2": 0, "3": 0}, "Losses": 0}

    @commands.hybrid_group()
    @commands.guild_only()
    async def race(self, ctx):
        """Race related commands."""
        pass

    @race.command()
    async def start(self, ctx):
        """Starts s race."""
        await ctx.defer(ephemeral=False)
        if self.active[ctx.guild.id]:
            return await ctx.send(f"A race is already in progress! Type {ctx.prefix}`race enter` to enter!")
        self.active[ctx.guild.id] = True
        self.players[ctx.guild.id].append(ctx.author)
        wait = 120
        current = 0

        await ctx.send(
            f"🚩 A race has begun! Type {ctx.prefix}race enter "
            f"to join the race! 🚩\nThe race will begin in "
            f"{wait} seconds!\n\n**{ctx.author.mention}** entered the race!"
            , allowed_mentions=AllowedMentions.all())
        await asyncio.sleep(wait)
        self.started[ctx.guild.id] = True
        await ctx.channel.send("🏁 The race is now in progress. 🏁")
        await self.run_game(ctx)

        msg, embed = await self._build_end_screen(ctx)
        await ctx.channel.send(content=msg, embed=embed)
        await self._race_teardown(ctx)

    @race.command()
    @app_commands.describe(user="The user to get stats for.")
    async def stats(self, ctx, user: typing.Optional[discord.Member]):
        """Display your race stats."""
        await ctx.send("This command is currently disabled.")
        # if not user:
        #     user = ctx.author
        # color = await ctx.embed_colour()
        # user_data = await self.config.member(user).all()
        # player_total = sum(user_data["Wins"].values()) + user_data["Losses"]
        # server_total = await self.config.guild(ctx.guild).Games_Played()
        # try:
        #     percent = round((player_total / server_total) * 100, 1)
        # except ZeroDivisionError:
        #     percent = 0
        # embed = discord.Embed(color=color, description="Race Stats")
        # embed.set_author(name=f"{user}", icon_url=user.avatar.url)
        # embed.add_field(
        #     name="Wins",
        #     value=(
        #         f"1st: {user_data['Wins']['1']}\n2nd: {user_data['Wins']['2']}\n3rd: {user_data['Wins']['3']}"
        #     ),
        # )
        # embed.add_field(name="Losses", value=f'{user_data["Losses"]}')
        # embed.set_footer(
        #     text=(
        #         f"You have played in {player_total} ({percent}%) races out "
        #         f"of {server_total} total races on the server."
        #     )
        # )
        # await ctx.send(embed=embed)

    @race.command()
    @app_commands.describe(bet="The amount to bet.")
    @app_commands.describe(user="The user to place a bet on.")
    async def bet(self, ctx, bet: int, user: discord.Member):
        """Bet on a user in the race."""
        if await self.bet_conditions(ctx, bet, user):
            self.bets[ctx.guild.id][ctx.author.id] = {user.id: bet}
            user_data = await ctx.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
            await user_data.subtract_balance(bet)
            await ctx.send(f"{ctx.author.mention} placed a ${bet} bet on {user.display_name}.")

    @race.command()
    async def enter(self, ctx):
        """Allows you to enter the race.
        """
        if self.started[ctx.guild.id]:
            return await ctx.send(
                "A race has already started.  Please wait for the first one to finish before entering or starting a race."
            )
        elif not self.active.get(ctx.guild.id):
            return await ctx.send("A race must be started before you can enter.")
        elif ctx.author in self.players[ctx.guild.id]:
            return await ctx.send("You have already entered the race.")
        elif len(self.players[ctx.guild.id]) >= 14:
            return await ctx.send("The maximum number of players has been reached.")
        else:
            self.players[ctx.guild.id].append(ctx.author)
            await ctx.send(f"{ctx.author.mention} has joined the race.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def race_clear(self, ctx):
        self.clear_local(ctx)
        await ctx.send("Race cleared.")

    async def stats_update(self, ctx):
        names = [player for player, emoji in self.winners[ctx.guild.id]]
        for player in self.players[ctx.guild.id]:
            if player in names:
                position = names.index(player) + 1
                # current = await self.config.member(player).Wins.get_raw(str(position))
                # await self.config.member(player).Wins.set_raw(str(position), value=current + 1)
                pass
            else:
                # current = await self.config.member(player).Losses()
                # await self.config.member(player).Losses.set(current + 1)
                pass

    async def _race_teardown(self, ctx):
        await self.stats_update(ctx)
        await self.distribute_prizes(ctx)
        await self.bet_payouts(ctx)
        self.clear_local(ctx)

    def clear_local(self, ctx):
        self.players[ctx.guild.id].clear()
        self.winners[ctx.guild.id].clear()
        self.bets[ctx.guild.id].clear()
        self.active[ctx.guild.id] = False
        self.started[ctx.guild.id] = False

    async def distribute_prizes(self, ctx):
        if 1 > len(self.players[ctx.guild.id]):
            return

        if self.winners[ctx.guild.id][0][0].bot:
            return

        user_data = await ctx.bot.db_client.get_user(user_id=self.winners[ctx.guild.id][0][0].id, guild_id=ctx.guild.id)
        await user_data.add_balance(100 * len(self.players[ctx.guild.id]))

    async def bet_payouts(self, ctx):
        if not self.bets[ctx.guild.id]:
            return
        multiplier = 2
        first = self.winners[ctx.guild.id][0]
        for user_id, wagers in self.bets[ctx.guild.id].items():
            for jockey, bet in wagers.items():
                if jockey == first[0].id:
                    user = ctx.guild.get_member(user_id)
                    user_data = await ctx.bot.db_client.get_user(user_id=user_id, guild_id=ctx.guild.id)
                    await user_data.add_balance(int(bet * multiplier))

    async def bet_conditions(self, ctx, bet, user):
        if not self.active[ctx.guild.id]:
            await ctx.send(":x: There isn't a race right now.")
            return False
        elif self.started[ctx.guild.id]:
            await ctx.send(":x: You can't place a bet after the race has started.")
            return False
        elif user not in self.players[ctx.guild.id]:
            await ctx.send(":x: You can't bet on someone who isn't in the race.")
            return False
        elif self.bets[ctx.guild.id][ctx.author.id]:
            await ctx.send(":x: You have already entered a bet for the race.")
            return False
        minimum = 10
        maximum = 100000
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if bet > user_data.balance:
            await ctx.send(":x: You do not have enough money.")
            return False
        elif minimum <= bet <= maximum:
            return True
        else:
            await ctx.send(f":x: Bet must not be lower than {minimum} or higher than {maximum}.")
            return False

    async def _build_end_screen(self, ctx):
        if len(self.winners[ctx.guild.id]) == 3:
            first, second, third = self.winners[ctx.guild.id]
        else:
            first, second, = self.winners[ctx.guild.id]
            third = None
        payout_msg = self._payout_msg(ctx)
        footer = await self._get_bet_winners(ctx, first[0])
        color = await generate_embed_color(first[0])
        embed = discord.Embed(colour=color, title="Race Results")
        embed.add_field(name=f"{first[0].display_name} 🥇", value=first[1].emoji)
        embed.add_field(name=f"{second[0].display_name} 🥈", value=second[1].emoji)
        if third:
            embed.add_field(name=f"{third[0].display_name} 🥉", value=third[1].emoji)
        embed.add_field(name="-" * 90, value="\u200b", inline=False)
        embed.add_field(name="Payouts", value=payout_msg)
        embed.set_footer(text=f"Bet winners: {footer[0:2000]}")
        mentions = "" if first[0].bot else f"{first[0].mention}"
        mentions += "" if second[0].bot else f", {second[0].mention}" if not first[0].bot else f"{second[0].mention}"
        mentions += "" if third is None or third[0].bot else f", {third[0].mention}"
        return mentions, embed

    def _payout_msg(self, ctx):
        if self.winners[ctx.guild.id][0][0].bot:
            return f"{self.winners[ctx.guild.id][0][0]} is the winner!"
        return f"{self.winners[ctx.guild.id][0][0]} received ${100 * len(self.players[ctx.guild.id])}."

    async def _get_bet_winners(self, ctx, winner):
        bet_winners = []
        multiplier = 2
        for better, bets in self.bets[ctx.guild.id].items():
            for jockey, bet in bets.items():
                if jockey == winner.id:
                    member = ctx.guild.get_member(better)
                    bet_winners.append(f"{member.display_name}: {bet * multiplier}")
        return ", ".join(bet_winners) if bet_winners else "None."

    async def _game_setup(self, ctx):
        users = self.players[ctx.guild.id]
        players = [(Animal(*random.choice(racers)), user) for user in users]
        if len(players) == 1:
            players.append((Animal(*random.choice(racers)), ctx.bot.user))
        return players

    async def run_game(self, ctx):
        players = await self._game_setup(ctx)
        setup = "\u200b\n" + "\n".join(
            f":carrot: **{animal.current}** 🏁[{jockey.display_name}]" for animal, jockey in players
        )
        track = await ctx.channel.send(setup)
        while not all(animal.position == 0 for animal, jockey in players):
            await asyncio.sleep(2.0)
            fields = []
            for animal, jockey in players:
                if animal.position == 0:
                    fields.append(f":carrot: **{animal.current}** 🏁  [{jockey.display_name}]")
                    continue
                animal.move()
                fields.append(f":carrot: **{animal.current}** 🏁  [{jockey.display_name}]")
                if animal.position == 0 and len(self.winners[ctx.guild.id]) < 3:
                    self.winners[ctx.guild.id].append((jockey, animal))
            t = "\u200b\n" + "\n".join(fields)
            try:
                await track.edit(content=t)
            except discord.errors.NotFound:
                pass


async def setup(bot):
    await bot.add_cog(Race(bot))
