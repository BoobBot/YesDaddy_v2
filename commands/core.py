import datetime
import random

import discord
import emoji
from discord import app_commands
from discord.ext import commands

from utils.paginator import Paginator
from utils.utilities import generate_embed_color
from views.help_view import HelpView
from views.stats_view import StatsView


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_emote(self, emote):
        for e in self.bot.emojis:
            if emote == str(e):
                return True
        return emoji.is_emoji(emote)

    @commands.hybrid_command(name="say", description="Make the bot say something.")
    @commands.guild_only()
    @commands.is_owner()
    async def say(self, ctx, *, message):
        msg = f"{ctx.author.mention} says: \n{message}"
        await ctx.send(msg)

    @commands.hybrid_command(name="stats", description="View bot stats.")
    @commands.guild_only()
    async def stats_command(self, ctx):
        em = discord.Embed(title="Stats List", colour=discord.Colour.blue())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        await user_data.update_stat(command=ctx.command.name)
        em.set_author(
            name="Stats Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        view = StatsView(ctx, user_data.stats)
        await ctx.reply(embed=em, view=view)

    @commands.hybrid_command(name="ping", description="Show bot and API latency.")
    @commands.guild_only()
    async def ping(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        await user_data.update_stat(command=ctx.command.name)
        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="Pong!", description=f"Bot latency: {self.bot.latency * 1000:.2f} ms")
        em.set_author(
            name="Ping Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="invite", description="Invite the bot to your server.")
    @commands.guild_only()
    async def invite(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        await user_data.update_stat(command=ctx.command.name)
        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="add me!",
                           description=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot+applications.commands")
        em.set_author(
            name="Invite Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="support", description="Join the support server.")
    @commands.guild_only()
    async def support(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        await user_data.update_stat(command=ctx.command.name)
        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="Get support", description="https://discord.gg/invite/bra")
        em.set_author(
            name="Support Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.reply(embed=em)

    @commands.hybrid_command(name="github", description="View the bot's GitHub repository.")
    @commands.guild_only()
    async def github(self, ctx):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        await user_data.update_stat(command=ctx.command.name)
        color = await generate_embed_color(ctx.author)
        em = discord.Embed(color=color, title="GitHub", description="https://github.com/BoobBot/YesDaddy_v2")
        em.set_author(
            name="Github Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        await ctx.reply(embed=em)

    @commands.hybrid_group(name="settings", description="Shop Commands")
    @commands.guild_only()
    async def guild_settings(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @guild_settings.group(name="lvlroles", description="View or change level roles.")
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def lvlrole(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @lvlrole.command(name="add", description="Add a level role.")
    @app_commands.describe(level="The level to add the role for.")
    @app_commands.describe(role="The role to add.")
    @commands.has_guild_permissions(ban_members=True)
    async def lvlrole_add(self, ctx, level: int, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)

        if any(r.get('role_id') == role.id for r in guild.lvl_roles):
            return await ctx.reply(":x: That role is already a level role.")

        guild.lvl_roles.append(
            {"level": level, "role_id": role.id})  # TODO dedicated method to handle updating just this field
        await self.bot.db_client.update_guild(ctx.guild.id, guild.to_dict())  # Call Guild.save()?
        await ctx.reply(f"Added {role.mention} as a level role for level {level}.")

    @lvlrole.command(name="remove", description="Remove a level role.")
    @commands.has_guild_permissions(ban_members=True)
    async def lvlrole_remove(self, ctx, level: int, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        guild.lvl_roles.remove(
            {"level": level, "role_id": role.id})  # TODO dedicated method to handle updating just this field
        await self.bot.db_client.update_guild(ctx.guild.id, guild.to_dict())
        await ctx.reply(f"Removed {role.mention} as a level role for level {level}.")

    @lvlrole.command(name="list", description="List all level roles.")
    async def lvlrole_list(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        roles = guild.lvl_roles
        if not roles:
            return await ctx.reply("There are no level roles.")
        color = await generate_embed_color(ctx.author)
        embed = discord.Embed(color=color, title="Level Roles")
        embed.set_author(
            name="level role list",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        embed.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png")
        )
        for role in roles:
            embed.add_field(name=f"Level {role.get('level')}", value=f"<@&{role.get('role_id')}>")
        await ctx.reply(embed=embed)

    @guild_settings.group(name="bonus_roles", description="View or change bonus roles.")
    @commands.has_guild_permissions(ban_members=True)
    async def bonus_role(self, ctx):
        await ctx.send("Please use a valid subcommand")

    @bonus_role.command(name="add", description="Add a bonus role.")
    @app_commands.describe(role="The role to add.")
    @commands.has_guild_permissions(ban_members=True)
    async def bonus_role_add(self, ctx, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        if role.id in [role.get("role_id") for role in guild.bonus_roles]:
            return await ctx.reply("That role is already a bonus role.")
        guild.bonus_roles.append({"role_id": role.id})  # TODO dedicated method to handle updating just this field
        await self.bot.db_client.update_guild(ctx.guild.id, guild.to_dict())
        await ctx.reply(f"Added {role.mention} as a bonus role.")

    @bonus_role.command(name="remove", description="Remove a bonus role.")
    @app_commands.describe(role="The role to remove.")
    @commands.has_guild_permissions(ban_members=True)
    async def bonus_role_remove(self, ctx, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        guild.bonus_roles.remove({"role_id": role.id})  # TODO dedicated method to handle updating just this field
        await self.bot.db_client.update_guild(ctx.guild.id, guild.to_dict())
        await ctx.reply(f"Removed {role.mention} as a bonus role.")

    @bonus_role.command(name="list", description="List all bonus roles.")
    async def bonus_role_list(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        roles = guild.bonus_roles
        if not roles:
            return await ctx.reply("There are no bonus roles.")
        embed = discord.Embed(title="Bonus Roles")
        for role in roles:
            embed.add_field(name=f"Role", value=f"<@&{role.get('role_id')}>")
        await ctx.reply(embed=embed)

    @guild_settings.group(name="bonus_cash_roles", description="View or change Bonus roles")
    @commands.has_any_role(694641646922498069, 694641646918434875)
    async def bonus_cash_roles(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @bonus_cash_roles.command(name="add_cash_role", description="Add an role to cash roles")
    @app_commands.describe(role="The role to add.")
    @app_commands.describe(cash="The amount of cash to give.")
    @app_commands.describe(description="The description of the role.")
    @commands.has_guild_permissions(ban_members=True)
    async def bonus_cash_add_role(self, ctx: commands.Context, role: discord.Role, cash: int, description: str):
        role_data = {
            "_id": role.id,
            "name": role.name,
            "added_by": ctx.author.id,
            "color": role.color.to_rgb(),
            "add_at": datetime.datetime.utcnow(),
            "cash": cash,
            "description": description
        }
        await self.bot.db_client.add_cash_role(guild_id=ctx.guild.id, role_data=role_data)
        await ctx.send(f"Added {role.mention} to the cash roles.")

    @bonus_cash_roles.command(name="remove_cash_role", description="Remove an role from cash roles")
    @app_commands.describe(role="The role to remove.")
    @commands.has_guild_permissions(ban_members=True)
    async def bonus_cash_remove_role(self, ctx: commands.Context, role: discord.Role):
        await self.bot.db_client.delete_cash_role(guild_id=ctx.guild.id, role_id=role.id)
        await ctx.send(f"Removed {role.mention} from the shop.")

    @bonus_cash_roles.command(name="list_cash_roles", description="List all cash roles")
    @commands.has_guild_permissions(ban_members=True)
    async def bonus_cash_list_roles(self, ctx: commands.Context):
        roles = await self.bot.db_client.get_cash_roles(guild_id=ctx.guild.id)
        em = discord.Embed(title="Cash Roles", color=await generate_embed_color(ctx.author))
        for role_data in roles:
            role = ctx.guild.get_role(int(role_data.get('_id')))
            em.add_field(name="",
                         value=f"\nRole: {role.mention}\nCash: {role_data.get('cash')}\nAdded By: <@{role_data.get('added_by')}>",
                         inline=False)
        await ctx.send(embed=em)

    @guild_settings.group(name="shop_admin", description="Shop Admin Commands")
    @commands.has_any_role(694641646922498069, 694641646918434875)
    async def shop_admin(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @shop_admin.command(name="add_role", description="Add an role to the shop")
    @app_commands.describe(role="The role to add.")
    @app_commands.describe(price="The price of the role.")
    @app_commands.describe(description="The description of the role.")
    @commands.has_guild_permissions(ban_members=True)
    async def shop_admin_add_role(self, ctx: commands.Context, role: discord.Role, price: int, description: str):
        role_data = {
            "_id": role.id,
            "name": role.name,
            "added_by": ctx.author.id,
            "color": role.color.to_rgb(),
            "add_at": datetime.datetime.utcnow(),
            "price": price,
            "description": description
        }
        await self.bot.db_client.add_shop_role(guild_id=ctx.guild.id, role_data=role_data)
        await ctx.send(f"Added {role.mention} to the shop.")

    @shop_admin.command(name="remove_role", description="Remove an role from the shop")
    @app_commands.describe(role="The role to remove.")
    @commands.has_guild_permissions(ban_members=True)
    async def shop_admin_remove_role(self, ctx: commands.Context, role: discord.Role):
        await self.bot.db_client.delete_shop_role(guild_id=ctx.guild.id, role_id=role.id)
        await ctx.send(f"Removed {role.mention} from the shop.")

    @shop_admin.command(name="list_roles", description="List all roles in the shop")
    async def shop_admin_list_roles(self, ctx: commands.Context):
        roles = await self.bot.db_client.get_shop_roles(guild_id=ctx.guild.id)
        em = discord.Embed(title="Shop Roles", color=await generate_embed_color(ctx.author))
        for role_data in roles:
            role = ctx.guild.get_role(int(role_data.get('_id')))
            em.add_field(name="",
                         value=f"\nRole: {role.mention}\nPrice: {role_data.get('price')}\nAdded By: <@{role_data.get('added_by')}>",
                         inline=False)
        await ctx.send(embed=em)

    @shop_admin.command(name="add_gift", description="Add an gift to the shop")
    @app_commands.describe(name="The name gift to add.")
    @app_commands.describe(price="The price of the gift.")
    @app_commands.describe(description="The description of the gift.")
    @app_commands.describe(value="The value of the gift.")
    @app_commands.describe(emote="The emote of the gift.")
    @app_commands.describe(positive="Is the gift positive?")
    @commands.has_guild_permissions(ban_members=True)
    async def shop_admin_add_gift(self, ctx: commands.Context, name: str, price: int, description: str, value: int,
                                  emote: str, positive: bool):
        is_emote = await self.is_emote(emote)
        if not is_emote:
            return await ctx.send("That is not a valid emote.")
        gift_data = {
            "_id": name.lower(),
            "name": name.capitalize(),
            "added_by": ctx.author.id,
            "add_at": datetime.datetime.utcnow(),
            "price": price,
            "description": description,
            "value": value,
            "emote": emote,
            "positive": positive
        }
        await self.bot.db_client.add_shop_gift(guild_id=ctx.guild.id, gift_data=gift_data)
        await ctx.send(f"Added {name}{emote} to the shop.")

    @shop_admin.command(name="remove_gift", description="Remove an gift from the shop")
    @app_commands.describe(name="The name of the gift to remove.")
    @commands.has_guild_permissions(ban_members=True)
    async def shop_admin_remove_gift(self, ctx: commands.Context, name: str):
        await self.bot.db_client.delete_shop_gift(guild_id=ctx.guild.id, gift_id=name)
        await ctx.send(f"Removed {name} from the shop.")

    @shop_admin.command(name="list_gifts", description="List all gifts in the shop")
    async def shop_admin_list_gifts(self, ctx: commands.Context):
        gifts = await self.bot.db_client.get_shop_gifts(guild_id=ctx.guild.id)
        sorted_gifts = sorted(gifts, key=lambda x: x['value'], reverse=True)
        embeds = []
        first_page_title = "Gift list"
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
                em.add_field(name="",
                             value=f"\nName: {gift_data.get('name')}\n"
                                   f"Price: {gift_data.get('price'):,}\n"
                                   f"Description: {gift_data.get('description')}\n"
                                   f"Value: {gift_data.get('value'):,}\n"
                                   f"Emote: {gift_data.get('emote')}\n"
                                   f"Positive: {gift_data.get('positive')}\n"
                                   f"Added By: <@{gift_data.get('added_by')}>",
                             inline=False)

            # Append the embed to the list of embeds
            embeds.append(em)
        await Paginator(delete_on_timeout=False, timeout=120).start(ctx, pages=embeds)

    # @shop_admin.command(name="add_item", description="Add an item to the shop")
    # @app_commands.describe(item="The item to add.")
    # async def shop_admin_add_item(self, ctx: commands.Context, item: str, price: int):
    #     item_data = {
    #         "_id": item,
    #         "name": item,
    #         "added_by": ctx.author.id,
    #         "add_at": datetime.datetime.utcnow(),
    #         "price": price
    #     }
    #     await self.bot.db_client.add_item(item_data)
    #     await ctx.send(f"Added {item} to the shop.")

    @guild_settings.group(name="lvl_up_channel", description="View or change the level up channel.")
    @commands.has_guild_permissions(ban_members=True)
    async def lvl_up_channel(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @lvl_up_channel.command(name="set_lvl_channel", description="Set the level up channel.")
    @app_commands.describe(channel="The channel to set.")
    @commands.has_guild_permissions(ban_members=True)
    async def lvl_up_channel_set(self, ctx, channel: discord.TextChannel):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        await guild.update_config("lvl_up_channel", channel.id)
        await ctx.reply(f"Set the level up channel to {channel.mention}.")

    @lvl_up_channel.command(name="remove_lvl_channel", description="Remove the level up channel.")
    @commands.has_guild_permissions(ban_members=True)
    async def lvl_up_channel_remove(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        await guild.update_config("lvl_up_channel", None)
        await ctx.reply("Removed the level up channel.")

    @lvl_up_channel.command(name="view_lvl_channel", description="View the level up channel.")
    async def lvl_up_channel_view(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        channel_id = await guild.get_config("lvl_up_channel")
        if not channel_id:
            return await ctx.reply("There is no level up channel.")
        channel = ctx.guild.get_channel(channel_id)
        await ctx.reply(f"The level up channel is {channel.mention}.")

    @guild_settings.group(name="text_reactions", description="View or change text reactions.")
    @commands.has_guild_permissions(ban_members=True)
    async def text_reaction(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @text_reaction.command(name="add", description="Add a text reaction.")
    @app_commands.describe(trigger="The trigger for the text reaction.")
    @app_commands.describe(response="The response for the text reaction.")
    @commands.has_guild_permissions(ban_members=True)
    async def text_reaction_add(self, ctx, trigger: str, response: str):
        is_emote = await self.is_emote(response)
        if not is_emote:
            return await ctx.reply("That is not a valid emote.")
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        if trigger in [reaction.get("trigger") for reaction in guild.text_reactions]:
            return await ctx.reply("That trigger is already a text reaction.")
        guild.text_reactions.append(
            {"trigger": trigger, "response": response, "added_by": ctx.author.id, "add_at": datetime.datetime.utcnow()})
        await self.bot.db_client.update_guild(ctx.guild.id, {"text_reactions": guild.text_reactions})
        await ctx.reply(f"Added `{trigger}` as a text reaction.")

    @text_reaction.command(name="remove", description="Remove a text reaction.")
    @app_commands.describe(trigger="The trigger for the text reaction.")
    @commands.has_guild_permissions(ban_members=True)
    async def text_reaction_remove(self, ctx, trigger: str):
        # if ctx.author.id == 383932871985070085:
        #     return await ctx.reply("404 forbidden\nYou do not have permission to use this command.\ntry gitting gud.")
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        react = next((reaction for reaction in guild.text_reactions if reaction.get("trigger") == trigger), None)
        if not react:
            return await ctx.reply("That trigger is not a text reaction.")
        guild.text_reactions.remove(react)
        await self.bot.db_client.update_guild(ctx.guild.id, {"text_reactions": guild.text_reactions})
        await ctx.reply(f"Removed `{trigger}` as a text reaction.")

    @text_reaction.command(name="list", description="List all text reactions.")
    async def text_reaction_list(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        reactions = guild.text_reactions
        if not reactions:
            return await ctx.reply("There are no text reactions.")
        embed = discord.Embed(title="Text Reactions")
        for reaction in reactions:
            added_by = reaction.get("added_by", None)

            embed.add_field(name="react",
                            value=f"{reaction.get('trigger')}: {reaction.get('response')}\nAdded by <@{added_by}>",
                            inline=False)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="help", description="have a list of commands")
    async def help(self, ctx):
        em = discord.Embed(title="Commands List", colour=discord.Colour.blue())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        if ctx.guild:
            user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
            await user_data.update_stat(command=ctx.command.name)
        em.set_author(
            name="Help Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name} at {timestamp}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        # em.add_field(name="<a:core:1158418275559022674> Core:",
        #              value="</github:1146802715511492670>: view the bots github repo\n</invite:1146802715511492668>: invite the bot to your server\n</ping:1145445177092231339>: show bot and API latency\n</support:1146802715511492669>: join the support server\n",
        #              inline=False)
        # em.add_field(name="<:currency:1158418293879754833> Currency:",
        #              value="</adventure:1146773955642937375>: go on an adventure\n</chop:1146110870632530063>: chop some wood\n</fish:1146100979532570694>: go fishing\n</mine:1146109054154977373>: go mining\n</daily:1145445177092231343>: get your daily free coins\n</weekly:1145445177092231344>: get your weekly free coins\n</work:1145445177092231345>: slave away for capitalism\n</challenge:1186691561174609980>: solve a daily challenge for a reward\n",
        #              inline=False)
        # em.add_field(name="<:Gambling:1158418665209864212> Gambling:",
        #              value="</blackjack:1146852161481883779>: play blackjack\n</coinflip:1146775189732987011>: play coinflip\n</dice:1146842135736356886>: roll some dice\n</slots:1145445177092231340>: play slots\n</roulette:1146842135736356887>: play roulette\n</rps:1146842135736356884>: play rock paper scissors\n</rpsls:1146842135736356885>: play rock paper scissors lizard spock\n</highlow:1153770798050459838>: play a game of highlow\n</wheel:1146879853321269348>: spin the wheel of fortune\n</crime:1145445177092231346>: do some crime\n</rob:1145445177092231347>: rob someone\n</race start:1169321390407688223>: start a race\n</race enter:1169321390407688223>: join a race\n</race bet:1169321390407688223>: bet on a race and fuel your addiction\n",
        #              inline=False)
        # em.add_field(name="<:Profile1:1158418933221695608> Profile:",
        #              value="</avatar:1145798060560089088>: look at yours or somebody elses avatar\n</profile:1145445177092231342>: look at yours or somebody elses profile\n</rank:1155848810157850738>: generate yours or somebody elses rank card\n</bail:1145445177092231341>: release you or someone else from jail\n</stats:1186787637885939752>: see your bot usage stats\n</race stats:1169321390407688223>: your raceing stats\n</inventory role view:1163486147650003065>: view your role inventory\n</inventory role toggle:1163486147650003065>: toggle a role from your inventory\n</inventory role give:1163486147650003065>: gift a role from your inventory\n</inventory items view:1163486147650003065>: view your items inventory\n</inventory items use:1163486147650003065>: use an item from your inventory\n</inventory items equip:1163486147650003065>: equip an item from you inventory\n</inventory gifts view:1163486147650003065>: view your gifts inventory\n</inventory gifts give:1163486147650003065>: give a gift from your inventory\n",
        #              inline=False)
        # em.add_field(name="<a:transaction:1158419857138778142> Transactions:",
        #              value="</transactions balance:1145445177092231348>: check your balance\n</transactions pay:1145445177092231348>: pay someone money\n</transactions deposit:1145445177092231348>: deposit money into your bank\n</transactions depall:1145445177092231348>: deposit all your money into the bank\n</transactions withdraw:1145445177092231348>: withdraw money from your bank\n</transactions withall:1145445177092231348>: withdraw all your money from the bank\n",
        #              inline=False)
        # em.add_field(name="<:leaderboard:1186917831657406484> Leaderboard:",
        #              value="</leaderboard summary:1145503523652517968>: the name kind of explains it, doesnt it\n</leaderboard level:1145503523652517968>: check the level leaderboard\n</leaderboard balance:1145503523652517968>: check the cash balance leaderboard\n</leaderboard bank:1145503523652517968>: check the bank balance leaderboard\n</leaderboard total:1145503523652517968>: check the total balance leaderboard\n</leaderboard waifu:1145503523652517968>: check the waifu leaderboard\n",
        #              inline=False)
        # em.add_field(name="<:misc:1186928407548801055> Miscellaneous:",
        #              value="</urban:1163281362963410964>: search the urban dictionary\n</penis:1170469859113578586>: detects user's penis length, this is 100% accurate\n</ban_chart:1163145353994965032>: display a chart of the moderators with the most bans\n",
        #              inline=False)
        # em.add_field(name="<:shop:1187028991333380156> Shop:",
        #              value="</shop gift buy:1158410919387336724>: buy a gift from the shop\n</shop gift list:1158410919387336724>: list all gifts in the shop\n</shop roles buy:1158410919387336724>: buy a role from the shop\n</shop roles list:1158410919387336724>: list all roles in the shop\n</shop items buy:1158410919387336724>: buy an item from the shop\n</shop items list:1158410919387336724>: list all items in the shop\n",
        #              inline=False)
        # em.add_field(name="<:waifu:1187029479726534668> Waifu:",
        #              value="</waifu claim:1163610274251690014>: claim a waifu\n</waifu divorce:1163610274251690014>: divorce a waifu\n</waifu info:1163610274251690014>: get info about a waifu\n</waifu set-affinity:1163610274251690014>: set your affinity\n",
        #              inline=False)
        # em.add_field(name="<:settings:1186920164172763166> Configuration:",
        #              value="</pings:1168982695464927403>: role pings\n</settings lvlroles add:1163163800841748536>: add level roles\n</settings lvlroles remove:1163163800841748536>: remove level roles\n</settings lvlroles list:1163163800841748536>: list the current level roles\n</settings lvl_up_channel set_lvl_channel:1163163800841748536>: set a level up channel\n</settings lvl_up_channel remove_lvl_channel:1163163800841748536>: remove the level up channel\n</settings lvl_up_channel view_lvl_channel:1163163800841748536>: view which channel is set as the level up channel\n</settings bonus_roles add:1163163800841748536>: add a bonus role\n</settings bonus_roles remove:1163163800841748536>: remove a bonus role\n</settings bonus_roles list:1163163800841748536>: list all bonus roles\n</settings bonus_cash_roles add_cash_role:1163163800841748536>: add a role to cash roles\n</settings bonus_cash_roles remove_cash_role:1163163800841748536>: remove a role to cash roles\n</settings bonus_cash_roles list_cash_roles:1163163800841748536>: list all cash roles\n</settings shop_admin add_gift:1163163800841748536>: add a gift item to the shop\n</settings shop_admin remove_gift:1163163800841748536>: remove a gift item from the shop\n</settings shop_admin add_role:1163163800841748536>: add a role item to the shop\n</settings shop_admin remove_role:1163163800841748536>: remove a role item from the shop\n</settings shop_admin list_gifts:1163163800841748536>: list all gift items in the shop\n</settings shop_admin list_roles:1163163800841748536>: list all role items in the shop\n</settings text_reactions add:1163163800841748536>: add a text reaction\n</settings text_reactions remove:1163163800841748536>: remove a text reaction\n</settings text_reactions list:1163163800841748536>: list all text reactions\n</settings pings add:1163163800841748536>: add a ping role\n</settings pings remove:1163163800841748536>: remove a ping role\n</settings pings list:1163163800841748536>: list all ping roles\n",
        #              inline=False)
        # em.add_field(name="<:Moderator:1158420095136190506> Moderation:",
        #              value="</massnick start:1154508740482052186>: run a massnick\n</massnick cancel:1154508740482052186>: cancel your currently running massnick\n</massnick reset:1154508740482052186>: clear a massnick and reset everyones names\n</idiot set:1155875939079700581>: set an idiots nickname\n</idiot clear:1155875939079700581>: clear an idiots nickname\n</idiot list:1155875939079700581>: list all idiots\n</idiot check:1155875939079700581>: check if a user is an idiot\n</ratio:1155206383986298900>: check the ratio of nsfw to sfw channels\n</new_ticket:1156219459011358750>: create a new ticket\n</new_verify:1170458219353751582>: create a new verification ticket\n</kick:1158392520284327937>: kick a user from the server\n</ban:1158392520284327938>: ban a user from the server\n</purge:1158392520284327936>: purge messages from a channel\n",
        #              inline=False)
        view = HelpView(ctx)
        await ctx.reply(embed=em, view=view)

    @commands.hybrid_command(name="urban", description="Search the urban dictionary.")
    @commands.guild_only()
    @app_commands.describe(term="The term to search for.")
    async def urban(self, ctx, term: str):
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        await user_data.update_stat(command=ctx.command.name)
        try:
            req = await self.bot.web_client.get(f"https://api.urbandictionary.com/v0/define?term={term}")
            if not req.status == 200:
                return await ctx.reply(f'Failed to retrieve data from Urban Dictionary. Status code: {req.status}')
            data = await req.json()
            if data['list']:
                definition = data['list'][0]
                color = await generate_embed_color(ctx.author)
                em = discord.Embed(color=color, title="Urban dictionary", description=f"**Search term**: {term}")
                em.add_field(name='**Definition**', value=definition['definition'], inline=False)
                em.add_field(name='**Example**', value=definition['example'], inline=False)
                em.add_field(name='**Thumbs Up**', value=definition['thumbs_up'], inline=True)
                em.add_field(name='**Thumbs Down**', value=definition['thumbs_down'], inline=True)
                em.add_field(name='**Link**', value=definition['permalink'], inline=False)
                em.set_author(
                    name="Urban Command",
                    icon_url=self.bot.user.display_avatar.with_static_format("png"),
                    url="https://discord.gg/invite/tailss")
                timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
                em.set_footer(
                    text=f"Command ran by {ctx.author.display_name} at {timestamp}",
                    icon_url=ctx.author.display_avatar.with_static_format("png"))
                em.set_thumbnail(
                    url="https://static2.tgstat.ru/channels/_0/69/69eacff302f587d399c3b99c1183d94a.jpg")
                return await ctx.reply(embed=em)
            return await ctx.reply(f'No definitions found for "{term}" on Urban Dictionary.')
        except Exception as e:
            print(e)
            await ctx.send('An error occurred while fetching the Urban Dictionary definition.')

    @guild_settings.group(name="pings", description="View or change ping commands.")
    @commands.has_guild_permissions(ban_members=True)
    async def ping_roles(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @ping_roles.command(name="add", description="Add a ping command.")
    @app_commands.describe(trigger="The trigger for the ping command.")
    @app_commands.describe(response="The role to ping")
    @commands.has_guild_permissions(ban_members=True)
    async def ping_role_add(self, ctx, trigger: str, response: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        if trigger in [ping_tag.get("ping") for ping_tag in guild.ping_tags]:
            return await ctx.reply("That is already a ping.")
        guild.ping_tags.append(
            {"ping": trigger, "role": response.id})
        await self.bot.db_client.update_guild(ctx.guild.id, {"ping_tags": guild.ping_tags})
        await ctx.reply(f"Added `{trigger}` as a ping command.")

    @ping_roles.command(name="remove", description="Remove a ping command.")
    @app_commands.describe(trigger="The trigger for the ping command.")
    async def ping_role_remove(self, ctx, trigger: str):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        ping = next((ping_tag for ping_tag in guild.ping_tags if ping_tag.get("ping") == trigger), None)
        if not ping:
            return await ctx.reply("That trigger is not a ping.")
        guild.ping_tags.remove(ping)
        await self.bot.db_client.update_guild(ctx.guild.id, {"ping_tags": guild.ping_tags})
        await ctx.reply(f"Removed `{trigger}` as a ping.")

    @ping_roles.command(name="list", description="List all pings.")
    async def ping_role_list(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        ping_tags = guild.ping_tags
        if not ping_tags:
            return await ctx.reply("There are no pings.")
        embed = discord.Embed(title="ping roles")
        for ping_tag in ping_tags:
            embed.add_field(name=" ", value=f"{ping_tag.get('ping')}: <@&{ping_tag.get('role')}>", inline=False)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="penis", description="Detects user's penis length, This is 100% accurate.")
    @app_commands.describe(user="user to get penis size of")
    @commands.guild_only()
    async def penis(self, ctx, user: discord.Member):
        """Detects user's penis length, This is 100% accurate.
        """
        user_data = await self.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        await user_data.update_stat(command=ctx.command.name)
        random.seed(str(user.id))
        if ctx.bot.user.id == user.id:
            length = 50
        else:
            length = random.randint(0, 30)
        dong = "8{}D".format("=" * length)
        await ctx.send(f"**{user.mention}'s size:**\n{dong}\n")


async def setup(bot):
    await bot.add_cog(Core(bot))
