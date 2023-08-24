import datetime

from discord.ext import commands


def timedelta_to_discord_timestamp(delta):
    total_seconds = delta.total_seconds()
    days = int(total_seconds // (60 * 60 * 24))
    hours = int((total_seconds % (60 * 60 * 24)) // (60 * 60))
    minutes = int((total_seconds % (60 * 60)) // 60)
    seconds = int(total_seconds % 60)

    timestamp_str = f"{days}d {hours}h {minutes}m {seconds}s"
    return timestamp_str


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
            await ctx.send(f'You are on cooldown. Try again in {timedelta_to_discord_timestamp(delta)}.')
            return False

        await ctx.bot.db_client.user_collection.update_one(
            {'user_id': user_id},
            {'$set': {f'cooldowns.{ctx.command.name}': now}},
        )
        return True

    return commands.check(predicate)
