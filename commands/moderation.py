import discord
import unicodedata
from discord import app_commands
from discord.ext import commands

from views.confirm_view import Confirm


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.slash_command(name="selfban", description="Ban yourself from the server.")
    async def selfban(self, interaction: discord.Interaction):
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
                await interaction.followup.send("You can't selfban, suffer instead.", ephemeral=True)
