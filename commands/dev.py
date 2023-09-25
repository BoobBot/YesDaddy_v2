import contextlib
import datetime
import inspect
import io
import math
import os
import re
import subprocess
import sys
import textwrap
import traceback
from collections import Counter
from io import BytesIO
from typing import Literal, Optional, Tuple, Union

import discord
import psutil
from discord.ext import commands
from discord.ext.commands import Context, Greedy
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from database.user_entry import User
from views import support_channel_view
from views.rule_button_view import RuleButton
from views.verification_view import VerificationView


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def load(self, ctx, cog):
        try:
            await self.bot.load_extension(f'{cog}')
            await ctx.send(f'{cog} has been loaded.')
        except Exception as e:
            await ctx.send(f'Error loading {cog}: {e}')


    @commands.command()
    async def reload(self, ctx, cog):
        try:
            await self.bot.reload_extension(f'{cog}')
            await ctx.send(f'{cog} has been reloaded.')
        except Exception as e:
            await ctx.send(f'Error reloading {cog}: {e}')


    @commands.command()
    async def unload(self, ctx, cog):
        try:
            await self.bot.unload_extension(f'cogs.{cog}')
            await ctx.send(f'{cog} has been unloaded.')
        except Exception as e:
            await ctx.send(f'Error unloading {cog}: {e}')

    @commands.command()
    async def reload_all(self, ctx):
        for cog in self.bot.cogs.copy():
            await self.bot.reload_extension(str(cog))
        await ctx.send('reloaded')

    def get_dominant(self, image, average = False):
        colour_bands = [0, 0, 0]

        if average:
            colour_tuple = [None, None, None]

            for channel in range(3):
                # Get data for one channel at a time
                pixels = image.getdata(band=channel)
                values = []
                for pixel in pixels:
                    values.append(pixel)
                colour_tuple[channel] = int(sum(values) / len(values))
            return tuple(colour_tuple)
        else:
            for band in range(3):
                pixels = image.getdata(band=band)
                c = Counter(pixels)
                colour_bands[band] = c.most_common(1)[0][0]

            return tuple(colour_bands)

    def get_brightness(self, image) -> int:
        """
        Returns an integer between 0-255
        """
        dom_col = self.get_dominant(image, average=True)
        return (dom_col[0] * 0.299) + (dom_col[1] * 0.587) + (dom_col[2] * 0.114)

    def mask_ellipsis(self, img: Image, offset: int = 0):
        img_mask = Image.new('L', img.size, 0)
        mask = ImageDraw.Draw(img_mask)
        mask.ellipse((offset, offset, img_mask.width - offset, img_mask.height - offset), fill=255)
        img.putalpha(img_mask)

    def arc_bar(self, img: Image, xy: Tuple[int, int], size: Tuple[int, int],
                progress_pc: int, width: int,
                fill: Union[Tuple[int, int, int], Tuple[int, int, int, int]]):
        draw = ImageDraw.Draw(img)
        draw.arc((xy, size), start=-90, end=-90 + 3.6 * min(progress_pc, 100), width=width, fill=fill)

    def font_auto_scale(self, font: ImageFont, text: str, desired_width: int, size_max: int,
                        size_min: int, stepping: int = 1) -> ImageFont:
        for size in range(size_max, size_min - 1, -stepping):
            new_font: ImageFont.FreeTypeFont = font.font_variant(size=size)
            font_width = new_font.getmask(text).getbbox()[2]
            font.ImageFont.getbbox
            print(f'font {size} = {font_width}')
            if font_width <= desired_width:
                return new_font

        fallback = font.font_variant(size=size_min)
        return fallback

    @commands.command(name="rank", description="Generate a rank card")
    async def rank(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data: User = await self.bot.db_client.get_user(user.id)

        user_balance = user_data.balance
        user_xp = user_data.xp
        max_xp = int(((user_data.level + 1) * 10) ** 2)

        # Load user avatar from URL and resize it
        target_size = 1024
        avatar_url = user.avatar.with_size(target_size).url
        image_bytes = await (await self.bot.web_client.get(avatar_url)).read()
        user_avatar = Image.open(BytesIO(image_bytes)) \
            .convert('RGBA') \
            .resize((target_size, target_size), resample=Image.LANCZOS)  # ensure we load this with an alpha channel

        base = Image.new("RGBA", (600, 300))  # 300, 150
        filtered = user_avatar.copy().filter(ImageFilter.GaussianBlur(radius=10))
        base.paste(filtered, (-((user_avatar.width // 2) - (base.width // 2)), -((user_avatar.height // 2) - (base.height // 2))), user_avatar)

        avatar_circle = user_avatar.copy()
        self.mask_ellipsis(avatar_circle)  # Apply mask before resizing as this yields better quality edges after applying mask
        avatar_circle = avatar_circle.resize((220, 220), resample=Image.LANCZOS)
        base.paste(avatar_circle, (20, 40), avatar_circle)

        self.arc_bar(img=base, xy=(10, 30), size=(250, 270), progress_pc=100,
                     width=10, fill=(255, 255, 255))

        self.arc_bar(img=base, xy=(10, 30), size=(250, 270), progress_pc=(user_xp / max_xp) * 100,
                     width=10, fill=(0, 191, 255))

        text_fill = (255, 255, 255) if self.get_brightness(base) <= 128 else (0, 0, 0)
        # Add text for XP and Balance
        text = f'XP: {user_xp}\nBalance: {user_balance}'
        font = ImageFont.truetype('circular-black.ttf', size=42)
        font = self.font_auto_scale(font, text, desired_width=325, size_max=42, size_min=20)

        draw = ImageDraw.Draw(base)
        draw.text((275, 150), text, fill=text_fill, font=font, anchor="lm")

        # Image is rendered at 2x resolution to produce a higher quality output
        # This is far better than rendering natively at 300, 150, as it'd look pixelated. Downsampling is better here.  
        base = base.resize((300, 150), resample=Image.LANCZOS)
        img_buffer = BytesIO()
        base.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Send the rank card to the user
        await ctx.send(file=discord.File(img_buffer, filename="rank_card.png"))


    @commands.command(name="supporttest", description="????")
    @commands.is_owner()
    async def testing(self, ctx):

        em = discord.Embed(title="Support Ticket",
                           description="Click the button below to open a support ticket with staff. Please be patient while we get to you. Do not open a ticket unless you need help with something.",
                           color=discord.Color.blurple())
        await ctx.send(embed=em, view=support_channel_view.SupportChannelView())

    @commands.command(name="test", description="test stuff")
    async def lol(self, ctx):
        # user = ctx.author  # Replace with the desired user
        # avg_color = await generate_embed_color(user)
        # user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        # e = int(((user_data.level + 1) * 10) ** 2)
        #
        # s = progress_percentage(user_data.xp, e)
        # embed = discord.Embed(title="User Embed", description=s, color=avg_color)
        # await ctx.send(embed=embed)
        # # Create an embed instance
        embed = discord.Embed(
            title="Comprehensive Embed",
            description="This is a comprehensive example of Discord.py embed options.",
            color=discord.Color.gold()  # Set the color of the embed
        )

        # Set the author information
        embed.set_author(
            name="Author Name",
            icon_url="https://cdn.discordapp.com/attachments/1145071029954297888/1145449093326442526/coinflip-removebg-preview.png",
            url="https://cdn.discordapp.com/attachments/1145071029954297888/1145449093326442526/coinflip-removebg-preview.png"
        )

        # Set a thumbnail for the embed
        embed.set_thumbnail(
            url=ctx.author.display_avatar.with_static_format("png"))

        # Add fields to the embed
        embed.add_field(name="Field 1", value="Value 1", inline=True)
        embed.add_field(name="Field 2", value="Value 2", inline=True)
        embed.add_field(name="Field 3", value="Value 3", inline=False)
        embed.add_field(name="Field 4", value="Value 4", inline=False)
        embed.add_field(name="Field 5", value="Value 5", inline=False)

        # Add an inline field
        embed.add_field(name="Inline Field",
                        value="This field is inline.", inline=True)

        # Set an image for the embed
        embed.set_image(
            url=ctx.author.display_avatar.with_static_format("png"))

        # Add more fields
        embed.add_field(name="Field 6", value="Value 6", inline=True)
        embed.add_field(name="Field 7", value="Value 7", inline=True)
        embed.add_field(name="Field 8", value="Value 8", inline=False)

        # Set the footer information
        timestamp = discord.utils.format_dt(
            datetime.datetime.now(datetime.timezone.utc), style="f")
        embed.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )

        # Send the embed
        await ctx.send(embed=embed)

    @commands.command(name="clearcd")
    @commands.is_owner()
    async def cdclear(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_data.cooldowns = {}
        await user_data.update_user({"cooldowns": user_data.cooldowns}, self.bot)
        await ctx.reply("Cooldowns cleared.")

    # stolen from random gist
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object],
                   spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.command(name="attempt", description="????")
    @commands.is_owner()
    async def attempt(self, ctx):
        message = """
        __**STEPS**__

        1. Write down today's current date on a sheet of paper. Write down the name of the server (BoobBot) as well as your user ID.

        2. Take a photo of said sheet of paper with your photo ID on it. The ID must have DOB as well as an identification photo. You can censor all other info except DOB and ID photo.

        3. Take a photo of yourself holding the sheet of paper with your face clearly shown.

        **WE DO NOT ACCEPT BIRTH CERTIFICATES UNDER ANY CIRCUMSTANCES**

        🔴 Click the button below to verify 🔴
        """
        em = discord.Embed(title="Verification", description=message, color=discord.Color.blurple())
        await ctx.send(embed=em, view=VerificationView())

        # description = "• This server is 18+. Adults acting like children, arguing with staff or causing drama will be removed.\n\n" \
        #               "• Do not post illegal content, follow Discord TOS and Community Guidelines. No gore, bestiality, scat, necrophilia, etc.\n\n" \
        #               "• Treat others with respect and kindness, regardless of their age, gender, race, sexual orientation, or any other personal characteristics. Do not engage in any behavior that could be considered bullying, harassment, or discrimination.\n\n" \
        #               "• Do not post screenshots of private conversations/other servers. No doxing or posting photos of others.\n\n" \
        #               "• Catfishing will result in a ban. Just be yourself, It's better that way.\n\n" \
        #               "• Use the appropriate channels for different types of conversation.\n\n" \
        #               "• The staff reserves the right to ban anyone causing trouble. No mini modding. We got this, Just enjoy your time here.\n\n" \
        #               "• Please respect people's roles.\n\n" \
        #               "• This server is English ONLY\n\n" \
        #               "• If you have ever been called a snowflake ❄️ or consider yourself to be 'woke', you might want to save yourself and us some time and frustration and go ahead hit the leave server button."
        # em = discord.Embed(title="Rules of Boobbot Community",
        #                    description=description, color=discord.Color.blurple())
        # await ctx.send(embed=em, view=RuleButton())

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        try:
            # Run git pull command and capture output
            result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)

            # Get command output
            command_output = result.stdout + result.stderr
            # Send output to discord
            if result.returncode == 0:
                await ctx.send(f'```{command_output}```')
                await ctx.send('Git pull successful')
            else:
                self.bot.logger.error(
                    f'Git pull failed with error code {result.returncode} and output:\n{command_output}')
                # if the bot is logged out, it will not be able to send the message
                await ctx.send(f'Git pull failed. Output:\n```{command_output}```')
        except subprocess.CalledProcessError as e:
            self.bot.logger.error(
                f'Git pull failed with error code {e.returncode} and output:\n{e.output}')
            # if the bot is logged out, it will not be able to send the message
            await ctx.send(f'An error occurred: {e}')

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        try:
            await ctx.send(f'Restarting with {sys.executable} {sys.argv}')
            os.execv(sys.executable, ['python'] + sys.argv)
        except subprocess.CalledProcessError as e:
            self.bot.logger.error(
                f'restart failed with error code {e.returncode} and output:\n{e.output}')
            await ctx.send(f'An error occurred: {e}')

    #
    #
    # @commands.command(name="hi", description="????")
    # async def hi(self, ctx):
    #     chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
    #                                                    messages=[{"role": "user", "content": ctx.message.content}])
    #     print(chat_completion.choices[0].message.content)
    #
    #     # Send the response as a message
    #     await ctx.send(chat_completion.choices[0].message.content)
    #
    @commands.group(name="jail", description="Manage jail time for users.", invoke_without_command=True)
    @commands.is_owner()
    async def jail(self, ctx):
        await ctx.send("Please use subcommands: check, clear, or add.")

    @jail.command(name="check", description="Check jail time of a user.")
    async def check_jail(self, ctx, user: commands.UserConverter):
        user_data = await self.bot.db_client.get_user(user.id)
        jail_info = user_data.jail

        if not jail_info:
            await ctx.send(f"{user.display_name} is not in jail.")
        else:
            remaining_time = jail_info.get("remaining_time", 0)
            release_time = user_data.is_in_jail()
            remaining_timestamp = discord.utils.format_dt(
                release_time, style="R")
            await ctx.send(f"{user.display_name} is in jail till {remaining_timestamp} seconds.")

    @jail.command(name="clear", description="Clear jail time of a user.")
    async def clear_jail(self, ctx, user: commands.UserConverter):
        user_data = await self.bot.db_client.get_user(user.id)

        if not user_data.jail:
            await ctx.send(f"{user.display_name} is not in jail.")
        else:
            await user_data.update_user({"jail": {}}, self.bot)
            await ctx.send(f"Cleared jail time for {user.display_name}.")

    @jail.command(name="add", description="Add jail time for a user.")
    async def add_jail(self, ctx, user: commands.UserConverter, time_in_seconds: int):
        user_data = await self.bot.db_client.get_user(user.id)
        current_jail_info = user_data.jail or {}

        remaining_time = current_jail_info.get(
            "remaining_time", 0) + time_in_seconds
        await user_data.update_user({"jail": {"remaining_time": remaining_time}}, self.bot)
        await ctx.send(f"Added {time_in_seconds} seconds of jail time for {user.display_name}.")

    @commands.group("streaks", description="Manage user streaks.", invoke_without_command=True)
    @commands.is_owner()
    async def streaks(self, ctx):
        await ctx.send("Please use subcommands: cleardaily, or clearweekly.")

    @streaks.command(name="cleardaily", description="Clear the daily streak of a user.")
    async def clear_daily(self, ctx, user: commands.UserConverter):
        user_data = await self.bot.db_client.get_user(user.id)

        if not user_data.daily_streak:
            await ctx.send(f"{user.display_name} has no streak.")
        else:
            await user_data.update_user({"daily_streak": {}}, self.bot)
            await ctx.send(f"Cleared streak for {user.display_name}.")

    @streaks.command(name="clearweekly", description="Clear the weekly streak of a user.")
    async def clear_weekly(self, ctx, user: commands.UserConverter):
        user_data = await self.bot.db_client.get_user(user.id)

        if not user_data.weekly_streak:
            await ctx.send(f"{user.display_name} has no streak.")
        else:
            await user_data.update_user({"weekly_streak": {}}, self.bot)
            await ctx.send(f"Cleared streak for {user.display_name}.")

    @commands.group("economy", description="Manage user economy.", invoke_without_command=True)
    @commands.is_owner()
    async def economy(self, ctx):
        await ctx.send("Please use subcommands: add, remove, or set.")

    @economy.command(name="add", description="Add money to a user's balance.")
    async def add_money(self, ctx, user: commands.UserConverter, amount: int):
        user_data = await self.bot.db_client.get_user(user.id)
        await user_data.add_balance(amount, self.bot)
        await ctx.send(f"Added {amount} to {user.display_name}'s balance.")

    @economy.command(name="remove", description="Remove money from a user's balance.")
    async def remove_money(self, ctx, user: commands.UserConverter, amount: int):
        user_data = await self.bot.db_client.get_user(user.id)
        await user_data.subtract_balance(amount, self.bot)
        await ctx.send(f"Removed {amount} from {user.display_name}'s balance.")

    @economy.command(name="set", description="Set a user's balance.")
    async def set_money(self, ctx, user: commands.UserConverter, amount: int):
        user_data = await self.bot.db_client.get_user(user.id)
        await user_data.update_balance(amount, self.bot)
        await ctx.send(f"Set {user.display_name}'s balance to {amount}.")

    @commands.command(name="eval")
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'ctx': ctx,
            'bot': self.bot,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'message': ctx.message,
            'source': inspect.getsource,
            'discord': discord,
            'commands': commands,
            'os': os,
            'sys': sys,
            'psutil': psutil,
            're': re,
            'textwrap': textwrap,
            'traceback': traceback,
            'io': io,
            'BytesIO': BytesIO
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            em = discord.Embed(title="Error", description=f"```py\n{value}{traceback.format_exc()}\n```",
                               color=discord.Color.red())
            return await ctx.send(embed=em)

        value = stdout.getvalue()

        if ret is None:
            if value:
                em = discord.Embed(
                    title="Success", description=f"```py\n{value}\n```", color=discord.Color.green())
                return await ctx.send(embed=em)
            else:
                em = discord.Embed(title="Success", description="```py\nNo output\n```",
                                   color=discord.Color.green())
                return await ctx.send(embed=em)
        else:
            em = discord.Embed(
                title="Success", description=f"```py\n{value}{ret}\n```", color=discord.Color.green())
            return await ctx.send(embed=em)

    @staticmethod
    def cleanup_code(body):
        """Automatically removes code blocks from the code."""
        if body.startswith('```py') and body.endswith('```'):
            body = body[5:-3]
        if body.startswith('```') and body.endswith('```'):
            body = body[3:-3]
        # remove `foo`
        if body.startswith('`') and body.endswith('`'):
            body = body[1:-1]
        return body


async def setup(bot):
    await bot.add_cog(Dev(bot))
