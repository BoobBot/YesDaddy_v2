import contextlib
import inspect
import io
import os
import re
import subprocess
import sys
import textwrap
import traceback
from io import BytesIO

import discord
import psutil
from discord.ext import commands

from Views.rule_button_view import RuleButton
from utils.utilities import generate_embed_color, progress_percentage


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Show bot and API latency.")
    async def ping(self, ctx):
        await ctx.reply(f"Pong! Bot latency: {self.bot.latency * 1000:.2f} ms")

    @commands.command(name="test", description="test stuff")
    async def lol(self, ctx):
        user = ctx.author  # Replace with the desired user
        avg_color = await generate_embed_color(user)
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        e = int(((user_data.level + 1) * 10) ** 2)

        s = progress_percentage(user_data.xp, e)
        embed = discord.Embed(title="User Embed", description=s, color=avg_color)
        await ctx.send(embed=embed)

    @commands.command(name="clearcd")
    @commands.is_owner()
    async def cdclear(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_data = await ctx.bot.db_client.get_user(user_id=user.id)
        user_data.cooldowns = {}
        await user_data.update_user({"cooldowns": user_data.cooldowns}, self.bot)
        await ctx.reply("Cooldowns cleared.")

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx, guild: str = None):
        if guild is None:
            result = False
        else:
            result = True if "true" in guild.lower() else False
        await ctx.send(f"Syncing commands")
        guild = discord.Object(self.bot.config.testing_guild_id)
        self.bot.tree.copy_global_to(guild=guild)
        if result:
            await ctx.send("Syncing guild")
            await self.bot.tree.sync(guild=guild)
            await ctx.send("Synced commands for guild {self.bot.config.testing_guild_id}")
        else:
            await ctx.send("Syncing global")
            await self.bot.tree.sync()
            self.bot.log.info(f"Synced commands for global")
            await ctx.send("Synced commands for global")

    @commands.command(name='deletecommands', aliases=['clear'])
    @commands.is_owner()
    async def delete_commands(self, ctx):
        guild = discord.Object(self.bot.config.testing_guild_id)
        await self.bot.tree.clear_commands(guild=guild)
        await self.bot.tree.sync(guild=guild)
        await self.bot.tree.sync()
        await ctx.send('Commands deleted.')

    @commands.command(name="attempt", description="????")
    @commands.is_owner()
    async def attempt(self, ctx):
        # message = """
        # __**STEPS**__
        #
        # 1. Write down today's current date on a sheet of paper. Write down the name of the server (BoobBot) as well as your user ID.
        #
        # 2. Take a photo of said sheet of paper with your photo ID on it. The ID must have DOB as well as an identification photo. You can censor all other info except DOB and ID photo.
        #
        # 3. Take a photo of yourself holding the sheet of paper with your face clearly shown.
        #
        # **WE DO NOT ACCEPT BIRTH CERTIFICATES UNDER ANY CIRCUMSTANCES**
        #
        # 🔴 Click the button below to verify 🔴
        # """
        description = "• This server is 18+. Adults acting like children, arguing with staff or causing drama will be removed.\n\n" \
                      "• Do not post illegal content, follow Discord TOS and Community Guidelines. No gore, bestiality, scat, necrophilia, etc.\n\n" \
                      "• Treat others with respect and kindness, regardless of their age, gender, race, sexual orientation, or any other personal characteristics. Do not engage in any behavior that could be considered bullying, harassment, or discrimination.\n\n" \
                      "• Do not post screenshots of private conversations/other servers. No doxing or posting photos of others.\n\n" \
                      "• Catfishing will result in a ban. Just be yourself, It's better that way.\n\n" \
                      "• Use the appropriate channels for different types of conversation.\n\n" \
                      "• The staff reserves the right to ban anyone causing trouble. No mini modding. We got this, Just enjoy your time here.\n\n" \
                      "• Please respect people's roles.\n\n" \
                      "• This server is English ONLY\n\n" \
                      "• If you have ever been called a snowflake ❄️ or consider yourself to be 'woke', you might want to save yourself and us some time and frustration and go ahead hit the leave server button."
        em = discord.Embed(title="Rules of Boobbot Community", description=description, color=discord.Color.blurple())
        await ctx.send(embed=em, view=RuleButton())

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
                await ctx.send(f'Git pull successful. Restarting with {sys.executable} {sys.argv}')
                # Restart the bot
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                self.bot.logger.error(
                    f'Git pull failed with error code {result.returncode} and output:\n{command_output}')
                # if the bot is logged out, it will not be able to send the message
                await ctx.send(f'Git pull failed. Output:\n```{command_output}```')
        except subprocess.CalledProcessError as e:
            self.bot.logger.error(f'Git pull failed with error code {e.returncode} and output:\n{e.output}')
            # if the bot is logged out, it will not be able to send the message
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
                em = discord.Embed(title="Success", description=f"```py\n{value}\n```", color=discord.Color.green())
                return await ctx.send(embed=em)
            else:
                em = discord.Embed(title="Success", description="```py\nNo output\n```",
                                   color=discord.Color.green())
                return await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Success", description=f"```py\n{value}{ret}\n```", color=discord.Color.green())
            return await ctx.send(embed=em)

    def cleanup_code(self, body):
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
    await bot.add_cog(Core(bot))
