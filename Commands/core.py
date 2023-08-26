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
        self.process = psutil.Process(os.getpid())
        self.env = {}
        self.stdout = io.StringIO()

    async def _eval(self, ctx, code):
        if code == "exit()":
            self.env = {}
            return await ctx.send("History reset.")

        env = {
            "message": ctx.message,
            "author": ctx.author,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "ctx": ctx,
            "self": self,
            "bot": self.bot,
            "inspect": inspect,
            "discord": discord,
            "contextlib": contextlib
        }

        self.env.update(env)

        async def func():
            try:
                with contextlib.redirect_stdout(self.stdout):
                    exec(code, self.env)
                if '_' in self.env:
                    result = self.env['_']
                    if inspect.isawaitable(result):
                        result = await result
                    return result
            finally:
                self.env.update(locals())

        try:
            result = await func()
        except Exception as e:
            result = traceback.format_exc()

        output, embed = self._format(code, result)
        try:
            await ctx.send(f"```py\n{output}```", embed=embed)
        except discord.HTTPException:
            data = BytesIO(output.encode('utf-8'))
            await ctx.send(content="Too long to send, here's a text file instead.",
                           file=discord.File(data, filename="Result.txt"))

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
        result = True if "true" in guild.lower() else Fals
        await ctx.send(f"Syncing commands for guild {self.bot.config.testing_guild_id}")
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
    async def __eval(self, ctx, *, code):
        """ Run eval in a REPL-like format. """
        code = code.strip("`")
        if code.startswith("py\n"):
            code = "\n".join(code.split("\n")[1:])

        if not re.search(r"^(return|import|for|while|def|class|"
                         r"from|exit|[a-zA-Z0-9]+\s*=)",
                         code, re.M) and len(code.split("\n")) == 1:
            code = "_ = " + code

        await self._eval(ctx, code)

    def _format(self, input_code, output_result):
        self.env["_"] = output_result

        formatted_input = textwrap.dedent(input_code)

        self.stdout.seek(0)
        output_text = self.stdout.read()
        self.stdout.close()
        self.stdout = io.StringIO()

        if output_text:
            formatted_input += output_text + "\n"

        if output_result is None:
            return formatted_input

        if isinstance(output_result, discord.Embed):
            return formatted_input + "\n<Embed>"
        else:
            formatted_input += str(output_result)
            return formatted_input


async def setup(bot):
    await bot.add_cog(Core(bot))
