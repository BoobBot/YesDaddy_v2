import os
import subprocess
import sys

import discord
import openai
from discord.ext import commands

from Views.verification_view import VerificationView


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Show bot and API latency.")
    async def ping(self, ctx):
        await ctx.reply(f"Pong! Bot latency: {self.bot.latency * 1000:.2f} ms")


    @commands.command(name="test", description="????")
    @commands.is_owner()
    async def test(self, ctx):
        message = """
        __**STEPS**__

        1. Write down today's current date on a sheet of paper. Write down the name of the server (BoobBot) as well as your user ID.

        2. Take a photo of said sheet of paper with your photo ID on it. The ID must have DOB as well as an identification photo. You can censor all other info except DOB and ID photo.

        3. Take a photo of yourself holding the sheet of paper with your face clearly shown.

        **WE DO NOT ACCEPT BIRTH CERTIFICATES UNDER ANY CIRCUMSTANCES**

        🔴 Click the button below to verify 🔴
        """
        await ctx.send(message, view=VerificationView())

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        try:
            # Run git pull command and capture output
            result = subprocess.run(['git', 'pull', 'origin', 'master'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)

            # Get command output
            command_output = result.stdout + result.stderr
            # Send output to discord
            if result.returncode == 0:
                await ctx.send(f'```{command_output}```')
                await ctx.send(f'Git pull successful. Restarting with {sys.executable} {sys.argv}')
                # Restart the bot
                await self.bot.logout()
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                self.bot.logger.error(f'Git pull failed with error code {result.returncode} and output:\n{command_output}')
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


async def setup(bot):
    await bot.add_cog(Core(bot))
