import datetime
import random

import discord
from discord.ext import tasks, commands


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_jail_loop.start()
        self.change_role_color.start()
        self.voice_xp.start()
        self.guild_sync_loop.start()

    def cog_unload(self):
        self.check_jail_loop.cancel()
        self.change_role_color.cancel()
        self.voice_xp.cancel()
        self.guild_sync_loop.cancel()

    @tasks.loop(minutes=15)
    async def guild_sync_loop(self):
        try:
            support = self.bot.get_guild(440526421388165120)
            community = self.bot.get_guild(694641646780022818)
            lounge = self.bot.get_guild(449970824812953612)
            contributor = discord.utils.get(support.roles, id=528615882709008430)
            contributor_plus = discord.utils.get(support.roles, id=528615837305929748)
            kissy_contributor = discord.utils.get(support.roles, id=528615659115118602)
            nitro_booster = discord.utils.get(support.roles, id=585533009797578759)
            lounge_booster = discord.utils.get(lounge.roles, id=588226955778850816)
            for member in contributor.members:
                try:
                    mem = await community.fetch_member(member.id)
                    # self.bot.log.info(f"Syncing {mem.name} to community")
                    if mem:
                        await mem.add_roles(discord.utils.get(community.roles, id=694641646901395515))
                except Exception as e:
                    pass
            for member in contributor_plus.members:
                try:
                    mem = await community.fetch_member(member.id)
                    # self.bot.log.info(f"Syncing {mem.name} to community")
                    if mem:
                        await mem.add_roles(discord.utils.get(community.roles, id=694641646914109460))
                except Exception as e:
                    pass
            for member in kissy_contributor.members:
                try:
                    mem = await community.fetch_member(member.id)
                    # self.bot.log.info(f"Syncing {mem.name} to community")
                    if mem:
                        await mem.add_roles(discord.utils.get(community.roles, id=694641646838480978))
                except Exception as e:
                    pass
            for member in nitro_booster.members:
                try:
                    mem = await community.fetch_member(member.id)
                    # self.bot.log.info(f"Syncing {mem.name} to community")
                    if mem:
                        await mem.add_roles(discord.utils.get(community.roles, id=872596931598225489))
                except Exception as e:
                    pass
            for member in lounge_booster.members:
                try:
                    mem = await community.fetch_member(member.id)
                    if mem:
                        await mem.add_roles(discord.utils.get(community.roles, id=872596931598225489))
                except Exception as e:
                    pass
        except Exception as e:
            self.bot.log.error(e)
            pass

    @guild_sync_loop.before_loop
    async def before_guild_sync(self):
        await self.bot.wait_until_ready()
        # Start the loop after the bot is ready
        print("Starting the sync loop")
        # Run the loop once to initialize the role color
        await self.guild_sync_loop()

    @tasks.loop(minutes=1)
    async def voice_xp(self):
        try:
            guild = self.bot.guilds
            for guild in guild:
                voice_channels = [channel for channel in guild.voice_channels if len(channel.members) > 0]
                for channel in voice_channels:
                    # Check if the channel is the AFK channel
                    if guild.afk_channel and channel.id == guild.afk_channel.id:
                        continue
                    count = len([member for member in channel.members if not member.bot])
                    if count <= 1:
                        continue
                    for member in channel.members:
                        # Check if any of the following conditions are met:
                        # - Member is deafened by the guild
                        # - Member is muted by the guild
                        # - Member is self-muted
                        # - Member is self-deafened
                        if member.voice.deaf or member.voice.mute or member.voice.self_mute or member.voice.self_deaf:
                            continue  # Skip giving XP to this member
                        user = await self.bot.db_client.get_user(member.id)
                        if user:
                            data = await self.bot.db_client.get_guild(guild.id)
                            bonus_xp = sum(
                                1 for role in member.roles for r in data.bonus_roles if role.id == r.get("role_id"))
                            bonus_xp += 1
                            xp = random.randint(10, 50) * bonus_xp
                            await user.add_xp(xp)
                            await user.update_last_seen()
                            self.bot.log.info(f"{member.name} {xp} -> {user.xp}")
        except Exception as e:
            self.bot.log.error(e)
            pass

    @tasks.loop(minutes=5)
    async def check_jail_loop(self):
        users_in_jail = await self.bot.db_client.get_users_in_jail()

        for user_id in users_in_jail:
            user = await self.bot.db_client.get_user(user_id)
            if user.is_in_jail():
                release_time = user.jail["start_time"].replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(
                    hours=user.jail["duration_hours"])
                current_time = datetime.datetime.now(datetime.timezone.utc)

                if current_time >= release_time:
                    fine = user.jail.get("fine", 0)
                    await user.subtract_balance(fine)
                    await user.update_user({"jail": {}})
                    self.bot.log.info(
                        f"User {user_id} has been released from jail.")

    @tasks.loop(minutes=5)  # Run the task every 5 minutes
    async def change_role_color(self):
        print("Changing role color")
        guild = self.bot.get_guild(694641646780022818)
        role_id_1 = 694641646901395506
        role_id_2 = 694641646922498068
        role_1 = guild.get_role(role_id_1)
        role_2 = guild.get_role(role_id_2)
        print(f"has {guild}")

        if role_1 and role_2:
            non_yellow_color = None

            while not non_yellow_color or self.is_yellow(non_yellow_color):
                non_yellow_color = discord.Color.random()

            await role_1.edit(color=non_yellow_color)
            await role_2.edit(color=discord.Color.random())
        print("Changed color.")

    @staticmethod
    def is_yellow(color):
        r, g, b = color.r / 255, color.g / 255, color.b / 255

        max_value = max(r, g, b)
        min_value = min(r, g, b)

        if max_value == min_value:
            hue = 0
        elif max_value == r:
            hue = 60 * ((g - b) / (max_value - min_value))
        elif max_value == g:
            hue = 60 * (2 + (b - r) / (max_value - min_value))
        else:
            hue = 60 * (4 + (r - g) / (max_value - min_value))

        return 30 <= hue <= 60

    @change_role_color.before_loop
    async def before_change_role_color(self):
        await self.bot.wait_until_ready()
        # Start the loop after the bot is ready
        print("Starting the role color change loop")
        # Run the loop once to initialize the role color
        await self.change_role_color()


async def setup(bot):
    await bot.add_cog(Loops(bot))
