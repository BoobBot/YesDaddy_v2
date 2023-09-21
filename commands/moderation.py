import discord
import unicodedata
from discord import app_commands
from discord.ext import commands

from views.confirm_view import Confirm


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="selfban", description="Ban yourself from the server.")
    async def selfban(self, interaction: discord.Interaction):
        if interaction.user.id == 596330574109474848:
            return await interaction.response.send_message("Tom said No, Stop fucking trying <:pikascream:585952447801982977>")
        if [role for role in interaction.user.roles if role.id == 694641646922498069]:
            return await interaction.response.send_message("You can't selfban from the community server, you absolute idiot, suffer instead.")

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
                await interaction.user.ban(delete_message_days=0,
                                          reason="wah wah, selfbanned.")
                await interaction.followup.send(f"{interaction.user} decided to selfban. Fucking idiot.")
            except:
                await interaction.followup.send("You can't selfban, suffer instead.")

    @app_commands.command(name="massnick", description="mass change nicknames of your server members")
    async def massnick():

async def setup(bot):
    await bot.add_cog(Moderation(bot))
