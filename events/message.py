import asyncio
import contextlib
import math
import random

import discord
from discord.ext import commands


async def dump_delete(msg):
    with contextlib.suppress(Exception):
        await asyncio.sleep(120)
        await msg.delete()


async def process_level_roles(user, member, guild, bot):
    data = await bot.db_client.get_guild(guild.id)
    for role in data.lvl_roles:
        if role.get("level") <= user.level:
            await member.add_roles(discord.utils.get(guild.roles, id=role.get("role_id")))
        # else:
        #     await user.remove_role(role.get("role_id"), bot=bot)


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id == 1141856931984715807:
            await dump_delete(msg)
        if msg.author.bot:
            return
        if msg.guild is None:
            guild = 694641646780022818
            guild = self.bot.get_guild(guild)
            data = await self.bot.db_client.get_guild(guild.id)
            ticket = next((ticket for ticket in data.support_tickets if
                           ticket.get("dm_channel_id") == msg.channel.id and ticket.get("status") == "open"), None)
            if ticket:
                print(ticket.get("channel_id"))
                channel = await guild.fetch_channel(ticket.get("channel_id"))
                await channel.send(f"**{msg.author.name}**#{msg.author.discriminator}: {msg.content}")
                if msg.attachments:
                    for attachment in msg.attachments:
                        await channel.send(attachment.url)
                return
        if msg.guild:
            await msg.add_reaction("<:indo:911816843126243338>")
            data = await self.bot.db_client.get_guild(msg.guild.id)
            for reaction in data.text_reactions:
                if reaction.get("trigger") in msg.content.lower():
                    await msg.add_reaction(reaction.get("response"))

            if msg.channel.category_id == 1141700782006222970:
                if msg.content.startswith("-"):
                    data = await self.bot.db_client.get_guild(msg.guild.id)
                    ticket = next((ticket for ticket in data.support_tickets if
                                   ticket.get("channel_id") == msg.channel.id and ticket.get("status") == "open"),
                                  None)
                    if ticket:
                        print(ticket.get("dm_channel_id"))
                        channel = await self.bot.fetch_channel(int(ticket.get("dm_channel_id")))
                        await channel.send(f"**{msg.author.name}**#{msg.author.discriminator}: {msg.content[1:]}")
                        if msg.attachments:
                            for attachment in msg.attachments:
                                await channel.send(attachment.url)
                        return
            user = await self.bot.db_client.get_user(user_id=msg.author.id)
            bonus_xp = sum(1 for role in msg.author.roles for r in data.bonus_roles if role.id == r.get("role_id"))
            bonus_xp += 1
            xp = random.randint(1, 10) * bonus_xp
            lvl = math.floor(0.1 * math.sqrt(user.xp + xp))
            if lvl > user.level:
                await msg.channel.send(
                    f"Congratulations {msg.author.mention}! You have leveled up to level {lvl}! <a:lvlup:1138933829185323149>")
                user.level = lvl
                await user.update_level(amount=user.level, bot=self.bot)
                await process_level_roles(user, msg.author, msg.guild, self.bot)
            await user.update_messages(bot=self.bot)
            await user.add_xp(xp, bot=self.bot)
            await user.update_last_seen(bot=self.bot)


async def setup(bot):
    await bot.add_cog(Message(bot))
