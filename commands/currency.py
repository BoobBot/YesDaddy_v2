import datetime
import random
import re
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from config.items import maybe_loot
from config.lists import job_descriptions, adv_success_strings, adv_scenarios, adv_failure_strings
from config.settings_config import chop_resource_info, mine_resource_info, fish_info, monsters
from utils.checks import persistent_cooldown
from utils.utilities import generate_embed_color
from views.reminder_view import Reminder


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="adventure", description="Go on an adventure!")
    @persistent_cooldown(1, 600, commands.BucketType.user)
    @commands.guild_only()
    async def adventure(self, ctx):
        author = ctx.author.mention
        user = ctx.author
        user_color = await generate_embed_color(ctx.author)
        success_list = []
        fail_list = []
        [success_list.append(i) if i[1] else fail_list.append(i)
         for i in adv_scenarios]
        monster_rarity_threshold = random.uniform(0.1, 1)
        available_monsters = [
            monster for monster in monsters if monster["rarity"] >= monster_rarity_threshold]

        if not available_monsters:
            # Use all monsters if none available for the selected rarity threshold
            available_monsters = monsters

        monster = random.choice(available_monsters)

        is_successful = random.random() <= monster["success_rate"]

        emoji_id = re.search(r'(?<=:)\d+', monster["emoji"]).group(0)
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"

        if is_successful:
            user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
            cash = monster["value"] * random.randint(5, 10)
            await user_data.add_balance(cash)
            scenario = random.choice(success_list)
            outcome = random.choice(adv_success_strings)
            scenario_text = scenario[0].format(author, monster["emoji"])
            outcome = " " + \
                      outcome.format(
                          author, monster["emoji"]) + f" you earned ${cash}!"
            check_loot = maybe_loot()
            if check_loot is not None:
                item = check_loot
                owned_item = user_data.get_item_by_key("name", item.get("name"), "items")
                if owned_item is not None:
                    owned_item["quantity"] += 1
                    await user_data.set_item_by_key("name", item.get("name"), owned_item, "items")
                else:
                    item["quantity"] = 1
                    await user_data.set_item_by_key("name", item.get("name"), item, "items")
                outcome += f"\nYou also found a {check_loot.get('rarity')} {item.get('emote')} {item.get('name')}!"
        else:
            scenario = random.choice(fail_list)
            scenario_text = scenario[0].format(author, monster["emoji"])
            outcome = random.choice(adv_failure_strings).format(
                author, monster["emoji"])

        em = discord.Embed(color=user_color,
                           title=f"{user}'s adventure!",
                           description=scenario_text + outcome)
        em.set_thumbnail(url=emoji_url)
        em.set_author(
            name="Adventure",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")

        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')

        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.send(embed=em)

    # chop command
    @commands.hybrid_command(name="chop", description="Go chopping!")
    @persistent_cooldown(1, 120, commands.BucketType.user)
    @commands.guild_only()
    async def chop(self, ctx):
        chosen_resource = \
            random.choices(list(chop_resource_info.keys()),
                           weights=[info['rarity'] for info in chop_resource_info.values()], k=1)[0]
        resource = chop_resource_info[chosen_resource]
        resource_amount = random.randint(1, 5)
        resource_value = random.randint(resource['min_value'], resource['max_value'])

        user_id = ctx.author.id
        user_data = await ctx.bot.db_client.get_user(user_id=user_id, guild_id=ctx.guild.id)
        user_balance = user_data.balance
        msg = (f"You chopped x{resource_amount} {resource['emote']} {chosen_resource} "
               f"worth ${resource_value}!, "
               f"you now have ${user_balance + resource_value * resource_amount}!")
        if user_data.equipped_items.get("Axe"):
            item_data = user_data.equipped_items.get("Axe")
            resource_amount *= item_data.get("multiplier")
            resource_amount = int(resource_amount)
            msg = (f"Using your {item_data.get('emote')}{item_data.get('name')}"
                   f"\nYou chopped x{resource_amount} {resource['emote']} {chosen_resource} worth ${resource_value}"
                   f"\nYou now have ${user_balance + resource_value * resource_amount}!"
                   f"\nYour axe has {item_data.get('durability') - 1} durability left!")
            item_data.get("durability") - 1
            if item_data.get("durability") <= 0:
                await user_data.remove_item("Axe")
                await ctx.send("Your axe broke!")
            await user_data.update_fields(equipped_items=user_data.equipped_items)
        await user_data.add_balance(resource_value * resource_amount)
        color = await generate_embed_color(ctx.author)

        em = discord.Embed(title="You chopped some resources!",
                           description=msg,
                           color=color)
        em.set_author(
            name="Chop Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.reply(embed=em)

    # mining command
    @commands.hybrid_command(name="mine", description="Go mining!")
    @persistent_cooldown(1, 120, commands.BucketType.user)
    @commands.guild_only()
    async def mine(self, ctx):
        chosen_resource = \
            random.choices(list(mine_resource_info.keys()),
                           weights=[info['rarity']
                                    for info in mine_resource_info.values()],
                           k=1)[0]
        resource = mine_resource_info[chosen_resource]
        resource_amount = random.randint(1, 10)
        resource_value = random.randint(
            resource['min_value'], resource['max_value'])

        user_id = ctx.author.id
        user_data = await ctx.bot.db_client.get_user(user_id=user_id, guild_id=ctx.guild.id)
        user_balance = user_data.balance
        await user_data.add_balance(resource_value * resource_amount)
        color = await generate_embed_color(ctx.author)
        em = discord.Embed(title="You mined some resources!",
                           description=f"You mined x{resource_amount} {resource['emote']} {chosen_resource} worth ${resource_value}! You now have ${user_balance + resource_value}!",
                           color=color)
        em.set_author(
            name="Mine Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.reply(embed=em)

    # Fishing command
    @commands.hybrid_command(name="fish", description="Go fishing!")
    @persistent_cooldown(1, 120, commands.BucketType.user)
    @commands.guild_only()
    async def fish(self, ctx):
        fish_name = random.choice(list(fish_info.keys()))
        fish_value = random.randint(10, 100)

        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        user_balance = user_data.balance
        await user_data.add_balance(fish_value)
        color = await generate_embed_color(ctx.author)

        em = discord.Embed(title="You caught a fish!",
                           description=f"You caught a {fish_info[fish_name]} {fish_name} worth ${fish_value}!, you now have ${user_balance + fish_value} gold!",
                           color=color)
        em.set_author(
            name="Fish Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="daily", description="Get your daily coins!.")
    @persistent_cooldown(1, 86400, commands.BucketType.user)
    @app_commands.describe(user="The user to give your daily to.")
    @commands.guild_only()
    async def daily(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        user_color = await generate_embed_color(user)
        author_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        streak_broken, daily_streak = await author_data.claim_daily()
        if not streak_broken:
            claimed_money = 1000 + 100 * min(daily_streak, 50)
        else:
            claimed_money = 1000

        if user.id == ctx.author.id:
            description = f"Daily: + ${claimed_money}"
            if claimed_money > 1000:
                description = f"Daily: + ${claimed_money} (Streak: {daily_streak})"
            em = discord.Embed(
                color=user_color, title=f"{ctx.author}'s daily", description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        else:
            description = "\nGifted Currency: +$100"
            claimed_money += 100
            if claimed_money > 1100:
                description = f"Gifted: + ${claimed_money} (Streak: {daily_streak})"
            em = discord.Embed(color=user_color,
                               title=f"{ctx.author} has given {user} their daily, plus a bonus!",
                               description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        roles = await self.bot.db_client.get_cash_roles(guild_id=ctx.guild.id)
        bonus_roles = []
        for role_data in roles:
            if role_data["_id"] in [r.id for r in user.roles]:
                role = ctx.guild.get_role(int(role_data.get('_id')))
                claimed_money += role_data["cash"]
                bonus_roles.append(f"{role.mention} + ${role_data['cash']}")
        if bonus_roles:
            em.add_field(name=f"Bonus", value="\n".join(bonus_roles), inline=False)
        em.add_field(name="Amount Added", value=f"${claimed_money}")
        em.add_field(name="New Balance",
                     value=f"{user_data.balance + claimed_money}")
        if streak_broken:
            em.add_field(name="Streak Broken!",
                         value=f"You broke your daily streak of {daily_streak} days!")

        em.set_author(
            name="Daily Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )

        await user_data.add_balance(claimed_money)
        view = Reminder(timeout=30)
        view.author = ctx.author
        view.bot = ctx.bot
        view.seconds = 86400
        view.type = "daily"
        message = await ctx.reply(embed=em, view=view)
        view.message = message

    @commands.hybrid_command(name="weekly", description="Get your weekly coins!.")
    @persistent_cooldown(1, 604800, commands.BucketType.user)
    @app_commands.describe(user="The user to give your weekly to.")
    @commands.guild_only()
    async def weekly(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        user_color = await generate_embed_color(user)

        money = 10000
        newbal = user_data.balance + money

        if user.id == ctx.author.id:
            description = f"Weekly: + ${money}"
            em = discord.Embed(
                color=user_color, title=f"{ctx.author}'s weekly", description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        else:
            description = "\nGifted Currency: +$1000"
            em = discord.Embed(color=user_color,
                               title=f"{ctx.author} has given {user} their weekly, plus a bonus!",
                               description=description)
            em.set_thumbnail(url=user.display_avatar.with_static_format("png"))

        em.add_field(name="Amount Added", value=f"${money}")
        em.add_field(name="New Balance", value=f"${newbal}")

        await user_data.add_balance(money)
        em.set_author(
            name="Weekly Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        view = Reminder(timeout=30)
        view.author = ctx.author
        view.bot = ctx.bot
        view.seconds = 604800
        view.type = "weekly"
        message = await ctx.reply(embed=em, view=view)
        view.message = message

    @commands.hybrid_command(name="work", description="get a job")
    @persistent_cooldown(1, 3600, commands.BucketType.user)
    @commands.guild_only()
    async def work(self, ctx):
        random.shuffle(job_descriptions)
        job = random.choice(job_descriptions)
        cash = random.randint(20, 250)
        job = job.replace("{0}", ctx.author.mention)
        user_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if user_data.is_in_jail():
            release_time = user_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(release_time, style="R"
                                                          )
            return await ctx.send(
                f"Look at you all handcuffed and shit, you'll get out of those {remaining_timestamp}")
        new_bal = user_data.balance + cash
        description = f"{job}\n\nCash: + ${cash}"
        em = discord.Embed(color=discord.Color.random(),
                           title=f"{ctx.author}'s job", description=description)
        em.set_thumbnail(
            url=ctx.author.display_avatar.with_static_format("png"))
        em.add_field(name="New Balance", value=f"${new_bal}")
        await user_data.add_balance(cash)
        em.set_author(
            name="Work Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        view = Reminder(timeout=30)
        view.author = ctx.author
        view.bot = ctx.bot
        view.seconds = 3600
        view.type = "work"
        message = await ctx.reply(embed=em, view=view)
        view.message = message


async def setup(bot):
    await bot.add_cog(Currency(bot))
