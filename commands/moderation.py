import datetime
import re
from io import BytesIO
from typing import List
from typing import Tuple, Union, Optional

import discord
import matplotlib
from discord import AllowedMentions
from discord import app_commands
from discord.ext import commands

from utils.checks import persistent_cooldown
from utils.paginator import Paginator
from utils.utilities import generate_embed_color, search
from views import support_view
from views.confirm_view import Confirm
from views.tickets_view import TicketView
from config.lists import get_all_items

matplotlib.use("agg")
import asyncio
import functools
import matplotlib.pyplot as plt

plt.switch_backend("agg")
from collections import Counter

ID_RE = re.compile(r"\d{15,21}")
LIMIT = 1000000
# TODO: add a way to add/remove users to this list. guild.config?
untouchables = [248294452307689473, 596330574109474848, 270393700394205185, 383932871985070085]


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.nickname_task: Optional[asyncio.Task] = None

    @staticmethod
    async def get_ban_limit(guild, limit: int) -> Tuple[int, list]:
        bans = [entry async for entry in guild.bans(limit=limit)]
        ban_count = len(bans)
        limit = min(LIMIT, min(limit, ban_count))
        return limit, bans

    @staticmethod
    def get_name(user: Union[discord.User, int]) -> str:
        name = str(user)
        if len(name) > 23:
            name = name[:20] + "..."
        return name.replace("$", "\\$")

    async def get_chart_file(self, ctx: commands.Context, counter: Counter):
        task = functools.partial(self.create_chart, counter, f"Mods for the last {sum(counter.values())} bans")
        task = self.bot.loop.run_in_executor(None, task)
        try:
            ban_chart = await asyncio.wait_for(task, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send("An error occurred while generating this image. Try again later.")
        return discord.File(ban_chart, "ban_chart.png")

    @staticmethod
    def create_chart(data: Counter, title: str):
        plt.clf()
        plt.style.use("dark_background")
        most_common = data.most_common()
        total = sum(data.values())
        sizes = [(x[1] / total) * 100 for x in most_common][:20]
        labels = [
            f"{x[0]} {round(sizes[index], 1):g}%" for index, x in enumerate(most_common[:20])
        ]
        if len(most_common) > 20:
            others = sum(x[1] / total for x in most_common[20:])
            sizes.append(others)
            labels.append("Others {:g}%".format(others))
        title = plt.title(title)
        title.set_va("top")
        title.set_ha("center")
        plt.gca().axis("equal")
        colors = [
            "r",
            "darkorange",
            "gold",
            "y",
            "olivedrab",
            "green",
            "darkcyan",
            "mediumblue",
            "darkblue",
            "blueviolet",
            "indigo",
            "orchid",
            "mediumvioletred",
            "crimson",
            "chocolate",
            "yellow",
            "limegreen",
            "forestgreen",
            "dodgerblue",
            "slateblue",
            "gray",
        ]
        pie = plt.pie(sizes, colors=colors, startangle=0)
        plt.legend(
            pie[0],
            labels,
            bbox_to_anchor=(0.7, 0.5),
            loc="center",
            fontsize=10,
            bbox_transform=plt.gcf().transFigure,
        )
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
        image_object = BytesIO()
        plt.savefig(image_object, format="PNG", transparent=True)
        image_object.seek(0)
        return image_object

    async def do_idiot(self, user: discord.Member, mod_id: int, nickname: str):
        user_data = await self.bot.db_client.get_user(user_id=user.id, guild_id=user.guild.id)
        if user_data.idiot.get("idiot", None):
            idiot_data = user_data.idiot
            idiot_data["idiot"] = True
            idiot_data["nickname"] = nickname
            idiot_data["idiot_by"] = mod_id
            idiot_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
            idiot_data["times_idiot"] += 1
            idiot_data["change"] = 0
            await user_data.update_fields(idiot=idiot_data)
            await user.edit(nick=nickname, reason="what a idiot")
            return
        idiot_data = {
            "nickname": nickname,
            "idiot": True,
            "idiot_by": mod_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            "times_idiot": 1,
            "change": 0
        }
        await user_data.update_fields(idiot=idiot_data)
        await user.edit(nick=nickname, reason="what a idiot")
        return

    @commands.bot_has_permissions(ban_members=True, view_audit_log=True)
    @commands.hybrid_command(name="ban_chart", description="Display a chart of the moderators with the most bans.")
    @app_commands.describe(limit="The number of bans to check, between 1 and 1,000,000")
    @commands.guild_only()
    async def ban_chart(self, ctx: commands.Context, limit: Optional[int] = LIMIT):
        """
        Display a chart of the moderators with the most bans.

        This can take a while for servers with lots of bans.
        """
        await ctx.typing(ephemeral=False)
        await ctx.reply(f"Gathering stats up to the last {limit} bans.")
        limit, bans = await self.get_ban_limit(ctx.guild, limit)
        if not bans:
            return await ctx.reply(":x: No bans found.")

        counter = Counter()
        async for entry in ctx.guild.audit_logs(
                action=discord.AuditLogAction.ban, limit=limit
        ):
            if entry.user.bot and entry.reason:
                match = ID_RE.search(entry.reason)
                if match:
                    mod_id = int(match.group(0))
                    user = self.bot.get_user(mod_id) or mod_id
                else:
                    user = entry.user
            else:
                user = entry.user
            counter[self.get_name(user)] += 1
        chart_file = await self.get_chart_file(ctx, counter)
        await ctx.reply(file=chart_file)

    @commands.hybrid_group(name="idiot", description="idiot commands")
    @commands.has_permissions(manage_nicknames=True)
    @commands.guild_only()
    async def idiot(self, ctx):
        await ctx.send("Please use subcommands: set, clear, check, or list.")

    @idiot.command(name="set", description="set a idiots nickname")
    @app_commands.describe(user="The user to set the nickname of.")
    @app_commands.describe(nickname="The nickname to set.")
    async def idiot_set(self, ctx, user: discord.Member, *, nickname: str):
        user_data = await self.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        if user_data.idiot.get("idiot"):
            view = Confirm()
            color = await generate_embed_color(ctx.author)
            em = discord.Embed(color=color)
            em.description = f"{user.mention} is already an idiot, changed by <@{user_data.idiot.get('idiot_by')}>, are you sure you want to change their nickname?"
            view.message = await ctx.reply(embed=em, view=view)
            await view.wait()
            if view.value is None:
                await ctx.reply("Timed out.")
                return
            elif view.value is False:
                await ctx.reply("Ok, I wont change it.")
                return
            else:
                if any(user_data.idiot.get("idiot_by") == no_touch for no_touch in untouchables):
                    if not any(ctx.author.id == no_touch for no_touch in untouchables):
                        await self.do_idiot(ctx.author, ctx.author.id, nickname)
                        await ctx.reply(f"LOL you tried.")
                        return
                await self.do_idiot(user, ctx.author.id, nickname)
                await ctx.reply(f"Set {user.mention}'s nickname to {nickname}.")
                return
        user_data = await self.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        await self.do_idiot(user, ctx.author.id, nickname)
        await ctx.reply(f"Set {user.mention}'s nickname to {nickname}.")
        return

    @idiot.command(name="clear", description="clear a idiots nickname")
    @app_commands.describe(user="The user to clear the nickname of.")
    async def idiot_clear(self, ctx, user: discord.Member):
        user_data = await self.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        if user_data.idiot.get("idiot"):
            if any(user_data.idiot.get("idiot_by") == no_touch for no_touch in untouchables):
                if not any(ctx.author.id == no_touch for no_touch in untouchables):
                    await ctx.reply("You can't clear this idiots nickname, suffer instead.")
                    return
            user_data.idiot["idiot"] = False
            user_data.idiot["nickname"] = None
            user_data.idiot["idiot_by"] = None
            user_data.idiot["timestamp"] = None
            user_data.idiot["change"] = None
            await user_data.update_fields(idiot=user_data.idiot)
            await user.edit(nick=None, reason="what a idiot")
            await ctx.reply(f"Cleared {user.mention}'s nickname.")
        else:
            await ctx.reply(f"{user.mention} is not an idiot.")

    @idiot.command(name="check", description="check if a user is an idiot")
    @app_commands.describe(user="The user to check.")
    async def idiot_check(self, ctx, user: discord.Member):
        user_data = await self.bot.db_client.get_user(user_id=user.id, guild_id=ctx.guild.id)
        if user_data.idiot.get("idiot"):
            color = await generate_embed_color(ctx.author)
            em = discord.Embed(color=color)
            em.description = (f"{user.mention} is an idiot\n"
                              f"**Changed by**: <@{user_data.idiot.get('idiot_by')}>\n"
                              f"**Tried to change**: {user_data.idiot['change']}\n"
                              f"**Times idioted**: {user_data.idiot['times_idiot']}.")
            await ctx.reply(embed=em)
        else:
            await ctx.reply(f"{user.mention} is not an idiot.")

    @idiot.command(name="list", description="list all idiots")
    async def idiot_list(self, ctx):
        idiots = []
        guild_data = await self.bot.db_client.get_guild(ctx.guild.id)
        for user in guild_data.users:
            if 'idiot' in user:
                print(user)
                if user.get("idiot").get("idiot", False):
                    idiots.append(
                        f"**user**: <@{user['user_id']}>\n"
                        f"**Idiot**: {user.get('idiot').get('nickname')}\n"
                        f"**Changed by**: <@{user.get('idiot').get('idiot_by')}>\n"
                        f"**Tried to change**: {user.get('idiot').get('change')}\n"
                        f"**Times idioted**: {user.get('idiot').get('times_idiot')}.")
        em = discord.Embed(color=await generate_embed_color(ctx.author))
        em.title = "Idiots"
        em.description = "\n\n".join(idiots)
        await ctx.reply(embed=em)

    @app_commands.command(name="selfban", description="Ban yourself from the server.")
    @commands.guild_only()
    async def selfban(self, interaction: discord.Interaction):
        # should be removed
        if interaction.user.id == 596330574109474848:
            return await interaction.response.send_message(
                "Tom said No, Stop fucking trying <:pikascream:585952447801982977>")

        if any(role.id == 694641646922498069 for role in interaction.user.roles):
            return await interaction.response.send_message(
                "You can't selfban from the community server, you absolute idiot, suffer instead.")

        em = discord.Embed(color=interaction.user.color,
                           description="This is a one-way trip. You will not be able to rejoin the server unless you draw an unpunishment cat.")
        em.set_author(name="Are you sure about this? It really will ban you.")
        view = Confirm()
        await interaction.response.send_message(embed=em, view=view, ephemeral=True)
        view.message = await interaction.original_response()
        await view.wait()
        if view.value is None:
            await interaction.followup.send("Timed out.", ephemeral=True)
        elif view.value is False:
            await interaction.followup.send("You absolute coward.", ephemeral=True)
        else:
            try:
                await interaction.user.ban(delete_message_days=0,
                                           reason="wah wah, selfbanned.")
            except:
                await interaction.followup.send("You can't selfban, suffer instead.")
            else:
                await interaction.followup.send(f"{interaction.user} decided to selfban. Fucking idiot.")

    @commands.hybrid_group(name="massnick", description="massnick users")
    @commands.guild_only()
    async def massnick(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @massnick.command(name="start", description="begin a massnick")
    @commands.has_permissions(manage_nicknames=True)
    @app_commands.describe(nickname="What you want the massnick to be. This is mutually exclusive to random.",
                           role="The role you want to massnick.",
                           random="Whether to use a random name for each member.",
                           idiot="Whether to prevent users from changing their nicknames.")
    async def massnick_start(self, ctx: commands.Context, nickname: Optional[str],
                             role: Optional[discord.Role], random: Optional[bool],
                             idiot: Optional[bool]):
        if self.nickname_task is not None:
            return await ctx.send("I'm already doing a massnick, chill tf out", ephemeral=True)

        role = role or ctx.guild.get_role(694641646780022826)

        view = Confirm()
        view.message = await ctx.send(f"{ctx.author.mention}, are you sure you want me to run this massnick?",
                                      view=view)
        await view.wait()

        if view.value is None:
            return await ctx.send("Timed out.")

        if view.value is False:
            return await ctx.send("Fine I wont massnick the plebs.")

        self.nickname_task = asyncio.create_task(
            self._do_massnick(ctx, role.members, nickname, random is True, idiot is True))
        await ctx.send("Okie dokie, I'll hit you up when I'm finished :)")

    @massnick.command(name="cancel", description="Cancel your currently running massnick")
    @commands.has_permissions(manage_nicknames=True)
    async def massnick_cancel(self, ctx: commands.Context):
        if self.nickname_task is not None:
            if self.nickname_task.cancelling() > 0:
                return await ctx.send("The massnick is already pending cancellation.", ephemeral=True)

            if self.nickname_task.cancelled():
                self.nickname_task = None
            else:
                self.nickname_task.cancel()

            return await ctx.send("The massnick has been cancelled.", ephemeral=True)

        return await ctx.send("What are you cancelling if I'm not running a massnick?", ephemeral=True)

    @massnick.command(name="reset", description="Reset everyones names")
    @commands.has_permissions(manage_nicknames=True)
    @app_commands.describe(role="Will reset everyone with this role's name")
    async def massnick_reset(self, ctx: commands.Context, role: Optional[discord.Role]):
        # if self.nickname_task is not None:
        #     await self.nickname_task.cancel()
        #     await asyncio.sleep(1.5)  # Give the task time to cancel.

        role = role or ctx.guild.get_role(694641646780022826)
        view = Confirm()
        view.message = await ctx.send(f"{ctx.author.mention}, are you sure you want me to reset the members names?",
                                      view=view)
        await view.wait()

        if view.value is None:
            return await ctx.send("Timed out.")

        if view.value is False:
            return await ctx.send("Fine I wont reset.")

        await ctx.send("Okie dokie, I'll hit you up when I'm finished :)")
        self.nickname_task = asyncio.create_task(self._do_massnick(ctx, role.members, nickname=None))

    async def _do_massnick(self, ctx: commands.Context, members: List[discord.Member],
                           nickname: Optional[str], random: bool = False, idiot: bool = False):
        """
        Sets the nickname on all the members provided.
        ``nickname`` and ``random`` are mutually exclusive parameters.

        Parameters
        ----------
        nickname: Optional[str]
            The new nickname for each member. This can be ``None`` to reset. Any value provided
            for this, is ignored if ``random`` is ``True``.
        random: bool
            Whether the nickname should be randomly generated. This must be ``False``
            if nickname is set
        idiot: bool
            Whether members should be able to change their nicknames.
        """
        updated = 0
        failed = 0
        cancelled = False
        print(nickname)
        try:
            for member in members:
                print(member)
                if member.top_role >= ctx.guild.me.top_role:
                    continue

                try:
                    new_name = (await (await self.bot.web_client.get("https://nekos.life/api/v2/name")).json())[
                        'name'] if random is True else nickname
                    print(new_name)
                    # if idiot:

                    if member.display_name == new_name or new_name is not None and new_name > 32:
                        print(f"Skipping {member}'s nickname as it's the same as the current one or too long.")
                        continue
                    print(f"Changing {member}'s nickname to {new_name}.")
                    await member.edit(nick=new_name)
                    print("done")
                    updated += 1
                    print(f"Changed {member}'s nickname to {new_name}.")
                except (discord.Forbidden, discord.HTTPException):
                    failed += 1
                    print(f"Failed to change {member}'s nickname.")
        except asyncio.CancelledError:
            print("cancelled")
            cancelled = True

        self.nickname_task = None
        print("done")
        await ctx.author.send(
            f'Massnick results (updated: {updated} / failed: {failed}){" [cancelled]" if cancelled else ""}')

    @commands.hybrid_command(name="purge", description="Purge messages from a channel")
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(limit="The number of messages to purge.")
    @app_commands.describe(channel="The channel to purge messages from.")
    @app_commands.describe(from_bot="Set to True to purge bot messages only. Default is False.")
    @app_commands.describe(from_user="Set user to purge messages from a specific user.")
    @app_commands.describe(images_only="Set to True to purge messages with images only. Default is False.")
    @commands.guild_only()
    async def purge(self, ctx: commands.Context, limit: int,
                    channel: Optional[discord.TextChannel] = None,
                    from_bot: Optional[bool] = False,
                    from_user: Optional[discord.User] = None,
                    images_only: Optional[bool] = False):
        await ctx.defer()

        channel = channel or ctx.channel

        def check(message):
            if not from_bot and not from_user and not images_only and from_user is None:
                return True
            if from_bot and message.author.bot:
                return True
            if from_user and message.author == from_user:
                return True
            if images_only and len(message.attachments) > 0:
                return True
            return False

        two_weeks_ago = datetime.datetime.utcnow() - datetime.timedelta(weeks=2)
        counter = 0
        try:
            messages = [message async for message in channel.history(limit=limit) if check(message)]
        except Exception as e:
            return await ctx.send(f"Error occurred while fetching messages")
        new_messages = [message for message in messages if
                        message.created_at > two_weeks_ago.replace(tzinfo=datetime.timezone.utc)]
        counter += len(new_messages)
        # First, try to bulk delete messages younger than two weeks.
        try:
            await channel.delete_messages(new_messages, reason=f"Purged by {ctx.author}")
        except Exception as e:
            print(f"Error occurred while bulk deleting: {e}")

        # Then, delete older messages one by one.
        old_messages = [message for message in messages if
                        message.created_at < two_weeks_ago.replace(tzinfo=datetime.timezone.utc)]
        counter += len(old_messages)
        for message in old_messages:
            try:
                await message.delete()
            except Exception as e:
                print(f"Error occurred while deleting an old message: {e}")
            await asyncio.sleep(0.3)  # Ensure we respect the rate limit
        await ctx.channel.send(f"Purged {counter} messages from {channel.mention}", delete_after=5)

    @commands.hybrid_command(name="kick", description="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(user="The user to kick.")
    @app_commands.describe(reason="The reason for kicking the user.")
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str):
        await user.kick(reason=reason)
        await ctx.send(f"Kicked {user.mention} for {reason}", ephemeral=True)

    @commands.hybrid_command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(user="The user to ban.")
    @app_commands.describe(reason="The reason for banning the user.")
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason: str):
        await user.ban(reason=reason)
        await ctx.send(f"Banned {user.mention} for {reason}", ephemeral=True)

    @commands.hybrid_group(name="shop", description="Shop Commands")
    @commands.guild_only()
    async def shop(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @shop.group(name="roles", description="Role Commands")
    async def roles(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @roles.command(name="list", description="List all roles in the shop")
    async def shop_role_list(self, ctx: commands.Context):
        roles = await self.bot.db_client.get_shop_roles(guild_id=ctx.guild.id)
        em = discord.Embed(title="Shop Roles", color=await generate_embed_color(ctx.author))
        for role_data in roles:
            role = ctx.guild.get_role(int(role_data.get('_id')))
            em.add_field(name="",
                         value=f"\nRole: {role.mention}\nPrice: {role_data.get('price')}\nDescription: {role_data.get('description')}",
                         inline=False)
        await ctx.send(embed=em)

    @roles.command(name="buy", description="Buy a role from the shop")
    @app_commands.describe(role="The role to buy.")
    async def buy_role(self, ctx: commands.Context, role: str):
        role_data = await self.bot.db_client.get_shop_roles(guild_id=ctx.guild.id)
        role_data = next((r for r in role_data if str(r.get("_id")) == role), None)

        if not role_data:
            return await ctx.send("That role doesn't exist in the shop.")

        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        if user_data.balance < role_data.get("price"):
            return await ctx.send("You don't have enough money to buy that role.")
        role = ctx.guild.get_role(int(role_data.get('_id')))
        retrieved_role = user_data.get_item_by_key("role_id", role.id, "roles")
        if retrieved_role is not None:
            return await ctx.send("You already own that role.")
        await user_data.set_item_by_key("_id", role_data.get('_id'), role_data, "roles")
        await user_data.update_fields(balance=user_data.balance - role_data.get("price"))
        await ctx.send(f"Bought {role_data.get('name')} for {role_data.get('price')}.")

    @buy_role.autocomplete('role')
    async def buy_role_autocomplete(self,
                                    interaction: discord.Interaction,
                                    current: str,
                                    ) -> List[app_commands.Choice[str]]:
        roles = await self.bot.db_client.get_shop_roles(guild_id=interaction.guild.id)

        return [
                   app_commands.Choice(name=role.get('name'), value=str(role.get('_id')))
                   for role in roles
                   if not current or search(role.get('name').lower(), current.lower())
               ][:25]

    @shop.group(name="items", description="Item Commands")
    async def items(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @items.command(name="list", description="List all items in the shop")
    async def item_list(self, ctx: commands.Context):
        items = get_all_items()
        # Create an empty list for embeds
        embeds = []

        # Define a title for the first page
        first_page_title = "Shop Items"

        # Split the items list into chunks of maximum 10 items per embed
        for i in range(0, len(items), 10):
            chunk = items[i:i + 10]
            # Create a new embed for each chunk
            em = discord.Embed(title=first_page_title if i == 0 else "", color=await generate_embed_color(ctx.author))
            # Add the sorted items to the description of the embed
            for item_data in chunk:
                item_text = (f"\n**Item**: {item_data.get('name')} {item_data.get('emote')}"
                             f"\n**Required Level**: {item_data.get('required_level')}"
                             f"\n**Rarity**: {item_data.get('rarity')}"
                             f"\n**Price**: ${item_data.get('price'):,}"
                             f"\n**Description**: {item_data.get('description')}"
                             f"\n\n")
                em.add_field(name="", value=item_text, inline=False)
            # Append the embed to the list of embeds
            embeds.append(em)
        await Paginator(delete_on_timeout=False, timeout=60).start(ctx, pages=embeds)

    @items.command(name="buy", description="Buy an item from the shop")
    @app_commands.describe(item="The item to buy.")
    async def buy_item(self, ctx: commands.Context, item: str):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        item_data = next((i for i in get_all_items() if i.get("name") == item), None)
        if user_data.level < item_data.get("required_level"):
            return await ctx.send(f":x: You don't have a high enough level to buy that item."
                                  f"\nYou are level {user_data.level} "
                                  f"and you need to be level {item_data.get('required_level')}")
        if user_data.balance < item_data.get("price"):
            return await ctx.send(":x: You don't have enough money to buy that item.")
        owned_item = user_data.get_item_by_key("name", item_data.get("name"), "items")
        await user_data.update_fields(balance=user_data.balance - item_data.get("price"))
        if owned_item is not None:
            owned_item["quantity"] += 1
            await user_data.set_item_by_key("name", item_data.get("name"), owned_item, "items")
            return await ctx.send(f"Bought {item_data.get('name')} for {item_data.get('price')}.")
        else:
            item_data["quantity"] = 1
            await user_data.set_item_by_key("name", item_data.get("name"), item_data, "items")
            await ctx.send(f"Bought {item_data.get('emote')} {item_data.get('name')} for {item_data.get('price')}.")

    @buy_item.autocomplete('item')
    async def buy_item_autocomplete(self,
                                    interaction: discord.Interaction,
                                    current: str,
                                    ) -> List[app_commands.Choice[str]]:
        items = get_all_items()

        return [
                   app_commands.Choice(name=item.get('name'), value=str(item.get('name')))
                   for item in items
                   if not current or search(item.get('name').lower(), current.lower())
               ][:25]

    @shop.group(name="gift", description="buy Commands")
    async def gift(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @gift.command(name="list", description="List all gifts in the shop")
    async def list_gifts(self, ctx: commands.Context):
        gifts = await self.bot.db_client.get_shop_gifts(guild_id=ctx.guild.id)
        # Sort the list of dictionaries by the 'value' key
        sorted_gifts = sorted(gifts, key=lambda x: x['value'], reverse=True)
        if len(sorted_gifts) == 0:
            return await ctx.send("There are no gifts in the shop.")
        # Create an empty list for embeds
        embeds = []

        # Define a title for the first page
        first_page_title = "Gift list"

        # Split the sorted list into chunks of maximum 10 items per embed
        for i in range(0, len(sorted_gifts), 10):
            chunk = sorted_gifts[i:i + 10]
            # Create a new embed for each chunk
            em = discord.Embed(title=first_page_title if i == 0 else "", description="")
            em.set_author(
                name="Gift list Command",
                icon_url=self.bot.user.display_avatar.with_static_format("png"),
                url="https://discord.gg/invite/tailss")
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
            em.set_footer(
                text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                icon_url=ctx.author.display_avatar.with_static_format("png"))
            # Add the sorted gifts to the description of the embed
            for gift_data in chunk:
                e = "➕" if gift_data.get("positive") else "➖"
                em.description += f"\nGift: {gift_data.get('name')} {gift_data.get('emote')}\nPrice: {gift_data.get('price'):,}\nValue: {e} {gift_data.get('value'):,}\n"
            # Append the embed to the list of embeds
            embeds.append(em)
        await Paginator(delete_on_timeout=False, timeout=120).start(ctx, pages=embeds)
        # em = discord.Embed(title="Shop Gifts", color=await generate_embed_color(ctx.author))
        # for gift_data in gifts:
        #     e = "➕" if gift_data.get("positive") else "➖"
        #     em.add_field(name="",
        #                  value=f"\nGift: {gift_data.get('name')} {gift_data.get('emote')}\nPrice: {gift_data.get('price')}\nValue: {e} {gift_data.get('value')}\n",
        #                  inline=False)
        # await ctx.send(embed=em)

    @gift.command(name="buy", description="Buy a gift from the shop")
    @app_commands.describe(gift="The gift to buy.")
    @app_commands.describe(quantity="The quantity of the gift to buy.")
    async def buy_gift(self, ctx: commands.Context, gift: str, quantity: int = 1):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        gift_data = await self.bot.db_client.get_shop_gifts(guild_id=ctx.guild.id)
        gift_data = next((gd for gd in gift_data if str(gd.get("_id")) == str(gift)), None)
        if not gift_data:
            return await ctx.send("That gift doesn't exist in the shop.")
        if user_data.balance < gift_data.get("price"):
            return await ctx.send("You don't have enough money to buy that gift.")
        owned_gift = user_data.get_item_by_key("_id", gift_data.get("_id"), "gifts")
        await user_data.update_fields(balance=user_data.balance - gift_data.get("price") * quantity)
        if owned_gift is not None:
            owned_gift["quantity"] += quantity
            await user_data.set_item_by_key("_id", gift_data.get("_id"), owned_gift, "gifts")
            return await ctx.send(f"Bought {gift_data.get('name')} for {gift_data.get('price')}.")
        else:
            gift_data["quantity"] = quantity
            await user_data.set_item_by_key("_id", gift_data.get("_id"), gift_data, "gifts")
            await ctx.send(f"Bought {quantity} {gift_data.get('name')} for {gift_data.get('price')}.")

    @buy_gift.autocomplete('gift')
    async def buy_gift_autocomplete(self,
                                    interaction: discord.Interaction,
                                    current: str,
                                    ) -> List[app_commands.Choice[str]]:
        gifts = await self.bot.db_client.get_shop_gifts(guild_id=interaction.guild.id)

        return [
                   app_commands.Choice(name=gift.get('name'), value=str(gift.get('_id')))
                   for gift in gifts
                   if not current or search(gift.get('name').lower(), current.lower())
               ][:25]

    @commands.hybrid_command(name="ratio", description="Check how many nsfw vs sfw channels there are")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def ratio(self, ctx):
        sfw = 0
        nsfw_channel_names = []
        nsfw = 0
        allchannels = len(ctx.guild.channels)
        for ch in ctx.guild.channels:
            if ch.nsfw:
                nsfw += 1
                nsfw_channel_names.append(ch.name)
            else:
                sfw += 1

        if nsfw_channel_names:
            nsfw_channel_names_str = "\n".join(nsfw_channel_names)
            description = f"Age-restricted channels: \n{nsfw_channel_names_str}"
            em = discord.Embed(title="NSFW Channel List", description=description, colour=discord.Color.random())
            await ctx.reply(embed=em)

        em = discord.Embed(title="Ratio Check", colour=discord.Color.random())
        em.add_field(name="SFW:", value=sfw)
        em.add_field(name="NSFW:", value=nsfw)
        em.add_field(name="All Channels:", value=allchannels)
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="new_ticket", description="Create a new ticket")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def support(self, ctx: commands.Context, user: discord.Member):
        retrieved_guild = await self.bot.db_client.get_guild(ctx.guild.id)
        try:
            dm_channel = await user.create_dm()
            await dm_channel.send("Hello! opening a support ticket for you.")
        except discord.Forbidden:
            return await ctx.send("I couldn't DM you! Do you have DMs disabled?",
                                  ephemeral=True)

        category_id = 1141700782006222970
        category = ctx.guild.get_channel(category_id)
        staff = ctx.guild.get_role(694641646918434875)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
            staff: discord.PermissionOverwrite(send_messages=True, read_messages=True, embed_links=True,
                                               read_message_history=True, attach_files=True)
        }
        new_channel = await ctx.guild.create_text_channel(user.name, category=category,
                                                          overwrites=overwrites)
        await ctx.send("Opened support ticket, check your DMs!", ephemeral=True)
        ticket_data = {
            "channel_id": new_channel.id,
            "dm_channel_id": dm_channel.id,
            "user_id": user.id,
            "status": "open",
            "resolved_by": None,
            "resolved_at": None,
            "created_at": datetime.datetime.utcnow(),
            "reason": "Support"
        }

        await self.bot.db_client.add_support_ticket(ctx.guild.id, ticket_data)
        await dm_channel.send("Your ticket has been created. Please describe your issue.")
        await new_channel.send(
            f"<@&981426793925992448> Support Ticket by {user.mention}",
            view=support_view.SupportTicketView())

    @commands.hybrid_command(name="new_verify", description="Create a new verify ticket")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def verify(self, ctx, user: discord.Member):
        retrieved_guild = await self.bot.db_client.get_guild(ctx.guild.id)
        count = len([ticket for ticket in retrieved_guild.tickets if
                     ticket.get("user_id") == user.id and
                     ticket.get("status") == "closed" and
                     ticket.get("reason") == "Verification"])
        # Create a new ticket
        category = discord.utils.get(ctx.guild.categories, id=1141700782006222970)

        if category:
            staff = ctx.guild.get_role(694641646918434875)
            overwrites = {
                user: discord.PermissionOverwrite(send_messages=True, read_messages=True, embed_links=True,
                                                  read_message_history=True, attach_files=True),
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
                staff: discord.PermissionOverwrite(send_messages=True, read_messages=True, embed_links=True,
                                                   read_message_history=True, attach_files=True)
            }
            new_channel = await ctx.guild.create_text_channel(user.name, category=category,
                                                              overwrites=overwrites)
            await ctx.reply(f"Opened ticket {new_channel.mention}", ephemeral=True)
            ticket_data = {
                "channel_id": new_channel.id,
                "user_id": user.id,
                "status": "open",
                "resolved_by": None,
                "resolved_at": None,
                "created_at": datetime.datetime.utcnow(),
                "reason": "Verification"
            }
            print(ticket_data)
            await self.bot.db_client.add_ticket(ctx.guild.id, ticket_data)

            # Deny permissions for everyone
            # await new_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
            # Allow permissions for the specified user
            # await new_channel.set_permissions(interaction.user, send_messages=True, read_messages=True)
            # Send the ticket message
            await new_channel.send(
                f"<@&981426793925992448> Ticket by {user.mention}, {count} previous verification tickets",
                view=TicketView())
            # Send the verification message
            embed = discord.Embed(title="Ticket",
                                  description=f"Welcome {user.mention}! Thank you for contacting BoobBot support. Please send the photos required to verify following the below guidelines. All images sent will be deleted upon completion of the ticket. Please note that if you do not follow the guidelines, your ticket will be closed and you will be banned from the server. \n\n",
                                  color=0x00ff00)
            embed.set_image(url=ctx.bot.config.verification_image)
            await new_channel.send(embed=embed)

    @commands.hybrid_command(name="pings", description="role pings")
    @persistent_cooldown(1, 120, commands.BucketType.user)
    @app_commands.describe(ping="The ping to use.")
    @commands.guild_only()
    async def pings(self, ctx: commands.Context, ping: str):
        guild_data = await self.bot.db_client.get_guild(ctx.guild.id)
        ping_data = next((gd for gd in guild_data.ping_tags if str(gd.get("role")) == str(ping)), None)
        if not ping_data:
            return await ctx.send("That ping doesn't exist")
        await ctx.send(f"<@&{ping_data.get('role')}>", allowed_mentions=AllowedMentions.all())

    @pings.autocomplete('ping')
    async def pings_autocomplete(self,
                                 interaction: discord.Interaction,
                                 current: str,
                                 ) -> List[app_commands.Choice[str]]:
        guild_data = await self.bot.db_client.get_guild(interaction.guild.id)

        return [
                   app_commands.Choice(name=ping.get('ping'), value=str(ping.get('role')))
                   for ping in guild_data.ping_tags
                   if not current or search(ping.get('ping').lower(), current.lower())
               ][:25]


async def setup(bot):
    await bot.add_cog(Moderation(bot))
