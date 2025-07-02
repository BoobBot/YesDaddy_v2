import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from collections import defaultdict

class SnipeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = defaultdict(list)      # channel_id: list of (author, content, time, attachments)
        self.edit_snipes = defaultdict(list) # channel_id: list of (author, before, after, time)

    def trim_list(self, lst, limit=5):
        if len(lst) > limit:
            del lst[limit:]

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        attachments = [a.url for a in message.attachments]
        self.snipes[message.channel.id].insert(0, (
            message.author,
            message.content,
            message.created_at,
            attachments
        ))
        self.trim_list(self.snipes[message.channel.id])

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        self.edit_snipes[before.channel.id].insert(0, (
            before.author,
            before.content,
            after.content,
            before.edited_at or datetime.utcnow()
        ))
        self.trim_list(self.edit_snipes[before.channel.id])

    @commands.hybrid_command(name="snipe", description="Snipe a recently deleted message (default: latest)")
    async def snipe(self, ctx: commands.Context, index: int = 1):
        messages = self.snipes.get(ctx.channel.id)
        if not messages or index < 1 or index > len(messages):
            return await ctx.reply("There's nothing to snipe at that index.", ephemeral=True if ctx.interaction else False)

        author, content, timestamp, attachments = messages[index - 1]
        embed = discord.Embed(
            title=f"🧨 Sniped Message #{index}",
            description=content or "*[No text]*",
            color=discord.Color.orange(),
            timestamp=timestamp
        )
        embed.set_author(name=str(author), icon_url=author.display_avatar.url)
        if attachments:
            embed.add_field(name="Attachments", value="\n".join(attachments), inline=False)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="editsnipe", description="Snipe a recently edited message (default: latest)")
    async def editsnipe(self, ctx: commands.Context, index: int = 1):
        messages = self.edit_snipes.get(ctx.channel.id)
        if not messages or index < 1 or index > len(messages):
            return await ctx.reply("There's no edited message at that index.", ephemeral=True if ctx.interaction else False)

        author, before, after, timestamp = messages[index - 1]
        embed = discord.Embed(
            title=f"✏️ Edited Message #{index}",
            color=discord.Color.blue(),
            timestamp=timestamp
        )
        embed.set_author(name=str(author), icon_url=author.display_avatar.url)
        embed.add_field(name="Before", value=before or "*[No text]*", inline=False)
        embed.add_field(name="After", value=after or "*[No text]*", inline=False)
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(SnipeCog(bot))
