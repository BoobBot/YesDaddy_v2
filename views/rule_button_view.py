from datetime import datetime

import discord

from views.tickets_view import TicketView


class RuleButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='I accept the rules', style=discord.ButtonStyle.green,
                       custom_id='memberrole', emoji='✔️')
    async def ruleaccept(self, interaction: discord.Interaction, button: discord.ui.Button):
        # for testing await interaction.client.db_client.delete_guild(interaction.guild.id)
        # Check if the user already has the member role
        if 694641646780022826 in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("You already have the member role!", ephemeral=True)
        member = interaction.user
        await member.add_roles(
            discord.utils.get(interaction.guild.roles, id=694641646780022826))  # Member
        await interaction.response.send_message("You have received the member role!", ephemeral=True)