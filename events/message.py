import asyncio
import contextlib
import math
import random

import discord
from discord.ext import commands

from utils.utilities import calculate_level, is_today_weekend_or_holiday


async def dump_delete(msg):
    with contextlib.suppress(Exception):
        await asyncio.sleep(120)
        await msg.delete()


async def process_level_roles(user, member, guild, bot):
    data = await bot.db_client.get_guild(guild.id)
    for role in data.lvl_roles:
        if role.get("level") <= user.level:
            await member.add_roles(guild.get_role(int(role.get("role_id"))))
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
            user = await self.bot.db_client.get_user(user_id=msg.author.id, guild_id=msg.guild.id)
            bonus_xp = sum(1 for role in msg.author.roles for r in data.bonus_roles if role.id == r.get("role_id"))
            bonus_xp += 1
            xp = random.randint(1, 10) * bonus_xp
            lvl = calculate_level(user.xp + xp)
            if is_today_weekend_or_holiday():
                xp *= 2
            if lvl > user.level:
                lvl_up_bonus = 1000 * lvl
                guild = await self.bot.db_client.get_guild(msg.guild.id)
                channel_id = await guild.get_config("lvl_up_channel")
                if channel_id:
                    channel = msg.guild.get_channel(int(channel_id))
                    if channel:
                        await channel.send(
                            f"# 🎉Congratulations {msg.author.mention}!\n## <a:lvlup:1138933829185323149> You have leveled up to level {lvl}!\n### <:info:486945488080338944> You have been awarded ${lvl_up_bonus} as a level up bonus!")
                    else:
                        await msg.channel.send(
                            f"# 🎉Congratulations {msg.author.mention}!\n## <a:lvlup:1138933829185323149> You have leveled up to level {lvl}!\n### <:info:486945488080338944> You have been awarded ${lvl_up_bonus} as a level up bonus!")
                else:
                    await msg.channel.send(
                        f"# 🎉Congratulations {msg.author.mention}!\n## <a:lvlup:1138933829185323149> You have leveled up to level {lvl}!\n### <:info:486945488080338944> You have been awarded ${lvl_up_bonus} as a level up bonus!")
                user.level = lvl

                await user.update_fields(level=lvl, balance=user.balance + lvl_up_bonus)
                await process_level_roles(user, msg.author, msg.guild, self.bot)
            await user.update_fields(xp=user.xp + xp, messages=user.messages + 1, last_seen=msg.created_at)


async def setup(bot):
    await bot.add_cog(Message(bot))
