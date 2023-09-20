from datetime import datetime

import discord

from views import support_view
from views.tickets_view import TicketView


class SupportChannelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Start a support ticket', style=discord.ButtonStyle.green,
                       custom_id='persistent_view:support', emoji='🆘')
    async def support(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            dm_channel = await interaction.user.create_dm()
            await dm_channel.send("Hello! opening a support ticket for you.")
        except discord.Forbidden:
            return await interaction.response.send_message("I couldn't DM you! Do you have DMs disabled?",
                                                           ephemeral=True)

        retrieved_guild = await interaction.client.db_client.get_guild(interaction.guild.id)
        # if interaction.user.id in [ticket.get("user_id") for ticket in retrieved_guild.support_tickets if
        #                            ticket.get("status") == "open"]:
        #     return await interaction.response.send_message("You are already have a ticket", ephemeral=True)

        category_id = 1141700782006222970
        category = interaction.guild.get_channel(category_id)
        staff = discord.utils.get(interaction.guild.roles, id=694641646918434875)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
            staff: discord.PermissionOverwrite(send_messages=True, read_messages=True, embed_links=True,
                                               read_message_history=True, attach_files=True)
        }
        new_channel = await interaction.guild.create_text_channel(interaction.user.name, category=category,
                                                                  overwrites=overwrites)
        await interaction.response.send_message("Opened support ticket, check your DMs!", ephemeral=True)
        ticket_data = {
            "channel_id": new_channel.id,
            "dm_channel_id": dm_channel.id,
            "user_id": interaction.user.id,
            "status": "open",
            "resolved_by": None,
            "resolved_at": None,
            "created_at": datetime.utcnow(),
            "reason": "Support"
        }

        await interaction.client.db_client.add_support_ticket(interaction.guild.id, ticket_data)
        await dm_channel.send("Your ticket has been created. Please describe your issue.")
        await new_channel.send(
            f"<@&981426793925992448> Support Ticket by {interaction.user.mention}",
            view=support_view.SupportTicketView())

        await interaction.client.db_client.update_guild(interaction.guild.id, retrieved_guild.__dict__)

    