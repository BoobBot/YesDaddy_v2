from typing import Optional

import discord
import unicodedata
from discord import app_commands
from discord.ext import commands

from views.confirm_view import Confirm


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.cancelled = False

    @app_commands.command(name="selfban", description="Ban yourself from the server.")
    async def selfban(self, interaction: discord.Interaction):
        # if interaction.user.id == 596330574109474848:
        #     return await interaction.response.send_message(
        #         "Tom said No, Stop fucking trying <:pikascream:585952447801982977>")
        # if [role for role in interaction.user.roles if role.id == 694641646922498069]:
        #     return await interaction.response.send_message(
        #         "You can't selfban from the community server, you absolute idiot, suffer instead.")

        em = discord.Embed(color=interaction.user.color)
        em.set_author(name="Are you sure about this? It really will ban you.")
        em.description = "This is a one-way trip. You will not be able to rejoin the server unless you draw an unpunishment cat."
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
                # await interaction.user.ban(delete_message_days=0,
                #                            reason="wah wah, selfbanned.")
                await interaction.followup.send(f"{interaction.user} decided to selfban. Fucking idiot.")
            except:
                await interaction.followup.send("You can't selfban, suffer instead.")

    # @commands.group(name="massnick", description="massnick commands")
    # async def massnick(self, ctx):
    #     await ctx.send("Please use subcommands: start, reset, cancel, or unidiot.")
    #
    # @staticmethod
    # async def staff_only(interaction: discord.Interaction):
    #     return any(
    #         [role for role in [694641646922498069, 694641646918434875] if
    #          role in [role.id for role in interaction.user.roles]])
    #
    # @massnick.command(name="start", description="begin a massnick")
    # @app_commands.check(staff_only)
    # @app_commands.describe(text="what you want the massnick to be", role="The role you want to massnick.",
    #                        random="random names", idiot="stops the users from changing it back")
    # @massnick.command(name="cancel", description="Cancel your currently running massnick")
    # @app_commands.check(staff_only)
    # async def massnick_cancel(self, interaction: discord.Interaction):
    #     if self.running:
    #         self.cancelled = True
    #         return await interaction.response.send_message("Cancelling...")
    #     return await interaction.response.send_message("What are you cancelling if I'm not running a massnick?", ephemeral=True)
    #
    # @massnick.command(name="reset", description="Reset everyones names")
    # @app_commands.describe(role="Will iterate over this roles users")
    # @app_commands.check(staff_only)
    # async def massnick_reset(self, interaction: discord.Interaction, role: Optional[discord.Role]):
    #     if role:
    #         members = role.members
    #     else:
    #         member_role = interaction.guild.get_role(694641646780022826)
    #         members = interaction.guild.members
    #         members = [x for x in members if member_role in x.roles]
    #     view = Confirm()
    #     await interaction.response.send_message(
    #         f"{interaction.user.mention}, are you sure you want me to reset members names?", view=view
    #     )
    #     view.message = await interaction.original_response()
    #     await view.wait()
    #     if view.value is None:
    #         return await interaction.followup.send("Timed out.")
    #     if view.value is False:
    #         return await interaction.followup.send("Fine I wont reset.")
    #     await interaction.followup.send("Okie dokie, I'll hit you up when I'm finished :)")
    #
    # async def massnick_start(self, interaction: discord.Interaction, text: Optional[str], role: Optional[discord.Role],
    #                          random: Optional[bool], idiot: Optional[bool]):
    #     if self.running:
    #         return await interaction.response.send_message("I'm already doing a massnick, chill tf out", ephemeral=True)
    #     if role:
    #         members = role.members
    #     else:
    #         member_role = interaction.guild.get_role(694641646780022826)
    #         members = interaction.guild.members
    #         members = [x for x in members if x.top_role < interaction.guild.me.top_role]
    #         members = [x for x in members if member_role in x.roles]
    #     view = Confirm()
    #     await interaction.response.send_message(
    #         f"{interaction.user.mention}, are you sure you want me to run this massnick?", view=view)
    #     view.message = await interaction.original_response()
    #     await view.wait()
    #     if view.value is None:
    #         return await interaction.followup.send("Timed out.")
    #     if view.value is False:
    #         return await interaction.followup.send("Fine I wont massnick the plebs.")
    #     await interaction.followup.send("Okie dokie, I'll hit you up when I'm finished :)")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
