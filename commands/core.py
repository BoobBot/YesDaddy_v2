from discord.ext import commands


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Show bot and API latency.")
    async def ping(self, ctx):
        await ctx.reply(f"Pong! Bot latency: {self.bot.latency * 1000:.2f} ms")

    @commands.hybrid_command(name="invite", description="Invite the bot to your server.")
    async def invite(self, ctx):
        await ctx.reply(f"https://discord.com/api/oauth2/authorize?client_id={self.bot.id}&permissions=8&scope=bot+applications.commands")

    @commands.hybrid_command(name="support", description="Join the support server.")
    async def support(self, ctx):
        await ctx.reply("https://discord.gg/boobbot")

    @commands.hybrid_command(name="github", description="View the bot's GitHub repository.")
    async def github(self, ctx):
        await ctx.reply("https://github.com/BoobBot/YesDaddy_v2")


async def setup(bot):
    await bot.add_cog(Core(bot))
