from datetime import datetime

import discord

from views.tickets_view import TicketView


class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Start a support ticket', style=discord.ButtonStyle.green,
                       custom_id='persistent_view:support', emoji='✔️')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            dm_channel = await interaction.user.create_dm()
        except discord.Forbidden:
            return await interaction.response.send_message("I couldn't DM you! Do you have DMs disabled?",
                                                           ephemeral=True)

        retrieved_guild = await interaction.client.db_client.get_guild(interaction.guild.id)
        if interaction.user.id in [ticket.get("user_id") for ticket in retrieved_guild.tickets if
                                   ticket.get("status") == "open"]:
            return await interaction.response.send_message("You are already have a ticket", ephemeral=True)

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
        retrieved_guild.tickets.append(ticket_data)





       
        # Store ticket data in MongoDB
        await create_ticket_data(ctx.author.id, dm_channel.id, ticket_channel.id)

        await dm_channel.send("Your ticket has been created. Please describe your issue.")

        if 694641646821703741 in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("You are already verified!", ephemeral=True)


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
            retrieved_guild.tickets.append(ticket_data)
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
            # Update the guild
            await interaction.client.db_client.update_guild(interaction.guild.id, retrieved_guild.__dict__)
