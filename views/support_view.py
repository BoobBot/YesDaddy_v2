import asyncio
import os
from datetime import datetime

import discord


class SupportTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='close', style=discord.ButtonStyle.grey, custom_id='support_view:close')
    async def support_ticket_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = 0
        data = await interaction.client.db_client.get_guild(interaction.guild.id)
        if not data:
            interaction.client.lof.error("No data found for Ticket, this should not happen :/")
            return await interaction.response.send_message("Something went wrong",
                                                           ephemeral=True)
        for ticket in data.support_tickets:
            if ticket.get("channel_id") == interaction.channel.id:
                if ticket.get("user_id") == interaction.user.id:
                    return await interaction.response.send_message(
                        "You can't close this yourself, This is not your button",
                        ephemeral=True)
                user_id = ticket.get("user_id")
                ticket["status"] = "closed"
                ticket["resolved_by"] = interaction.user.id
                ticket["resolved_at"] = datetime.utcnow()

        await interaction.client.db_client.update_guild(interaction.guild.id, {"support_tickets": data.support_tickets})
        # log the verification
        ch = interaction.guild.get_channel(1142915549198823546)
        try:
            user = await interaction.client.fetch_user(user_id)
        except discord.NotFound:
            user = None
        if user:
            await ch.send(
                f"support ticket by {user.name} ({user.id}) was closed by {interaction.user.mention} ({interaction.user.id})")
        else:
            await ch.send(
                f"support ticket by unknown/Deleted user was closed by {interaction.user.mention} ({interaction.user.id})")

        # Create an HTML transcript file with Discord-style CSS
        transcript_file = f"ticket_transcript_{user_id}.html"
        with open(transcript_file, "w", encoding="utf-8") as file:
            file.write("<html>\n<head>\n<title>Ticket Transcript</title>\n")
            file.write('<style>\n')
            file.write('body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 10px; }\n')
            file.write('h1 { background-color: #7289da; color: white; padding: 10px; }\n')
            file.write('p { background-color: #ffffff; border: 1px solid #d4d4d4; padding: 5px; margin: 5px; }\n')
            file.write('strong { color: #7289da; }\n')
            file.write('</style>\n')
            file.write("</head>\n<body>\n")
            file.write(f"<h1>Transcript of Ticket from {interaction.user}</h1>\n\n")

            # Copy messages to the transcript file with HTML formatting
            async for message in interaction.channel.history(limit=None):
                file.write(f'<p><strong>{message.author}:</strong> {message.content}</p>\n')

            file.write("</body>\n</html>")
            file.close()
            print(f"Transcript saved to {transcript_file}")
            await ch.send(f"Ticket Transcript for <@{user_id}>:",
                          file=discord.File(transcript_file, filename="ticket_transcript.html"))

            # Delete the transcript file
            os.remove(transcript_file)

            # Delete the ticket channel
        await interaction.response.send_message("Ticket Closed", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()
