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
                             subtraction_percentage, calculate_remaining_xp, search, get_title)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_name_or_unknown(self, key, data):
        user_id = data.get(key)
        if user_id is None:
            return "Unknown"
        try:
            user = await self.bot.fetch_user(int(user_id))
            return user.display_name if user is not None else "Unknown"
        except Exception:
            return "Unknown"

    @commands.hybrid_command(name="bail", description="get you or someone else out of jail")
    @app_commands.describe(user="User to bailout")
    @commands.guild_only()
    async def bail(self, ctx, user: Optional[discord.Member]):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        user_color = await generate_embed_color(user)
        if not user_data.is_in_jail():
            return await ctx.reply(f":x: {user.mention} is not in jail.")
        user_balance = max(user_data.balance + user_data.bank_balance, 0)
        cost = user_data.jail.get("fine", 0)
        # TODO add higher fine for longer jail time
        cost_total = subtraction_percentage(user_balance, 90) + cost
        if user != ctx.author:
            author_data = await ctx.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
            if author_data.balance < cost_total:
                return await ctx.reply(f":x: {ctx.author.mention} needs ${cost_total} to bail out {user.mention}.")
            await author_data.subtract_balance(cost_total)
        else:
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
    @commands.guild_only()
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
        em.add_field(name="Balance", value=f"{user_data.balance:,}")
        em.add_field(name="Bank Balance", value=f"{user_data.bank_balance:,}")
        em.add_field(name="Total Balance", value=f"{user_data.balance + user_data.bank_balance:,}")
        if user_data.equipped_items:
            msg = ""
            for k, v in user_data.equipped_items.items():
                msg += f"{k}: {v.get('rarity')} {v.get('emote')} {v.get('name')}\n"
                msg += f"{v.get('description')}\n\n"
            em.add_field(name="Equipped Items", value=msg, inline=False)
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
    @commands.guild_only()
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
    @commands.guild_only()
    async def leaderboard(self, ctx):
        await ctx.send("Please use a valid subcommand: `level` or `balance`.")

    @leaderboard.command(name="summary", aliases=["sum"], description="View the leaderboard summary.")
    async def leaderboard_summary(self, ctx):
        await ctx.defer()
        ranks = ['🥇', '🥈', '🥉']

        def format_member_name(user_id, default="Member Left?"):
            member = ctx.guild.get_member(user_id)
            return member.name if member else default

        def format_leaderboard_data(users_data, formatter, key):
            s = '$'
            formatted_data = []
            if key == 'level':
                s = ''
            for index, user_data in enumerate(users_data):
                formatted_data.append(
                    f"{ranks[index]} **{format_member_name(user_data.user_id)}** - {s}{user_data[key]:,}")

            return "\n".join(formatted_data)

        top_users_balance = await self.bot.db_client.get_top_users(
            limit=3, guild_id=ctx.guild.id, sort_key=lambda user: user.balance)
        top_users_level = await self.bot.db_client.get_top_users(
            limit=3, guild_id=ctx.guild.id, sort_key=lambda user: user.level)
        top_users_bank_balance = await self.bot.db_client.get_top_users(
            limit=3, guild_id=ctx.guild.id, sort_key=lambda user: user.bank_balance)
        guild_data = await self.bot.db_client.get_guild(guild_id=ctx.guild.id)
        all_waifus = guild_data.waifus
        sorted_data = sorted(all_waifus, key=lambda x: x['value'], reverse=True)
        top_users_waifu = sorted_data[:3]

        top_balance = format_leaderboard_data(top_users_balance, lambda user: user.balance, 'balance')
        top_level = format_leaderboard_data(top_users_level, lambda user: user.level, 'level')
        top_bank_balance = format_leaderboard_data(top_users_bank_balance, lambda user: user.bank_balance, 'bank_balance')
        top_waifus = []
        for index, waifu in enumerate(top_users_waifu):
            top_waifus.append(f"{ranks[index]} **{format_member_name(int(waifu['user_id']))}** - ${waifu['value']:,}")

        em = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard Summary", color=discord.Color.blurple())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Leaderboard Summary Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        em.add_field(name="Top Balance", value=top_balance if top_balance else 'Not enough data', inline=True)
        em.add_field(name="Top Level", value=top_level if top_level else 'Not enough data', inline=True)
        em.add_field(name="Top Bank Balance", value=top_bank_balance if top_bank_balance else 'Not enough data',
                     inline=True)
        em.add_field(name="Top Waifu", value="\n".join(top_waifus) if top_waifus else 'Not enough data', inline=True)
        await ctx.reply(embed=em)

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
        top_users = await self.bot.db_client.get_top_users(
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

    @leaderboard.command(name="waifu", description="waifu leaderboard")
    async def waifu_leaderboard(self, ctx):
        await ctx.typing(ephemeral=False)
        guild_data = await self.bot.db_client.get_guild(guild_id=ctx.guild.id)
        all_waifus = guild_data.waifus
        # Sort the list of dictionaries by the 'value' field
        sorted_data = sorted(all_waifus, key=lambda x: x['value'], reverse=True)

        # Create an empty list for embeds
        embeds = []
        # Initialize an empty string to accumulate entries
        page_entries = ""
        for index, waifu in enumerate(sorted_data, start=1):
            print(waifu)
            if not waifu["user_id"]:
                guild_data.waifus.remove(waifu)
                await ctx.bot.db_client.update_guild(ctx.guild.id, {"waifus": guild_data.waifus})
                continue
            user = ctx.guild.get_member(int(waifu["user_id"]))
            user_name = user.display_name if user else "No user found, left?"
            if not waifu["owner_id"]:
                entry = f"**#{index}** - <:money:1163891159349866526> ${waifu['value']:,}\n" \
                        f"**{user_name}** is unclaimed\n"
                page_entries += entry
                continue
            owner = ctx.guild.get_member(int(waifu["owner_id"]))
            owner_name = owner.display_name if owner else "No owner, left?"
            entry = f"**#{index}** - <:money:1163891159349866526> ${waifu['value']:,}\n" \
                    f"**{user_name}** claimed by **{owner_name}**\n"
            if not waifu["affinity"]:
                entry += f"but **{user_name}'s** heart is empty 💔\n\n"
            elif waifu["affinity"] == waifu["owner_id"]:
                entry += f"and **{user_name}** likes **{owner_name}** too ❤️\n\n"
            else:
                affinity_user = ctx.guild.get_member(int(waifu["affinity"]))
                affinity_user_name = affinity_user.display_name if affinity_user else "No affinity user, left?"
                entry += f"but **{user}** likes **{affinity_user_name}** 💔\n\n"
            page_entries += entry
            # Create a new embed after accumulating 10 entries or at the end
            if index % 10 == 0 or index == len(sorted_data):
                em = discord.Embed(title=f"Top Waifus (Page {len(embeds) + 1})")
                em.description = page_entries
                em.set_author(
                    name="Waifu Leaderboard Command",
                    icon_url=self.bot.user.display_avatar.with_static_format("png"),
                    url="https://discord.gg/invite/tailss")
                timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
                em.set_footer(
                    text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                    icon_url=ctx.author.display_avatar.with_static_format("png"))
                embeds.append(em)
                # Reset page_entries for the next page
                page_entries = ""

        await Paginator(delete_on_timeout=False, timeout=120).start(ctx, pages=embeds)

    @commands.hybrid_group(name="inventory", description="inventory commands")
    @commands.guild_only()
    async def inventory(self, ctx):
        await ctx.send("Please use a valid subcommand: `view` or `use`.")

    @inventory.group(name="role", description="role inventory commands")
    async def inventory_role(self, ctx):
        await ctx.send("Please use a valid subcommand: `view` or `use`.")

    @inventory_role.command(name="view", description="view role inventory")
    async def inventory_role_view(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("roles"):
            return await ctx.reply(":x: You don't have any roles in your inventory.")
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
            return await ctx.reply(":x: You don't have any roles in your inventory.")
        for r in user_data.inventory.get("roles"):
            if str(r.get("_id")) == str(role):
                role_obj = ctx.guild.get_role(int(r.get("_id")))
                if role_obj:
                    if role_obj in ctx.author.roles:
                        await ctx.author.remove_roles(role_obj)
                        color = await generate_embed_color(ctx.author)
                        em = discord.Embed(title=f"", color=color)
                        em.description = f"{role_obj.mention} removed."
                        return await ctx.reply(embed=em)
                    else:
                        await ctx.author.add_roles(role_obj)
                        color = await generate_embed_color(ctx.author)
                        em = discord.Embed(title=f"", color=color)
                        em.description = f"{role_obj.mention} added."
                        return await ctx.reply(embed=em)
        return await ctx.reply("Role not found in inventory.")

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

    @inventory_role.command(name="give", description="give role")
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
                if str(role_data.get("_id")) in [str(role.id) for role in ctx.author.roles]:
                    await ctx.author.remove_roles(ctx.guild.get_role(int(role_data.get("_id"))))
                user_data.inventory.get("roles").remove(role_data)
                await user_data.update_fields(inventory=user_data.inventory)
                await user_two_data.set_item_by_key("_id", role_data.get('_id'), role_data, "roles")
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

    @inventory.group(name="gifts", description="gift commands")
    async def inventory_gift(self, ctx):
        await ctx.send("Please use a valid subcommand: `view` or `give`.")

    @inventory_gift.command(name="view", description="view gift inventory")
    async def inventory_gift_view(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("gifts"):
            return await ctx.reply(":x: You don't have any gifts in your inventory.")
        em = discord.Embed(title=f"{ctx.author}'s Gift Inventory", color=discord.Color.blurple())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Gift Inventory Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        for gift_data in user_data.inventory.get("gifts"):
            e = "➕" if gift_data.get("positive") else "➖"
            em.add_field(name="",
                         value=f"\nGift: {gift_data.get('name')} {gift_data.get('emote')}\nPrice: {gift_data.get('price'):,}\nValue: {e} {gift_data.get('value'):,}\nQuantity: {gift_data.get('quantity')}",
                         inline=False)
        await ctx.reply(embed=em)

    @inventory_gift.command(name="give", description="give gift")
    @app_commands.describe(waifu="waifu to give gift to")
    async def inventory_gift_give(self, ctx, gift: str, waifu: discord.Member, quantity: int = 1):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("gifts"):
            return await ctx.reply("You don't have any gifts in your inventory.")
        for gift_data in user_data.inventory.get("gifts"):
            if str(gift_data.get("_id")) == str(gift):
                print("found gift")
                if gift_data.get("quantity") < quantity:
                    return await ctx.reply("You don't have enough of that gift.")
                gift_data["quantity"] -= quantity
                if gift_data["quantity"] <= 0:
                    user_data.inventory.get("gifts").remove(gift_data)
                await user_data.update_fields(inventory=user_data.inventory)
                guild_data = await self.bot.db_client.get_guild(guild_id=ctx.guild.id)
                waifu_data = await guild_data.get_waifu(waifu.id)
                value = gift_data.get("value") * quantity
                if waifu_data["affinity"] == ctx.author.id:
                    value = int(value * 1.5)
                if gift_data.get("positive"):
                    waifu_data["value"] += value
                else:
                    waifu_data["value"] -= value
                gift_data["quantity"] = quantity
                if gift_data["_id"] in [gift.get("_id") for gift in waifu_data["gifts"]]:
                    for gift in waifu_data["gifts"]:
                        if gift["_id"] == gift_data["_id"]:
                            gift["quantity"] += quantity
                else:
                    waifu_data["gifts"].append(gift_data)
                await guild_data.update_waifu(waifu_data)
                e = "➕" if gift_data.get("positive") else "➖"
                return await ctx.reply(
                    f"{e} Gift: {quantity} {gift_data.get('name')}: {gift_data.get('emote')} given to {waifu.mention}")
        return await ctx.reply("Gift not found in inventory.")

    @inventory_gift_give.autocomplete('gift')
    async def give_gift_autocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        user_data = await self.bot.db_client.get_user(user_id=interaction.user.id, guild_id=interaction.guild.id)
        gifts = user_data.inventory.get("gifts")
        return [
                   app_commands.Choice(name=gift.get('name'), value=str(gift.get('_id')))
                   for gift in gifts
                   if not current or search(gift.get('name').lower(), current.lower())
               ][:25]

    @inventory.group(name="items", description="item commands")
    async def inventory_item(self, ctx):
        await ctx.send("Please use a valid subcommand: `view` or `use`.")

    @inventory_item.command(name="view", description="view item inventory")
    async def inventory_item_view(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("items"):
            return await ctx.reply(":x: You don't have any items in your inventory.")
        em = discord.Embed(title=f"{ctx.author}'s Item Inventory", color=discord.Color.blurple())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Item Inventory Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        for item_data in user_data.inventory.get("items"):
            em.add_field(name=item_data.get("name"), value=f"{item_data.get('description')}")
        await ctx.reply(embed=em)

    @inventory_item.command(name="use", description="use item")
    @app_commands.describe(item="item to use")
    async def inventory_item_use(self, ctx, item: str):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("items"):
            return await ctx.reply("You don't have any items in your inventory.")
        # TODO temp
        return await ctx.reply("You don't have any items in your inventory.")

    @inventory_item.command(name="equip", description="equip item")
    @app_commands.describe(item="item to equip")
    async def inventory_item_equip(self, ctx, item: str):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if not user_data.inventory.get("items"):
            return await ctx.reply("You don't have any items in your inventory.")
        item_data = [i for i in user_data.inventory.get("items") if i.get("name") == item]
        if not item_data:
            return await ctx.reply("Item not found in inventory.")
        item_data = item_data[0]
        if not item_data.get("equippable"):
            return await ctx.reply("Item is not equippable.")
        equipped = user_data.equipped_items.get(item_data.get('type'))
        if equipped:
            return await ctx.reply("You already have an item equipped in that slot.")
        user_data.equipped_items[item_data.get('type')] = item_data
        await user_data.update_fields(equipped_items=user_data.equipped_items)
        if item_data.get("quantity") > 1:
            item_data["quantity"] -= 1
            await user_data.update_fields(inventory=user_data.inventory)
        else:
            user_data.inventory.get("items").remove(item_data)
            await user_data.update_fields(inventory=user_data.inventory)
        return await ctx.reply(f"{item_data.get('emote')} {item_data.get('name')} equipped.")

    @inventory_item_equip.autocomplete('item')
    async def equip_item_autocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        user_data = await self.bot.db_client.get_user(user_id=interaction.user.id, guild_id=interaction.guild.id)
        items = user_data.inventory.get("items")
        items = [item for item in items if item.get("equippable")]
        return [
                   app_commands.Choice(name=item.get('name'), value=str(item.get('name')))
                   for item in items
                   if not current or search(item.get('name').lower(), current.lower())
               ][:25]

    @inventory_item.command(name="unequip", description="unequip item")
    @app_commands.describe(item_type="type of item to unequip")
    async def inventory_item_unequip(self, ctx, item_type: str):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)

        # Check if the user has equipped items
        if not user_data.equipped_items.get(item_type):
            return await ctx.reply(f"You don't have any item equipped in the {item_type} slot.")

        # Retrieve the equipped item data
        unequipped_item = user_data.equipped_items.pop(item_type)

        # Add the unequipped item back to inventory
        inventory_items = user_data.inventory.get("items", [])
        matching_item = next((i for i in inventory_items if i.get("name") == unequipped_item["name"]), None)

        if matching_item:
            matching_item["quantity"] += 1
        else:
            inventory_items.append({**unequipped_item, "quantity": 1})

        # Update user data
        user_data.inventory["items"] = inventory_items
        await user_data.update_fields(equipped_items=user_data.equipped_items, inventory=user_data.inventory)

        return await ctx.reply(f"{unequipped_item.get('emote')} {unequipped_item.get('name')} unequipped.")

    @inventory_item_unequip.autocomplete('item_type')
    async def unequip_item_autocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        user_data = await self.bot.db_client.get_user(user_id=interaction.user.id, guild_id=interaction.guild.id)
        equipped_items = user_data.equipped_items

        return [
                   app_commands.Choice(name=slot, value=slot)
                   for slot in equipped_items.keys()
                   if not current or slot.lower().startswith(current.lower())
               ][:25]

    @commands.hybrid_group(name="waifu", description="waifu commands")
    @commands.guild_only()
    async def waifu(self, ctx):
        await ctx.send("Please use a valid subcommand")

    @waifu.command(name="claim", description="claim waifu")
    @app_commands.describe(waifu="Waifu to claim")
    async def waifu_claim(self, ctx, waifu: discord.Member, value: int):
        await ctx.typing(ephemeral=False)
        new_value = value
        if waifu.id == ctx.author.id:
            return await ctx.reply("You can't claim yourself, wtf is wrong with you?")
        guild_data = await self.bot.db_client.get_guild(guild_id=ctx.guild.id)
        waifu_data = await guild_data.get_waifu(waifu.id)
        if waifu_data and str(waifu_data["owner_id"]) == str(ctx.author.id):
            return await ctx.reply("You already own that waifu! Raise their value by giving them gifts!")
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if user_data.balance < value:
            return await ctx.reply("You don't have enough coins to claim that waifu.")
        if waifu_data["owner_id"]:
            if waifu_data['value'] * 1.10 > value:
                return await ctx.reply(f"That waifu is worth {int(waifu_data['value'] * 1.10) + 1:,}, try again.")
        if waifu_data['value'] > value:
            return await ctx.reply("That waifu is worth more than that.")
        if str(waifu_data["affinity"]) == str(ctx.author.id):
            new_value = int(value * 1.5)
        stolen = await guild_data.get_waifu(waifu_data['owner_id'])
        if waifu.id in stolen["claimed"]:
            stolen["claimed"].remove(waifu.id)
            await guild_data.update_waifu(stolen)
        waifu_data["owner_id"] = ctx.author.id
        waifu_data["value"] = new_value
        await guild_data.update_waifu(waifu_data)
        self_waifu = await guild_data.get_waifu(ctx.author.id)
        self_waifu["claimed"].append(waifu.id)
        await guild_data.update_waifu(self_waifu)
        await user_data.subtract_balance(value)
        await ctx.reply(f"You claimed {waifu.mention} for ${value}.")

    @waifu.command(name="set_affinity", description="set affinity")
    @app_commands.describe(waifu="Waifu to set affinity")
    async def waifu_set_affinity(self, ctx, waifu: discord.Member):
        await ctx.typing(ephemeral=False)
        guild_data = await self.bot.db_client.get_guild(guild_id=ctx.guild.id)
        waifu_data = await guild_data.get_waifu(ctx.author.id)
        waifu_data["affinity"] = waifu.id
        waifu_data["affinity_changes"] += 1
        await guild_data.update_waifu(waifu_data)
        return await ctx.reply(f"You set {waifu.mention} as your affinity.")

    @waifu.command(name="divorce", description="divorce waifu")
    @app_commands.describe(waifu="Waifu to divorce")
    async def waifu_divorce(self, ctx, waifu: discord.Member):
        await ctx.typing(ephemeral=False)
        guild_data = await self.bot.db_client.get_guild(guild_id=ctx.guild.id)
        waifu_data = await guild_data.get_waifu(waifu.id)
        if str(waifu_data.get("owner_id", 0)) != str(ctx.author.id):
            return await ctx.reply("You don't own that waifu.")
        waifu_data["owner_id"] = None
        await guild_data.update_waifu(waifu_data)
        self_waifu = await guild_data.get_waifu(ctx.author.id)
        self_waifu["claimed"].remove(waifu.id)
        self_waifu["divorce_count"] += 1
        await guild_data.update_waifu(self_waifu)
        return await ctx.reply(f"You divorced {waifu.mention}.")

    @waifu.command(name="info", description="waifu info")
    @app_commands.describe(waifu="Waifu to get info of")
    async def waifu_info(self, ctx, waifu: Optional[discord.Member]):
        max_names = 10
        waifu = waifu or ctx.author
        guild_data = await self.bot.db_client.get_guild(guild_id=ctx.guild.id)
        waifu_data = await guild_data.get_waifu(waifu.id)
        all_waifus = guild_data.waifus
        price = int(waifu_data.get("value") * 1.10)
        value = waifu_data.get("value")

        liked_by = [await self.get_name_or_unknown("claimed", {"claimed": w.get("user_id")})
                    for w in all_waifus if str(w.get("affinity")) == str(waifu.id)]

        formatted_liked_by = "\n".join(liked_by[:max_names])

        if len(liked_by) > max_names:
            remaining_names = len(liked_by) - max_names
            formatted_liked_by += f"...and {remaining_names} more."

        claimed_names = [await self.get_name_or_unknown("claimed", {"claimed": claim})
                         for claim in waifu_data.get("claimed", [])]

        formatted_claimed_names = "\n".join(claimed_names[:max_names])

        if len(claimed_names) > max_names:
            remaining_names = len(claimed_names) - max_names
            formatted_claimed_names += f"...and {remaining_names} more."

        if len(claimed_names) == 0:
            formatted_claimed_names = "No one :("

        if len(liked_by) == 0:
            formatted_liked_by = "No one :("

        plus_gifts = [gift for gift in waifu_data.get("gifts") if gift.get("positive")]
        minus_gifts = [gift for gift in waifu_data.get("gifts") if not gift.get("positive")]

        plus_gifts_str = [f"{gift.get('emote')}x{gift.get('quantity')}" for gift in plus_gifts]
        plus_gifts_list = [plus_gifts_str[i:i + 4] for i in range(0, len(plus_gifts_str), 4)]
        minus_gifts_str = [f"{gift.get('emote')}x{gift.get('quantity')}" for gift in minus_gifts]
        minus_gifts_list = [minus_gifts_str[i:i + 4] for i in range(0, len(minus_gifts_str), 4)]
        plus_gifts_value = '\n'.join([' '.join(line) for line in plus_gifts_list]) if plus_gifts_list else "No gifts"
        minus_gifts_value = '\n'.join([' '.join(line) for line in minus_gifts_list]) if minus_gifts_list else "No gifts"

        claim_title = get_title(rank=len(waifu_data.get("claimed")), title_type="claim") or ""
        divorce_title = get_title(rank=waifu_data.get("divorce_count"), title_type="divorce") or ""
        affinity_title = get_title(rank=waifu_data.get("affinity_changes"), title_type="affinity") or ""

        owner_name = await self.get_name_or_unknown("owner_id", waifu_data) if waifu_data.get(
            "owner_id") else "Nobody..."
        likes = await self.get_name_or_unknown("affinity", waifu_data) if waifu_data.get(
            "affinity") else "Nobody..."

        em = discord.Embed(title=f"Info for Waifu {waifu.display_name} {claim_title}", color=discord.Color.blurple())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Waifu Info Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        em.set_thumbnail(url=waifu.display_avatar.with_static_format("png"))
        em.add_field(name="<:black_hearts_padlock:1163891156392878182> **Owner**", value=f"{owner_name}")
        em.add_field(name="<:master:1163888867192078356> **Likes**", value=f"{likes}")
        em.add_field(name="<a:1bye_money_r_ateez:1163891153796616242> **Price**", value=f"${price:,}", inline=False)
        em.add_field(name="<:money:1163891159349866526> **Value**", value=f"${value:,}", inline=False)
        em.add_field(name="<:Gift:1163891158137700492> **Gifts** ➕:", value=f"{plus_gifts_value}")
        em.add_field(name="<a:explode2:1163902836300591175> **Gifts** ➖:", value=f"{minus_gifts_value}")
        em.add_field(name="<:apink_hearts:1163891155285594212> **Liked By**", value=f"{formatted_liked_by}",
                     inline=False)
        em.add_field(name="<:handcuffs:1163892821036646534> **Claimed**", value=f"{formatted_claimed_names}",
                     inline=False)
        em.add_field(name="<a:divorce:1163891160192921671> **Divorces**",
                     value=f"{divorce_title} {waifu_data.get('divorce_count')}", inline=False)
        em.add_field(name="💌 **Affinity Changes**", value=f"{affinity_title} {waifu_data.get('affinity_changes')}",
                     inline=False)
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Profile(bot))
