import datetime

import discord
from discord.ext import commands


def persistent_cooldown(rate, per, type=commands.BucketType.user):
    async def predicate(ctx, *args, **kwargs):
        now = datetime.datetime.utcnow()
        user_id = ctx.author.id
        document = await ctx.bot.db_client.user_collection.find_one({'user_id': user_id})
        if not document:
            pass
        command_cooldown = document['cooldowns'].get(ctx.command.name)
        if command_cooldown and (last_used := command_cooldown + datetime.timedelta(seconds=per)) > now:
            target_time = command_cooldown + datetime.timedelta(seconds=per)
            epoch = round(target_time.timestamp())
            embed = discord.Embed(
                title=f'You are on cooldown. Try again in <t:{epoch}:R>.',
                color=0x00ff00)
            await ctx.send(embed=embed)
            return False

        await ctx.bot.db_client.user_collection.update_one(
            {'user_id': user_id},
            {'$set': {f'cooldowns.{ctx.command.name}': now}},
        )
        return True

    return commands.check(predicate)
