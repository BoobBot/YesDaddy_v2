import discord
from discord.ext import commands


def has_ban_permissions(self, ctx):
    # Check if the author of the command has the "ban_members" permission
    return ctx.author.guild_permissions.ban_members


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Show bot and API latency.")
    async def ping(self, ctx):
        await ctx.reply(f"Pong! Bot latency: {self.bot.latency * 1000:.2f} ms")

    @commands.hybrid_command(name="invite", description="Invite the bot to your server.")
    async def invite(self, ctx):
        await ctx.reply(
            f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot+applications.commands")

    @commands.hybrid_command(name="support", description="Join the support server.")
    async def support(self, ctx):
        await ctx.reply("https://discord.gg/boobbot")

    @commands.hybrid_command(name="github", description="View the bot's GitHub repository.")
    async def github(self, ctx):
        await ctx.reply("https://github.com/BoobBot/YesDaddy_v2")

    @commands.hybrid_group(name="lvlroles", description="View or change level roles.")
    @commands.check(has_ban_permissions)
    async def lvlrole(self, ctx):
        await ctx.send("Please use a valid subcommand")

    @lvlrole.command(name="add", description="Add a level role.")
    async def lvlrole_add(self, ctx, level: int, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        if role.id in [role.get("role_id") for role in guild.lvl_roles]:
            return await ctx.reply("That role is already a level role.")
        guild.lvl_roles.append({"level": level, "role_id": role.id})
        await self.bot.db_client.update_guild(ctx.guild.id, guild.__dict__)
        await ctx.reply(f"Added {role.mention} as a level role for level {level}.")

    @lvlrole.command(name="remove", description="Remove a level role.")
    async def lvlrole_remove(self, ctx, level: int, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        guild.lvl_roles.remove({"level": level, "role_id": role.id})
        await self.bot.db_client.update_guild(ctx.guild.id, guild.__dict__)
        await ctx.reply(f"Removed {role.mention} as a level role for level {level}.")

    @lvlrole.command(name="list", description="List all level roles.")
    async def lvlrole_list(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        roles = guild.lvl_roles
        if not roles:
            return await ctx.reply("There are no level roles.")
        embed = discord.Embed(title="Level Roles")
        for role in roles:
            embed.add_field(name=f"Level {role.get('level')}", value=f"<@&{role.get('role_id')}>")
        await ctx.reply(embed=embed)


    @commands.hybrid_group(name="bonus_roles", description="View or change bonus roles.")
    @commands.check(has_ban_permissions)
    async def bonus_role(self, ctx):
        await ctx.send("Please use a valid subcommand")

    @bonus_role.command(name="add", description="Add a bonus role.")
    async def bonus_role_add(self, ctx, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        if role.id in [role.get("role_id") for role in guild.bonus_roles]:
            return await ctx.reply("That role is already a bonus role.")
        guild.bonus_roles.append({"role_id": role.id})
        await self.bot.db_client.update_guild(ctx.guild.id, guild.__dict__)
        await ctx.reply(f"Added {role.mention} as a bonus role.")

    @bonus_role.command(name="remove", description="Remove a bonus role.")
    async def bonus_role_remove(self, ctx, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        guild.bonus_roles.remove({"role_id": role.id})
        await self.bot.db_client.update_guild(ctx.guild.id, guild.__dict__)
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

    @commands.hybrid_group(name="text_reactions", description="View or change text reactions.")
    @commands.check(has_ban_permissions)
    async def text_reaction(self, ctx):
        await ctx.send("Please use a valid subcommand")

    @text_reaction.command(name="add", description="Add a text reaction.")
    async def text_reaction_add(self, ctx, trigger: str, response: str):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        if trigger in [reaction.get("trigger") for reaction in guild.text_reactions]:
            return await ctx.reply("That trigger is already a text reaction.")
        guild.text_reactions.append({"trigger": trigger, "response": response})
        await self.bot.db_client.update_guild(ctx.guild.id, guild.__dict__)
        await ctx.reply(f"Added `{trigger}` as a text reaction.")

    @text_reaction.command(name="remove", description="Remove a text reaction.")
    async def text_reaction_remove(self, ctx, trigger: str):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        guild.text_reactions.remove(trigger)
        await self.bot.db_client.update_guild(ctx.guild.id, guild.__dict__)
        await ctx.reply(f"Removed `{trigger}` as a text reaction.")

    @text_reaction.command(name="list", description="List all text reactions.")
    async def text_reaction_list(self, ctx):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        reactions = guild.text_reactions
        if not reactions:
            return await ctx.reply("There are no text reactions.")
        embed = discord.Embed(title="Text Reactions")
        for reaction in reactions:
            embed.add_field(name=f"Trigger", value=f"`{reaction.get('trigger')}`")
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Core(bot))
