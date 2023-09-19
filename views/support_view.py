import asyncio
import re
from datetime import datetime
from io import BytesIO

import discord

INDENT_REGEX = re.compile(r'^\s+', re.MULTILINE)


class SupportTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='close', style=discord.ButtonStyle.grey, custom_id='support_view:close')
    async def support_ticket_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = await interaction.client.db_client.get_guild(interaction.guild.id)
        if not data:
            interaction.client.log.error("No data found for ticket, this should not happen :/")
            return await interaction.response.send_message("Something went wrong", ephemeral=True)
        
        ticket = next((ticket for ticket in data.support_tickets if ticket.get("channel_id") == interaction.channel.id), None)

        if not ticket:
            return await interaction.response.send_message('Ticket data not found', ephemeral=True)

        if ticket.get("user_id") == interaction.user.id:
            return await interaction.response.send_message("You can't close this yourself, this is not your button",
                                                           ephemeral=True)

        user_id = ticket.get("user_id")
        ticket["status"] = "closed"
        ticket["resolved_by"] = interaction.user.id
        ticket["resolved_at"] = datetime.utcnow()

        await interaction.client.db_client.update_guild(interaction.guild.id, {"support_tickets": data.support_tickets})
        # log the verification
        ch = interaction.guild.get_channel(1153818515262947378)
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
        transcript = f"""
        <html>
          <head>
            <title>Ticket Transcript</title>
            <style>
              body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 10px; }}
              h1 {{ background-color: #7289da; color: white; padding: 10px; }}
              p {{ background-color: #ffffff; border: 1px solid #d4d4d4; padding: 5px; margin: 5px; }}
              strong {{ color: #7289da; }}
            </style>
          </head>
          <body>
            <h1>Transcript of Ticket from {interaction.user}</h1>
        """

        async for message in interaction.channel.history(limit=None):
            transcript += f'\n<p><strong>{message.author}:</strong> {message.content}</p>'

        transcript += '\n</body>\n</html>'
        transcript_bytes = BytesIO(transcript.encode())  # Create in-memory buffer. Encode just turns the string into bytes.
        transcript_bytes.seek(0)  # Instantiating a buffer causes the pointer to be at EOF. Seek back to the beginning so we can read the entire buffer contents.

        await ch.send(f"Ticket Transcript for <@{user_id}>:",
                      file=discord.File(transcript_bytes, filename="ticket_transcript.html"))

        # Delete the ticket channel
        await interaction.response.send_message("Ticket Closed", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()
