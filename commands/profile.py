import datetime
from io import BytesIO
from typing import Optional, List

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
                             subtraction_percentage, calculate_remaining_xp, search)


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
        # await user_data.update_user({"jail": {}})
        await user_data.update_fields(jail={})
        em = discord.Embed(title=f"{user}'s Bail",
                           description=f":white_check_mark: {user.mention} has been released from jail for {cost_total}.",
                           colour=user_color)
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
        # user_data = await ctx.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        user_data = await self.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        user_color = await generate_embed_color(user)
        remain, total = calculate_remaining_xp(user_data.xp)
        print(f'{remain} {total}')
        bar = progress_percentage(remain=user_data.xp, total=total)

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
        em.add_field(name="Experience", value=f"{user_data.xp} / {total}")
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
        user_data: User = await self.bot.db_client.get_user(guild_id=ctx.guild.id, user_id=user.id)

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
        top_users = await self.bot.db_client.get_top_users(limit=200, guild_id=ctx.guild.id,
                                                           sort_key=lambda user: user.level)

        guild = ctx.guild

        sorted_users = []
        for user in top_users:
            member = ctx.guild.get_member(user.user_id)
            if member:
                sorted_users.append((user, member))

        sorted_users.sort(key=lambda entry: entry[0].level, reverse=True)

        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Levels: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)

    @leaderboard.command(name="balance", aliases=["bal"], description="View the balance leaderboard.")
    async def leaderboard_balance(self, ctx):
        await ctx.typing()
        top_users = await self.bot.db_client.get_top_users(
            limit=200, guild_id=ctx.guild.id, sort_key=lambda user: user.balance)
        guild = ctx.guild
        sorted_users = []
        for user_data in top_users:
            user = user_data
            member = ctx.guild.get_member(user.user_id)
            if member:
                sorted_users.append((user, member))

        sorted_users.sort(key=lambda entry: entry[0].balance, reverse=True)
        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Balance: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)

    @leaderboard.command(name="bank", description="View the bank balance leaderboard.")
    async def leaderboard__bank_balance(self, ctx):
        await ctx.defer()
        top_users = await self.bot.db_client.get_top_users(
            limit=200, guild_id=ctx.guild.id, sort_key=lambda user: user.bank_balance)

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
        top_users = top_users_by_balance = await self.bot.db_client.get_top_users(
            limit=200, guild_id=ctx.guild.id, sort_key=lambda user: user.balance + user.bank_balance)
        guild = ctx.guild
        sorted_users = []
        for user_data in top_users:
            user = user_data
            member = ctx.guild.get_member(user.user_id)

            if member:
                sorted_users.append((user, member))

        sorted_users.sort(
            key=lambda entry: entry[0].balance + entry[0].bank_balance, reverse=True)
        pages = create_leaderboard_pages(
            sorted_users, "Leaderboard - Total Balance: Page")
        await Paginator(delete_on_timeout=True, timeout=120).start(ctx, pages=pages)

    @commands.hybrid_group(name="inventory", description="inventory commands")
    async def inventory(self, ctx):
        await ctx.send("Please use a valid subcommand: `view` or `use`.")

    @inventory.group(name="role", description="role inventory commands")
    async def inventory_role(self, ctx):
        await ctx.send("Please use a valid subcommand: `view` or `use`.")

    @inventory_role.command(name="view", description="view role inventory")
    async def inventory_role_view(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("roles"):
            return await ctx.reply("You don't have any roles in your inventory.")
        em = discord.Embed(title=f"{ctx.author}'s Role Inventory", color=discord.Color.blurple())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Role Inventory Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        for role in user_data.inventory.get("roles"):
            role_obj = ctx.guild.get_role(int(role.get("_id")))
            if role_obj:
                em.add_field(name=role_obj.name, value=f"{role_obj.mention} {role.get('description')}")
        await ctx.reply(embed=em)

    @inventory_role.command(name="toggle", description="toggle role")
    async def inventory_role_toggle(self, ctx, role: str):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("roles"):
            return await ctx.reply("You don't have any roles in your inventory.")
        for role in user_data.inventory.get("roles"):
            role_obj = ctx.guild.get_role(int(role.get("_id")))
            if role_obj:
                if role_obj in ctx.author.roles:
                    await ctx.author.remove_roles(role_obj)
                    return await ctx.reply(f"{role_obj.mention} removed.")
                else:
                    await ctx.author.add_roles(role_obj)
                    return await ctx.reply(f"{role_obj.mention} added.")
        await ctx.reply("Roles removed.")

    @inventory_role_toggle.autocomplete('role')
    async def toggle_role_autocomplete(self,
                                       interaction: discord.Interaction,
                                       current: str,
                                       ) -> List[app_commands.Choice[str]]:

        user_data = await self.bot.db_client.get_user(user_id=interaction.user.id, guild_id=interaction.guild.id)
        roles = user_data.inventory.get("roles")

        return [
                   app_commands.Choice(name=role.get('name'), value=str(role.get('_id')))
                   for role in roles
                   if not current or search(role.get('name').lower(), current.lower())
               ][:25]

    @inventory_role.command(name="give_role", description="give role")
    @app_commands.describe(user="User to give role to")
    async def inventory_role_give_role(self, ctx, role: str, user: discord.Member):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("roles"):
            return await ctx.reply("You don't have any roles in your inventory.")
        for role_data in user_data.inventory.get("roles"):
            if str(role_data.get("_id")) == str(role):
                print("found role")
                user_two_data = await self.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
                for role_data_two in user_two_data.inventory.get("roles", []):
                    if role_data_two.get("_id") == role:
                        return await ctx.reply("User already has role.")
                if role_data.get("_id") in [str(role.id) for role in ctx.author.roles]:
                    await ctx.author.remove_roles(ctx.guild.get_role(int(role_data.get("_id"))))
                user_data.inventory.get("roles").remove(role_data)
                await user_data.update_fields(inventory=user_data.inventory)
                user_two_data.inventory.get("roles", []).append(role_data)
                await user_two_data.update_fields(inventory=user_two_data.inventory)
                return await ctx.reply(f"{role_data.get('name')} given to {user.mention}")
        return await ctx.reply("Role not found in inventory.")

    @inventory_role_give_role.autocomplete('role')
    async def give_role_autocomplete(self,
                                     interaction: discord.Interaction,
                                     current: str,
                                     ) -> List[app_commands.Choice[str]]:

        user_data = await self.bot.db_client.get_user(user_id=interaction.user.id, guild_id=interaction.guild.id)
        roles = user_data.inventory.get("roles")
        return [
                   app_commands.Choice(name=role.get('name'), value=str(role.get('_id')))
                   for role in roles
                   if not current or search(role.get('name').lower(), current.lower())
               ][:25]


async def setup(bot):
    await bot.add_cog(Profile(bot))
