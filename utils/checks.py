import datetime

import discord
from discord.ext import commands


def persistent_cooldown(rate, per, type=commands.BucketType.user):
    async def predicate(ctx, *args, **kwargs):
        now = datetime.datetime.now(datetime.timezone.utc)
        user_id = ctx.author.id

        document = await ctx.bot.db_client.user_collection.find_one({'user_id': user_id})
        if not document:
            pass

        command_cooldown = document['cooldowns'].get(ctx.command.name)
        if command_cooldown:
            command_cooldown = command_cooldown.replace(
                tzinfo=datetime.timezone.utc)

        if command_cooldown and (last_used := command_cooldown + datetime.timedelta(seconds=per)) > now:
            delta = last_used - now
            target_time = now + delta
            remaining_timestamp = discord.utils.format_dt(target_time, style="R"
                                                          )

            em = discord.Embed(description=f":x: You are on cooldown. Try again {remaining_timestamp}",
                               color=discord.Color.red())
            await ctx.reply(embed=em)
            return False

        await ctx.bot.db_client.user_collection.update_one(
            {'user_id': user_id},
            {'$set': {f'cooldowns.{ctx.command.name}': now}},
        )
        return True

    return commands.check(predicate)
