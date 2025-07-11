import asyncio
import contextlib
import math
import random

import discord
from discord.ext import commands

from utils.utilities import calculate_level, is_today_weekend_or_holiday, amount_on_level_up, bad_flag, swap_flag, \
    good_flag

import string

TRIGGER_WORDS = {
    "gay",
    "homo",
    "homosexual",
    "lesbian",
    "bi",
    "bisexual",
    "trans",
    "transgender",
    "lgbt",
    "lgbtq",
    "queer",
    "nonbinary",
    "non-binary",
    "nb",
    "pansexual",
    "asexual",
    "ace",
    "aro",
    "aromantic",
    "drag",
    "pride",
    "closet",
    "closeted",
    "ally",
    "top",
    "bottom",
    "switch",
    "femboy",
    "twink",
    "bear",
    "daddy",
    "yas",
    "slay",
    "serve",
    "werk",
    "queen",
    "king",
    "gender",
    "genderfluid",
    "genderqueer",
    "pronoun",
    "he/him",
    "she/her",
    "they/them",
    "homophobia"
}

def contains_trigger_word_exact(message_content: str) -> bool:
    # Normalize message: lowercase and strip punctuation from words
    translator = str.maketrans('', '', string.punctuation)
    words = [w.translate(translator).lower() for w in message_content.split()]
    return any(word in TRIGGER_WORDS for word in words)


async def dump_delete(msg):
    with contextlib.suppress(Exception):
        await asyncio.sleep(120)
        await msg.delete()


async def process_level_roles(user, member, guild, bot):
    data = await bot.db_client.get_guild(guild.id)
    for role in data.lvl_roles:
        if role.get("level") <= user.level:
            print(role.get("role_id"))
            await member.add_roles(guild.get_role(int(role.get("role_id"))))
        else:
            print(role.get("role_id"))
            await member.remove_roles(guild.get_role(int(role.get("role_id"))))


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id == 1131746094313902171:
            if msg.attachments:
                await msg.add_reaction("❤️")
        if msg.channel.id == 1194630143239540788:
            await dump_delete(msg)
        if msg.channel.id == 1141856931984715807:
            await dump_delete(msg)
        #cab
        if msg.channel.id == 1092979518471422023:
            await dump_delete(msg)
        if msg.channel.id == 1092969722900914236:
            await dump_delete(msg)
        if msg.channel.id == 1378806059497558241:
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
            if bad_flag in msg.content:
                await msg.add_reaction(good_flag)
            if bad_flag in msg.author.display_name:
                new_name = swap_flag(msg.author.display_name)
                await msg.author.edit(nick=new_name)
            data = await self.bot.db_client.get_guild(msg.guild.id)
            for reaction in data.text_reactions:
                if reaction.get("trigger") in msg.content.lower():
                    await msg.add_reaction(reaction.get("response"))

            if contains_trigger_word_exact(msg.content):
                user = msg.guild.get_member(704819426679324672)
                if user:
                    await msg.channel.send(f"{user.mention} ⚠️ gay detected: \"{msg.content}\"", delete_after=60)



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
                if msg.guild.id != 1217880601135288493:
                    lvl_up_bonus = amount_on_level_up(lvl, 100, 1.05)
                    guild = await self.bot.db_client.get_guild(msg.guild.id)
                    channel_id = await guild.get_config("lvl_up_channel")
                    try:
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
                    except discord.Forbidden:
                        pass
                    user.level = lvl

                    await user.update_fields(level=lvl, balance=user.balance + lvl_up_bonus)
                    await process_level_roles(user, msg.author, msg.guild, self.bot)
            await user.update_fields(xp=user.xp + xp, messages=user.messages + 1, last_seen=msg.created_at, active={})


async def setup(bot):
    await bot.add_cog(Message(bot))
