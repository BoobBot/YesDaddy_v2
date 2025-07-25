import datetime
import random

import aiohttp
import discord
from discord.ext import tasks, commands

from database import User
from utils.utilities import calculate_level, is_today_weekend_or_holiday, amount_on_level_up


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_jail_loop.start()
        self.change_role_color.start()
        self.voice_xp.start()
        self.guild_sync_loop.start()
        self.reminder_loop.start()
        self.new_member_loop.start()
        self.delete_inactive.start()

    def cog_unload(self):
        self.check_jail_loop.cancel()
        self.change_role_color.cancel()
        self.voice_xp.cancel()
        self.guild_sync_loop.cancel()
        self.reminder_loop.cancel()
        self.new_member_loop.cancel()
        self.delete_inactive.cancel()

    @tasks.loop(minutes=30)
    async def delete_inactive(self):
        try:
            guilds = self.bot.guilds
            for guild in guilds:
                data = await self.bot.db_client.get_guild(guild.id)
                for user in data.users:
                    user = User.from_existing(self.bot.db_client, user)
                    if user.active.get('active', True) is False:
                        print(f"Deleting user {user.user_id}")
                        if datetime.datetime.utcnow() - user.active.get('timestamp') > datetime.timedelta(days=30):
                            await data.delete_user(user.user_id)

        except Exception as e:
            self.bot.log.error(e)
            pass

    async def daily_reminder(self, reminder):
        guild = self.bot.get_guild(reminder["guild_id"])
        channel = guild.get_channel(reminder["channel_id"])
        member = guild.get_member(reminder["user_id"])
        if not member:
            await self.bot.db_client.delete_reminder(guild.id, reminder["_id"])
            return
        await channel.send(f"{member.mention} you can </daily:1145445177092231343> again!",
                           allowed_mentions=discord.AllowedMentions.all())
        await self.bot.db_client.delete_reminder(guild.id, reminder["_id"])

    async def weekly_reminder(self, reminder):
        guild = self.bot.get_guild(reminder["guild_id"])
        channel = guild.get_channel(reminder["channel_id"])
        member = guild.get_member(reminder["user_id"])
        if not member:
            await self.bot.db_client.delete_reminder(guild.id, ["_id"])
            return
        await channel.send(f"{member.mention} you can </weekly:1145445177092231344> again!",
                           allowed_mentions=discord.AllowedMentions.all())
        await self.bot.db_client.delete_reminder(guild.id, reminder["_id"])

    async def work_reminder(self, reminder):
        guild = self.bot.get_guild(reminder["guild_id"])
        channel = guild.get_channel(reminder["channel_id"])
        member = guild.get_member(reminder["user_id"])
        if not member:
            await self.bot.db_client.delete_reminder(guild.id, reminder["_id"])
            return
        await channel.send(f"{member.mention} you can </work:1145445177092231345> again!",
                           allowed_mentions=discord.AllowedMentions.all())
        await self.bot.db_client.delete_reminder(guild.id, reminder["_id"])

    @tasks.loop(minutes=1)
    async def new_member_loop(self):
        try:
            members = await self.bot.db_client.get_all_new_members()
            for m in members:
                date = datetime.datetime.fromtimestamp(m["date"].timestamp(), datetime.timezone.utc)
                current_date = datetime.datetime.now(datetime.timezone.utc)
                days_difference = (current_date - date).days
                if days_difference >= 7:
                    guild = self.bot.get_guild(m["guild"])
                    member = guild.get_member(m["id"])
                    if not member:
                        await self.bot.db_client.delete_new_member(guild.id, m["id"])
                        continue
                    await self.bot.db_client.delete_new_member(guild.id, member.id)
                    await member.remove_roles(guild.get_role(1178610586423140382))
        except Exception as e:
            print(e)
            pass

    @new_member_loop.before_loop
    async def before_new_member_loop(self):
        await self.bot.wait_until_ready()
        # Start the loop after the bot is ready
        print("Starting the new member loop")

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        try:
            reminders = await self.bot.db_client.get_all_reminders()
            for reminder in reminders:
                now = datetime.datetime.now(datetime.timezone.utc)
                timestamp = datetime.datetime.fromtimestamp(reminder["timestamp"], datetime.timezone.utc)
                due = timestamp + datetime.timedelta(seconds=reminder["interval"])
                if now >= due:
                    if reminder["reminder_type"] == "daily":
                        await self.daily_reminder(reminder)
                    elif reminder["reminder_type"] == "weekly":
                        await self.weekly_reminder(reminder)
                    elif reminder["reminder_type"] == "work":
                        await self.work_reminder(reminder)
        except Exception as e:
            self.bot.log.error(e)
            pass

    @reminder_loop.before_loop
    async def before_reminder_loop(self):
        await self.bot.wait_until_ready()
        # Start the loop after the bot is ready
        print("Starting the reminder loop")

    @tasks.loop(minutes=15)
    async def guild_sync_loop(self):
        try:
            support = self.bot.get_guild(440526421388165120)
            community = self.bot.get_guild(694641646780022818)
            lounge = self.bot.get_guild(449931404151750657)
            #dyna = self.bot.get_guild(1217880601135288493)
            cab = self.bot.get_guild(1091163666071687168)
            contributor = support.get_role(528615882709008430)
            contributor_plus = support.get_role(528615837305929748)
            kissy_contributor = support.get_role(528615659115118602)
            nitro_booster = support.get_role(585533009797578759)
            lounge_booster = lounge.get_role(1323408923901956147)
            #dyna_booster = dyna.get_role(1315146916962766949)
            cab_booster = cab.get_role(1092271098139254844)
            for member in contributor.members:
                if member.id == 248294452307689473:
                    continue
                try:
                    if member in community.members:
                        mem = await community.fetch_member(member.id)
                        # self.bot.log.info(f"Syncing {mem.name} to community")
                        if mem:
                            await mem.add_roles(community.get_role(694641646901395515))
                except Exception as e:
                    pass
            for member in contributor_plus.members:
                if member.id == 248294452307689473:
                    continue
                try:
                    if member in community.members:
                        mem = await community.fetch_member(member.id)
                        # self.bot.log.info(f"Syncing {mem.name} to community")
                        if mem:
                            await mem.add_roles(community.get_role(694641646914109460))
                except Exception as e:
                    pass
            for member in kissy_contributor.members:
                if member.id == 248294452307689473:
                    continue
                try:
                    if member in community.members:
                        mem = await community.fetch_member(member.id)
                        # self.bot.log.info(f"Syncing {mem.name} to community")
                        if mem:
                            await mem.add_roles(community.get_role(694641646838480978))
                except Exception as e:
                    pass
            for member in nitro_booster.members:
                if member.id == 248294452307689473:
                    continue
                try:
                    if member in community.members:
                        mem = await community.fetch_member(member.id)
                        # self.bot.log.info(f"Syncing {mem.name} to community")
                        if mem:
                            await mem.add_roles(community.get_role(872596931598225489))
                except Exception as e:
                    pass
            for member in lounge_booster.members:
                if member.id == 248294452307689473:
                    continue
                try:
                    if member in community.members:
                        mem = await community.fetch_member(member.id)
                        if mem:
                            await mem.add_roles(community.get_role(872596931598225489))
                except Exception as e:
                    pass
            # for member in dyna_booster.members:
            #     if member.id == 248294452307689473:
            #         continue
            #     try:
            #         if member in community.members:
            #             mem = await community.fetch_member(member.id)
            #             if mem:
            #                 await mem.add_roles(community.get_role(872596931598225489))
            #     except Exception as e:
            #         pass
            for member in cab_booster.members:
                if member.id == 248294452307689473:
                    continue
                try:
                    if member in community.members:
                        mem = await community.fetch_member(member.id)
                        if mem:
                            await mem.add_roles(community.get_role(872596931598225489))
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

                    members = list(filter(lambda member: not member.bot, channel.members))

                    if len(members) <= 1:
                        continue

                    for member in members:
                        # Check if any of the following conditions are met:
                        # - Member is deafened by the guild
                        # - Member is muted by the guild
                        # - Member is self-muted
                        # - Member is self-deafened

                        if not (
                                member.voice.deaf or member.voice.mute or member.voice.self_mute or member.voice.self_deaf):
                            user = await self.bot.db_client.get_user(user_id=member.id, guild_id=guild.id)
                            if user:
                                data = await self.bot.db_client.get_guild(guild.id)
                                bonus_xp = sum(
                                    1 for role in member.roles for r in data.bonus_roles if role.id == r.get("role_id"))
                                bonus_xp += 1
                                xp = random.randint(10, 50) * bonus_xp
                                if is_today_weekend_or_holiday():
                                    xp *= 2
                                lvl = calculate_level(user.xp + xp)
                                if lvl > user.level:
                                    lvl_up_bonus = amount_on_level_up(lvl, 1000, 1.07)
                                    channel_id = await data.get_config("lvl_up_channel")
                                    if channel_id:
                                        channel = member.guild.get_channel(int(channel_id))
                                        if channel:
                                            await channel.send(
                                                f"# 🎉Congratulations {member.mention}!\n## <a:lvlup:1138933829185323149> You have leveled up to level {lvl}!\n### <:info:486945488080338944> You have been awarded a boosted ${lvl_up_bonus} as a level up bonus for leveling up in a voice call!")
                                    # self.bot.log.info(f"{member.name} {user.level} -> {lvl}")
                                    await user.update_fields(level=lvl, balance=user.balance + lvl_up_bonus)
                                await user.update_fields(xp=user.xp + xp)

                                #self.bot.log.info(f"{member.name} {xp} -> {user.xp}")

        except Exception as e:
            self.bot.log.error(e)
            pass

    @tasks.loop(minutes=5)
    async def check_jail_loop(self):
        users_in_jail = await self.bot.db_client.get_users_in_jail()

        for user in users_in_jail:
            if user.is_in_jail():
                release_time = user.jail["start_time"].replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(
                    hours=user.jail["duration_hours"])
                current_time = datetime.datetime.now(datetime.timezone.utc)

                if current_time >= release_time:
                    fine = user.jail.get("fine", 0)
                    await user.subtract_balance(fine)
                    await user.update_fields(jail={})
                    self.bot.log.info(
                        f"User {user.user_id} has been released from jail.")


    @tasks.loop(minutes=5)  # Run the task every 5 minutes
    async def change_role_color(self):
        try:
            guild = self.bot.get_guild(694641646780022818)
            role_id_1 = 694641646901395506
            role_id_2 = 694641646922498068
            role_1 = guild.get_role(role_id_1)
            role_2 = guild.get_role(role_id_2)


            r1, g1, b1 = self.generate_random_cmyk_no_yellow_and_convert_to_rgb()
            r2, g2, b2 = self.generate_random_cmyk_no_yellow_and_convert_to_rgb()

            primary_color = self.rgb_to_int(r1, g1, b1)
            secondary_color = self.rgb_to_int(r2, g2, b2)
            url = f"https://discord.com/api/v10/guilds/694641646780022818/roles/{role_id_2}"
            headers = {
                "Authorization": f"Bot {self.bot.http.token}",
                "Content-Type": "application/json"
            }

            json_data = {
                "color": primary_color,  # fallback solid color
                "colors": {
                    "primary_color": primary_color,
                    "secondary_color": secondary_color
                }
            }
            print(json_data)
            r = await self.bot.web_client.patch(url, json=json_data, headers=headers)
            if r.status != 200:
                self.bot.log.error(f"Failed to change role color: {r.status} {await r.text()}")
            else:
                self.bot.log.info(f"Changed role color")

            r1, g1, b1 = self.generate_random_cmyk_no_yellow_and_convert_to_rgb()
            r2, g2, b2 = self.generate_random_cmyk_no_yellow_and_convert_to_rgb()

            primary_color = self.rgb_to_int(r1, g1, b1)
            secondary_color = self.rgb_to_int(r2, g2, b2)
            url = f"https://discord.com/api/v10/guilds/694641646780022818/roles/{role_id_1}"
            headers = {
                "Authorization": f"Bot {self.bot.http.token}",
                "Content-Type": "application/json"
            }

            json_data = {
                "color": primary_color,  # fallback solid color
                "colors": {
                    "primary_color": primary_color,
                    "secondary_color": secondary_color
                }
            }
            print(json_data)
            r = await self.bot.web_client.patch(url, json=json_data, headers=headers)
            if r.status != 200:
                self.bot.log.error(f"Failed to change role color: {r.status} {await r.text()}")
            else:
                self.bot.log.info(f"Changed role color")

        except Exception as e:
            self.bot.log.error(e)
            pass


    def generate_random_cmyk_no_yellow_and_convert_to_rgb(self):
        """
        Generates a random CMYK color with Y=0 and converts it to RGB (0-255 tuple).
        """
        c = random.random()
        m = random.random()
        k = random.random()
        y = 0.0

        r = 1.0 - min(1.0, c + k)
        g = 1.0 - min(1.0, m + k)
        b = 1.0 - min(1.0, y + k)

        r_255 = int(round(r * 255))
        g_255 = int(round(g * 255))
        b_255 = int(round(b * 255))

        return (r_255, g_255, b_255)

    def rgb_to_int(self, r, g, b):
        """
        Convert RGB (0-255 each) to Discord API int color.
        """
        return (r << 16) + (g << 8) + b

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
