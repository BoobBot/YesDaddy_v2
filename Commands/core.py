import os
import subprocess
import sys

import discord
import openai
from discord.ext import commands

from Views.rule_button_view import RuleButton
from Views.verification_view import VerificationView
from utils.utilities import generate_embed_color


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
        embed = discord.Embed(title="User Embed", description="This is a user's embed.", color=avg_color)
        await ctx.send(embed=embed)

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


async def setup(bot):
    await bot.add_cog(Core(bot))
