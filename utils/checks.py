import datetime

import discord
from discord.ext import commands


import datetime
import discord
from discord.ext import commands

def persistent_cooldown(rate, per, type=commands.BucketType.user):
    async def predicate(ctx, *args, **kwargs):
        now = datetime.datetime.now(datetime.timezone.utc)
        user_id = ctx.author.id

        user = await ctx.bot.db_client.get_user(ctx.guild.id, user_id)

        command_cooldown = user.cooldowns.get(ctx.command.name)
        if command_cooldown:
            command_cooldown = command_cooldown.replace(tzinfo=datetime.timezone.utc)

        if command_cooldown and (last_used := command_cooldown + datetime.timedelta(seconds=per)) > now:
            delta = last_used - now
            target_time = now + delta
            remaining_timestamp = discord.utils.format_dt(target_time, style="R")

            em = discord.Embed(
                description=f":x: You are on cooldown. Try again {remaining_timestamp}",
                color=discord.Color.red()
            )
            await ctx.reply(embed=em)
            return False

        user.cooldowns[ctx.command.name] = now
        await user.update_fields(cooldowns=user.cooldowns)

        return True

    return commands.check(predicate)

