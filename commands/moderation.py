import asyncio
from typing import List, Optional

import discord
from discord import app_commands
from discord.ext import commands

from views.confirm_view import Confirm


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.nickname_task: Optional[asyncio.Task] = None

    # @commands.hybrid_group(name="idiot", description="idiot commands")
    # async def idiot(self, ctx):
    #     await ctx.send("Please use subcommands: set, clear, check, or list.")
    #
    # @idiot.command(name="set", description="set a idiots nickname")
    # async def idiot_set(self, ctx, user: discord.Member, *, nickname: str):
    #     user = self.bot.db_client.get_user(user.id)
    #     if user.idiot:
    #         if user.idiot.get("idiot"):
    #             view = Confirm()
    #             em = discord.Embed(color=ctx.author.user.color)
    #             em.description = f"{user.mention} is already an idiot, changed by <@{user.idiot.get('idiot_by')}>, are you sure you want to change their nickname?"
    #             view.message = await ctx.reply(embed=em, view=view, ephemeral=True)
    #             if view.value is None:
    #                 await ctx.reply("Timed out.", ephemeral=True)
    #             elif view.value is False:
    #                 await ctx.reply("Ok, I wont change it.", ephemeral=True)
    #                 return
    #             else:
    #                 idiot_data = user.idiot
    #                 idiot_data["idiot"] = True
    #                 idiot_data["nickname"] = nickname
    #                 idiot_data["times_idiot"] += 1
    #                 idiot_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
    #                 idiot_data["change"] = 0
    #                 idiot_data["idiot_by"] = ctx.author.id
    #         idiot_data = user.idiot
    #         idiot_data["idiot"] = True
    #         idiot_data["nickname"] = nickname
    #         idiot_data["times_idiot"] += 1
    #         idiot_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
    #         idiot_data["change"] = 0
    #         idiot_data["idiot_by"] = ctx.author.id
    #     else:
    #         idiot_data = {
    #             "nickname": nickname,
    #             "idiot": True,
    #             "idiot_by": ctx.author.id,
    #             "timestamp": datetime.datetime.now(datetime.timezone.utc),
    #             "times_idiot": 1,
    #             "change": 0
    #         }
    #
    #
    #     await user.update_user({"idiot_data": idiot_data}, self.bot)
    #     await ctx.reply(f"Set {user.mention}'s nickname to {nickname}.")

    @app_commands.command(name="selfban", description="Ban yourself from the server.")
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
    async def massnick(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.send_help(ctx.command)

    @massnick.command(name="start", description="begin a massnick")
    @commands.has_any_role(694641646922498069, 694641646918434875)
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
    @commands.has_any_role(694641646922498069, 694641646918434875)
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
    @commands.has_any_role(694641646922498069, 694641646918434875)
    @app_commands.describe(role="Will reset everyone with this role's name")
    async def massnick_reset(self, ctx: commands.Context, role: Optional[discord.Role]):
        if self.nickname_task is not None:
            await self.nickname_task.cancel()
            await asyncio.sleep(1.5)  # Give the task time to cancel.

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

        try:
            for member in members:
                if member.top_role >= ctx.guild.me.top_role:
                    continue

                try:
                    new_name = (await (await self.bot.web_client.get("https://nekos.life/api/v2/name")).json())[
                        'name'] if random is True else nickname
                    # if idiot:

                    if member.display_name == new_name or len(new_name) > 32:
                        continue

                    await member.edit(nick=new_name)
                    updated += 1
                except (discord.Forbidden, discord.HTTPException):
                    failed += 1
        except asyncio.CancelledError:
            cancelled = True

        self.nickname_task = None
        await ctx.author.send(
            f'Massnick results (updated: {updated} / failed: {failed}){" [cancelled]" if cancelled else ""}')

    @commands.hybrid_command(name="ratio", description="Check how many nsfw vs sfw channels there are")
    @commands.has_any_role(694641646922498069, 694641646918434875)
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
            nsfw_channel_names_str = ", ".join(nsfw_channel_names)
            description = f"Age-restricted channels: {nsfw_channel_names_str}"
            em = discord.Embed(title="NSFW Channel List", description=description)
            await ctx.reply(embed=em)

        em = discord.Embed(title="Ratio Check")
        em.add_field(name="SFW:", value=f"{sfw}")
        em.add_field(name="NSFW:", value=f"{nsfw}")
        em.add_field(name="All Channels:", value=f"{allchannels}")
        await ctx.reply(embed=em)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
