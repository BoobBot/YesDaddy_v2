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
