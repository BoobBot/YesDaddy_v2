import datetime

import discord
from discord.ext import commands

from utils.utilities import generate_embed_color


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Show bot and API latency.")
    async def ping(self, ctx):
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
        await ctx.send(embed=em)


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
    @commands.has_guild_permissions(ban_members=True)
    async def lvlrole(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @lvlrole.command(name="add", description="Add a level role.")
    async def lvlrole_add(self, ctx, level: int, role: discord.Role):
        guild = await self.bot.db_client.get_guild(ctx.guild.id)

        if any(role.get('role_id') == role.id for role in guild.lvl_roles):
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
    @commands.has_guild_permissions(ban_members=True)
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
    @commands.has_guild_permissions(ban_members=True)
    async def text_reaction(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

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
        # if ctx.author.id == 383932871985070085:
        #     return await ctx.reply("404 forbidden\nYou do not have permission to use this command.\ntry gitting gud.")
        guild = await self.bot.db_client.get_guild(ctx.guild.id)
        react = next((reaction for reaction in guild.text_reactions if reaction.get("trigger") == trigger), None)
        if not react:
            return await ctx.reply("That trigger is not a text reaction.")
        guild.text_reactions.remove(react)
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

    @commands.hybrid_command(name="help", description="have a list of commands")
    async def help(self, ctx):
        em = discord.Embed(title="Commands List", colour=discord.Colour.blue())
        em.set_footer(
            text=f"Command ran by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.with_static_format("png"))
        em.add_field(name="Core:",
                     value="</github:1146802715511492670>: view the bots github repo\n</invite:1146802715511492668>: invite the bot to your server\n</ping:1145445177092231339>: show bot and API latency\n</support:1146802715511492669>: join the support server\n", inline=False)
        em.add_field(name="Currency:",
                     value="</adventure:1146773955642937375>: go on an adventure\n</chop:1146110870632530063>: chop some wood\n</fish:1146100979532570694>: go fishing\n</mine:1146109054154977373>: go mining\n</daily:1145445177092231343>: get your daily free coins\n</weekly:1145445177092231344>: get your weekly free coins\n", inline=False)
        em.add_field(name="Gambling:",
                     value="</blackjack:1146852161481883779>: play blackjack\n</coinflip:1146775189732987011>: play coinflip\n</dice:1146842135736356886>: roll some dice\n</slots:1145445177092231340>: play slots\n</roulette:1146842135736356887>: play roulette\n</rps:1146842135736356884>: play rock paper scissors\n</rpsls:1146842135736356885>: play rock paper scissors lizard spock\n</highlow:1153770798050459838>: play a game of highlow\n</wheel:1146879853321269348>: spin the wheel of fortune\n</crime:1145445177092231346>: do some crime\n</rob:1145445177092231347>: rob someone\n", inline=False)
        em.add_field(name="Profile:",
                     value="</avatar:1145798060560089088>: look at yours or somebody elses avatar\n</profile:1145445177092231342>: look at yours or somebody elses profile\n</rank:1155848810157850738>: generate yours or somebody elses rank card\n</leaderboard level:1145503523652517968>: check the level leaderboard\n</leaderboard balance:1145503523652517968>: check the balance leaderboard\n</leaderboard bank:1145503523652517968>: check the bank leaderboard\n</bail:1145445177092231341>: release you or someone else from jail\n", inline=False)
        em.add_field(name="Transactions:",
                     value="</transactions balance:1145445177092231348>: check your balance\n</transactions pay:1145445177092231348>: pay someone money\n</transactions deposit:1145445177092231348>: deposit money into your bank\n</transactions depall:1145445177092231348>: deposit all your money into the bank\n</transactions withdraw:1145445177092231348>: withdraw money from your bank\n</transactions withall:1145445177092231348>: withdraw all your money from the bank\n",
                     inline=False)
        em.add_field(name="Moderation:",
                     value="</massnick start:1154508740482052186>: run a massnick\n</ratio:1155206383986298900>: check the ratio of nsfw to sfw channels\n", inline=False)
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Core(bot))
