import datetime
from io import BytesIO
from typing import Optional

import discord
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from discord import app_commands
from discord.ext import commands

from config.settings_config import create_leaderboard_pages
from database import User
from utils.paginator import Paginator
from utils.pillowutils import (arc_bar, font_auto_scale, get_brightness,
                               mask_ellipsis)
from utils.utilities import (generate_embed_color, progress_percentage,
                             subtraction_percentage)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="bail", description="get you or someone else out of jail")
    @app_commands.describe(user="User to bailout")
    async def bail(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        user_color = await generate_embed_color(user)
        if not user_data.is_in_jail():
            return await ctx.reply(f":x: {user.mention} is not in jail.")
        user_balance = max(user_data.balance + user_data.bank_balance, 0)
        cost = user_data.jail.get("fine", 0)
        # TODO add higher fine for longer jail time
        cost_total = subtraction_percentage(user_balance, 10) + cost
        if cost_total > user_data.balance:
            return await ctx.reply(f":x: {user.mention} needs ${cost_total} to get out of jail.")
        await user_data.subtract_balance(cost_total)
        #await user_data.update_user({"jail": {}})
        await user_data.update_fields(jail={})
        em = discord.Embed(title=f"{user}'s Bail", description=f":white_check_mark: {user.mention} has been released from jail for {cost_total}.", colour=user_color)
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Bail Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="profile", description="Look at your profile.")
    async def profile(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        #user_data = await ctx.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        user_color = await generate_embed_color(user)
        exp_needed = int(((user_data.level + 1) * 10) ** 2)
        bar = progress_percentage(user_data.xp, exp_needed)

        em = discord.Embed(title=f"{user}'s Profile", color=user_color)
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Profile Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
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

    @commands.hybrid_command(name="rank", description="Generate a rank card")
    @app_commands.describe(user="The user to get the rank card of.")
    @commands.guild_only()
    async def rank(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data: User = await self.bot.db_client.get_user(user.id, ctx.guild.id)

        user_level = user_data.level
        user_xp = user_data.xp
        max_xp = int(((user_data.level + 1) * 10) ** 2)

        # Load user avatar from URL and resize it
        target_size = 1024
        avatar_url = user.avatar.with_size(target_size).url
        image_bytes = await (await self.bot.web_client.get(avatar_url)).read()
        user_avatar = Image.open(BytesIO(image_bytes)) \
            .convert('RGBA') \
            .resize((target_size, target_size), resample=Image.LANCZOS)

        base = Image.new("RGBA", (600, 300))  # 300, 150
        filtered = user_avatar.copy().filter(ImageFilter.GaussianBlur(radius=10))
        base.paste(filtered, (-((user_avatar.width - base.width) // 2), -((user_avatar.height - base.height) // 2)),
                   user_avatar)

        mask_ellipsis(user_avatar)
        user_avatar = user_avatar.resize((220, 220), resample=Image.LANCZOS)
        base.paste(user_avatar, (20, 40), user_avatar)

        arc_bar(img=base, xy=(10, 30), size=(250, 270), progress_pc=100,
                width=10, fill=(255, 255, 255))

        arc_bar(img=base, xy=(10, 30), size=(250, 270), progress_pc=(user_xp / max_xp) * 100,
                width=10, fill=(0, 191, 255))

        brightness = get_brightness(base)
        text_fill, stroke_fill = ((255, 255, 255), (0, 0, 0)) if brightness <= 128 else ((0, 0, 0), (255, 255, 255))
        # Add text for XP and Balance
        text = f'Level: {user_level}\nEXP: {user_xp}/{max_xp}'
        font = ImageFont.truetype('circular-black.ttf', size=42)
        font = font_auto_scale(font, text, desired_width=305, size_max=42, size_min=20)

        draw = ImageDraw.Draw(base)
        draw.text((275, 150), text, fill=text_fill, font=font, anchor="lm", stroke_width=3, stroke_fill=stroke_fill)

        # Image is rendered at 2x resolution to produce a higher quality output
        # This is far better than rendering natively at 300, 150, as it'd look pixelated. Downsampling is better here.  
        base = base.resize((300, 150), resample=Image.LANCZOS)
        img_buffer = BytesIO()
        base.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Send the rank card to the user
        await ctx.send(file=discord.File(img_buffer, filename="rank_card.png"))

    @commands.hybrid_command(name="avatar", description="Look at someone's avatar.")
    @app_commands.describe(user="The user to get the avatar of.")
    async def avatar(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_color = await generate_embed_color(user)
        em = discord.Embed(title=f"{user}'s Avatar", color=user_color)
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Avatar Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        em.set_thumbnail(url=user.display_avatar.with_static_format("png"))
        em.set_image(url=user.display_avatar.with_static_format("png"))
        await ctx.reply(embed=em)

    @commands.hybrid_group(name="leaderboard", aliases=["lb"], description="View the leaderboard.")
    async def leaderboard(self, ctx):
        await ctx.send("Please use a valid subcommand: `level` or `balance`.")

    @leaderboard.command(name="level", aliases=["lvl"], description="View the level leaderboard.")
    async def leaderboard_level(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_level(limit=200, guild_id=ctx.guild.id)

        guild = ctx.guild

        sorted_users = []
        for user_data in top_users:
            # Provide a default value for 'jail' attribute
            user_data.setdefault("jail", {})
            user_data.pop("health", None)
            user = User(self.bot.db_client, **user_data)
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
            limit=200, guild_id=ctx.guild.id)

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
            limit=200, guild_id=ctx.guild.id)

        guild = ctx.guild
        sorted_users = []
        for user_data in top_users:
            user = user_data
            member = ctx.guild.get_member(user.user_id)

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(
            key=lambda entry: entry[0].bank_balance, reverse=True)
        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Bank Balance: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)

    @leaderboard.command(name="total", aliases=["net"], description="View the total balance leaderboard.")
    async def leaderboard_combined(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users_by_combined_balance(
            limit=200, guild_id=ctx.guild.id)

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
