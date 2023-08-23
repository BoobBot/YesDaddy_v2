import asyncio
from datetime import datetime

import discord


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='verify', style=discord.ButtonStyle.green, custom_id='persistent_view:verify')
    async def ticket_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check for Ticket data
        user_id = 0
        data = await interaction.client.db_client.get_guild(interaction.guild.id)
        if not data:
            interaction.client.lof.error("No data found for Ticket, this should not happen :/")
            return await interaction.response.send_message("Something went wrong",
                                                           ephemeral=True)
        for ticket in data.tickets:
            if ticket.get("channel_id") == interaction.channel.id and ticket.get("status") == "open":
                if ticket.get("user_id") == interaction.user.id:
                    return await interaction.response.send_message("You can't verify yourself, this is not your button",
                                                                   ephemeral=True)
                user_id = ticket.get("user_id")
                ticket["status"] = "verified"
                ticket["resolved_by"] = interaction.user.id
                ticket["resolved_at"] = datetime.utcnow()
                try:
                    member = await interaction.guild.fetch_member(int(user_id))
                except discord.NotFound:
                    return await interaction.response.send_message("User not found, did they leave the server?",
                                                                   ephemeral=True)
                # female = 694641646805057561 694641646821703740
                # male = 694641646805057560 694641646813577267
                # trans = 694641646805057562 694641646813577268

                async def switch(member):
                    if 694641646805057561 in [role.id for role in member.roles]:
                        # add female role
                        await member.add_roles(
                            discord.utils.get(interaction.guild.roles, id=694641646821703740))  # Verified female
                    if 694641646805057560 in [role.id for role in member.roles]:
                        # add male role
                        await member.add_roles(
                            discord.utils.get(interaction.guild.roles, id=694641646813577267))  # Verified male
                    if 694641646805057562 in [role.id for role in member.roles]:
                        # add other role
                        await member.add_roles(
                            discord.utils.get(interaction.guild.roles, id=694641646813577268))  # Verified trans

                await switch(member)
                # add verified role
                await member.add_roles(discord.utils.get(interaction.guild.roles, id=694641646821703741))  # Verified
                # log the verification
                ch = interaction.guild.get_channel(1142915549198823546)
                user = await interaction.client.fetch_user(user_id)
                await ch.send(f"verification ticket by {user.name} ({user.id}) was verified by {interaction.user.mention}")
                # store the ticket
                await interaction.client.db_client.update_guild(interaction.guild.id, {"tickets": data.tickets})
                # respond to the user
                await interaction.response.send_message("Ticket verified!", ephemeral=True)
                await asyncio.sleep(5)
                await interaction.channel.delete()

    @discord.ui.button(label='close', style=discord.ButtonStyle.grey, custom_id='persistent_view:close')
    async def ticket_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = 0
        data = await interaction.client.db_client.get_guild(interaction.guild.id)
        if not data:
            interaction.client.lof.error("No data found for Ticket, this should not happen :/")
            return await interaction.response.send_message("Something went wrong",
                                                           ephemeral=True)
        for ticket in data.tickets:
            if ticket.get("channel_id") == interaction.channel.id:
                if ticket.get("user_id") == interaction.user.id:
                    return await interaction.response.send_message(
                        "You can't close this yourself, This is not your button",
                        ephemeral=True)
                user_id = ticket.get("user_id")
                ticket["status"] = "closed"
                ticket["resolved_by"] = interaction.user.id
                ticket["resolved_at"] = datetime.utcnow()

        await interaction.client.db_client.update_guild(interaction.guild.id, {"tickets": data.tickets})
        # log the verification
        ch = interaction.guild.get_channel(1142915549198823546)
        user = await interaction.client.fetch_user(user_id)
        if user:
            await ch.send(f"verification ticket by {user.name} ({user.id}) was closed by {interaction.user.mention}")
        else:
            await ch.send(f"verification ticket by unknown/Deleted user was closed by {interaction.user.mention}")
        await interaction.response.send_message("Ticket Closed", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

    @discord.ui.button(label='ban', style=discord.ButtonStyle.red, custom_id='persistent_view:ban')
    async def ticket_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = 0
        data = await interaction.client.db_client.get_guild(interaction.guild.id)
        if not data:
            interaction.client.lof.error("No data found for Ticket, this should not happen :/")
            return await interaction.response.send_message("Something went wrong",
                                                           ephemeral=True)

        for ticket in data.tickets:
            if ticket.get("channel_id") == interaction.channel.id:
                if ticket.get("user_id") == interaction.user.id:
                    return await interaction.response.send_message(
                        "You can't close this yourself, This is not your button",
                        ephemeral=True)
                user_id = ticket.get("user_id")
                ticket["status"] = "banned"
                ticket["resolved_by"] = interaction.user.id
                ticket["resolved_at"] = datetime.utcnow()

        await interaction.client.db_client.update_guild(interaction.guild.id, {"tickets": data.tickets})

        ch = interaction.guild.get_channel(1142915549198823546)
        # Ban the user by ID
        try:
            await interaction.guild.ban(discord.Object(id=user_id), reason="Banned by ID")
        except discord.Forbidden:
            await ch.send(
                f"verification ticket by {user_id} was banned by {interaction.user.mention} but I don't have permissions to ban")
        ch = interaction.guild.get_channel(1142915549198823546)
        user = await interaction.client.fetch_user(user_id)
        if user:
            await ch.send(f"verification ticket by {user.name} ({user.id}) was banned by {interaction.user.mention}")
        else:
            await ch.send(f"verification ticket by unknown {user_id} was banned by {interaction.user.mention}")
        await interaction.response.send_message("Ticket Closed", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()
