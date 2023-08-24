import datetime

import discord
from discord.ext import commands


def datetime_to_discord_timestamp(dt):
    return dt.strftime("<t:%Y-%m-%d %H:%M:%S>")


def persistent_cooldown(rate, per, type=commands.BucketType.user):
    async def predicate(ctx, *args, **kwargs):
        now = datetime.datetime.utcnow()
        user_id = ctx.author.id

        document = await ctx.bot.db_client.user_collection.find_one({'user_id': user_id})
        print(document)
        if not document:
            print("User not found.")
            pass

        command_cooldown = document['cooldowns'].get(ctx.command.name)
        print()
        if command_cooldown and (last_used := command_cooldown + datetime.timedelta(seconds=per)) > now:
            delta = last_used - now
            target_time = now + delta
            embed = discord.Embed(
                title=f'You are on cooldown. Try again in {datetime_to_discord_timestamp(target_time)}.',
                description=datetime_to_discord_timestamp(target_time), color=0x00ff00)
            await ctx.send(embed=embed)
            return False

        await ctx.bot.db_client.user_collection.update_one(
            {'user_id': user_id},
            {'$set': {f'cooldowns.{ctx.command.name}': now}},
        )
        return True

    return commands.check(predicate)
