from datetime import datetime

import discord

from views.tickets_view import TicketView


class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Start verification', style=discord.ButtonStyle.green,
                       custom_id='persistent_view:verification', emoji='✔️')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        # for testing await interaction.client.db_client.delete_guild(interaction.guild.id)
        # Check if the user is already verified
        if any(r.id == 694641646821703741 for r in interaction.user.roles):
            return await interaction.response.send_message("You are already verified!", ephemeral=True)

        # check for gender role
        # TODO add to guild config
        # female = 694641646805057561
        # male = 694641646805057560
        # trans = 694641646805057562
        genders = [694641646805057561, 694641646805057560, 694641646805057562]
        if not any(role.id in genders for role in interaction.user.roles):
            return await interaction.response.send_message("You need a gender role from <#1141869787895574598>",
                                                           ephemeral=True)

        # Check if the user is already in the verification process
        retrieved_guild = await interaction.client.db_client.get_guild(interaction.guild.id)

        open_ticket = next((ticket for ticket in retrieved_guild.tickets if ticket.get('user_id') == interaction.user.id and ticket.get('status') == 'open'), None)

        if open_ticket is not None:
            return await interaction.response.send_message(f"You are already have an open ticket at <#{open_ticket['channel_id']}>", ephemeral=True)

        count = len([ticket for ticket in retrieved_guild.tickets if
                     ticket.get("user_id") == interaction.user.id and
                     ticket.get("status") == "closed" and
                     ticket.get("reason") == "Verification"])

        # Create a new ticket
        category = discord.utils.get(interaction.guild.categories, name="🆘 Tickets")
        if category:
            staff = discord.utils.get(interaction.guild.roles, id=694641646918434875)
            overwrites = {
                interaction.user: discord.PermissionOverwrite(send_messages=True, read_messages=True, embed_links=True,
                                                              read_message_history=True, attach_files=True),
                interaction.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
                staff: discord.PermissionOverwrite(send_messages=True, read_messages=True, embed_links=True,
                                                   read_message_history=True, attach_files=True)
            }
            new_channel = await interaction.guild.create_text_channel(interaction.user.name, category=category,
                                                                      overwrites=overwrites)
            await interaction.response.send_message(F"Opened ticket {new_channel.mention}", ephemeral=True)
            ticket_data = {
                "channel_id": new_channel.id,
                "user_id": interaction.user.id,
                "status": "open",
                "resolved_by": None,
                "resolved_at": None,
                "created_at": datetime.utcnow(),
                "reason": "Verification"
            }

            await interaction.client.db_client.add_ticket(interaction.guild.id, ticket_data)

            # Deny permissions for everyone
            # await new_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
            # Allow permissions for the specified user
            # await new_channel.set_permissions(interaction.user, send_messages=True, read_messages=True)
            # Send the ticket message
            await new_channel.send(
                f"<@&981426793925992448> Ticket by {interaction.user.mention}, {count} previous verification tickets",
                view=TicketView())
            # Send the verification message
            embed = discord.Embed(title="Ticket",
                                  description=f"Welcome {interaction.user.mention}! Thank you for contacting BoobBot support. Please send the photos required to verify following the below guidelines. All images sent will be deleted upon completion of the ticket. Please note that if you do not follow the guidelines, your ticket will be closed and you will be banned from the server. \n\n",
                                  color=0x00ff00)
            embed.set_image(url=interaction.client.config.verification_image)
            await new_channel.send(embed=embed)
