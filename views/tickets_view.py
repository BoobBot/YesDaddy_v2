import asyncio
import random
from datetime import datetime

import discord

post_verification_messages = [
    "Welcome to the server! We're glad to have you here.",
    "Congratulations on verifying! Feel free to explore the server.",
    "You’re all set! Jump into the channels and join the fun!",
    "Welcome aboard! Make yourself at home.",
    "Great to see you here! Enjoy your stay and have fun!",
    "Verification complete! Say hi to everyone in the general chat.",
    "You’re officially in! Start connecting with the community.",
    "Welcome to the crew! Let the adventure begin.",
    "Glad to have you with us! Check out the channels and introduce yourself.",
    "You made it! Dive into the conversations and make new friends.",
    "Welcome! Let’s make this an amazing experience for you.",
    "Now that you're verified, the fun begins! Enjoy your time here.",
    "Hello! The server is yours to explore. Have a great time!",
    "Awesome to see you here! Start exploring the channels.",
    "Congrats on completing verification! Welcome to our community.",
    "You’re in! Share your thoughts and enjoy your stay.",
    "Welcome, new member! Let’s create something great together.",
    "So glad you’re here! Get involved and enjoy the discussions.",
    "Welcome! We’re excited to see what you bring to the community.",
    "You're officially part of the crew! Dive into the fun.",
    "Welcome! Feel free to introduce yourself and get started.",
    "We’re thrilled to have you here! Enjoy every moment.",
    "Your journey starts here! Have a fantastic time.",
    "Welcome to our space! Engage, connect, and have fun.",
    "It's great to have you with us! Let’s make it awesome.",
    "Welcome! Your new adventure begins now.",
    "Glad to have you here! Enjoy the community vibe.",
    "You’ve made it! Feel free to connect with others.",
    "Welcome! Let’s make some great memories together.",
    "We’ve been waiting for you! Join in the fun.",
    "Happy to see you here! Let the good times roll.",
    "Welcome! The conversations are just getting started.",
    "Thanks for verifying! Enjoy exploring the server.",
    "Great to have you with us! Let’s make this a blast.",
    "Welcome! Feel free to ask if you need help with anything.",
    "You’re finally here! The community is excited to meet you.",
    "We’re so happy you joined us! Enjoy your stay.",
    "You’re one of us now! Let’s make it memorable.",
    "Welcome to your new digital home! Have a wonderful time.",
    "We’re excited you’re here! Dive into the activities.",
    "Welcome! We hope you have a fantastic time with us.",
    "Great to see you! Engage and enjoy the server.",
    "You’re all set up! Say hi and get involved.",
    "Welcome to the server! Let’s build something amazing.",
    "Hello and welcome! Start exploring and having fun.",
    "Welcome! We’re happy to have you on board.",
    "You’re verified! The adventure starts now.",
    "Welcome! Let’s make this place even better with you here.",
    "We’re glad you’re here! Let’s make it unforgettable.",
    "Awesome to see you join! Have a great time in the server."
]


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(label='verify', style=discord.ButtonStyle.green, custom_id='persistent_view:verify')
    async def ticket_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        # Check for Ticket data
        data = await interaction.client.db_client.get_guild(interaction.guild.id)

        if not data:
            interaction.client.log.error("No data found for Ticket, this should not happen :/")
            return await interaction.followup.send("Something went wrong",
                                                   ephemeral=True)

        ticket = next((ticket for ticket in data.tickets if ticket.get("channel_id") == interaction.channel.id \
                       and ticket.get("status") == "open"), None)

        if not ticket:
            return await interaction.followup.send('Ticket data not found', ephemeral=True)

        if ticket.get("user_id") == interaction.user.id:
            return await interaction.followup.send("You can't verify yourself, this is not your button.",
                                                   ephemeral=True)

        user_id = ticket.get("user_id")
        ticket["status"] = "verified"
        ticket["resolved_by"] = interaction.user.id
        ticket["resolved_at"] = datetime.utcnow()

        try:
            member = await interaction.guild.fetch_member(int(user_id))
        except discord.NotFound:
            return await interaction.followup.send("User not found, did they leave the server?",
                                                   ephemeral=True)

        # female = 694641646805057561 694641646821703740
        # male = 694641646805057560 694641646813577267
        # trans = 694641646805057562 694641646813577268

        async def switch(member):
            if any(r.id == 694641646805057561 for r in member.roles):
                # add female role
                await member.add_roles(interaction.guild.get_role(694641646821703740))  # Verified female

            if any(r.id == 694641646805057560 for r in member.roles):
                # add male role
                await member.add_roles(interaction.guild.get_role(694641646813577267))  # Verified male

            if any(r.id == 694641646805057562 for r in member.roles):
                # add other role
                await member.add_roles(interaction.guild.get_role(694641646813577268))  # Verified trans

        await switch(member)
        # add verified role
        await member.add_roles(interaction.guild.get_role(694641646821703741))  # Verified
        # add the new role
        await member.add_roles(interaction.guild.get_role(1178610586423140382))
        d = {"id": member.id, "date": datetime.utcnow(), "guild": interaction.guild.id}
        await interaction.client.db_client.add_new_member(guild_id=interaction.guild.id, data=d)
        # log the verification
        ch = interaction.guild.get_channel(1142915549198823546)
        user = await interaction.client.fetch_user(user_id)
        await ch.send(
            f"verification ticket by {user.name} ({user.id}) was verified by {interaction.user.mention} ({interaction.user.id})")
        # store the ticket
        await interaction.client.db_client.update_ticket(interaction.guild.id, interaction.channel.id, ticket)
        # respond to the user
        wmsg = f"""
                ## <@& 990274958234107914> {user.mention}\n{random.choice(post_verification_messages)}\n
                -# If you're looking for the NSFW stuff please make sure you carefully read <#957202739492962304>\n
                * Check out <#1153718280696103002> and <#1141873785562222763>\n
                * If you need something, hit us up in <#1141914446772588605>\n
                Lastly, join us in <#694641649044685285> and/or <#1131685130533081210> when you're ready.\n
                """

        w_channel = interaction.guild.get_channel(1181580837200859267)
        await w_channel.send(wmsg, allowed_mentions=discord.AllowedMentions.all())
        await interaction.followup.send("Ticket verified!", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

    @discord.ui.button(label='close', style=discord.ButtonStyle.grey, custom_id='persistent_view:close')
    async def ticket_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        data = await interaction.client.db_client.get_guild(interaction.guild.id)

        if not data:
            interaction.client.log.error("No data found for Ticket, this should not happen :/")
            return await interaction.followup.send("Something went wrong",
                                                   ephemeral=True)

        ticket = next((ticket for ticket in data.tickets if ticket.get("channel_id") == interaction.channel.id), None)

        if not ticket:
            return await interaction.followup.send('Ticket data not found', ephemeral=True)

        if ticket.get("user_id") == interaction.user.id:
            return await interaction.followup.send("You can't close this yourself, this is not your button.",
                                                   ephemeral=True)

        user_id = ticket.get("user_id")
        ticket["status"] = "closed"
        ticket["resolved_by"] = interaction.user.id
        ticket["resolved_at"] = datetime.utcnow()

        #await interaction.client.db_client.add_ticket(interaction.guild.id, ticket)
        await interaction.client.db_client.update_ticket(interaction.guild.id, interaction.channel.id, ticket)
        # log the verification
        ch = interaction.guild.get_channel(1142915549198823546)
        try:
            user = await interaction.client.fetch_user(user_id)
        except discord.NotFound:
            user = None
        if user:
            await ch.send(
                f"verification ticket by {user.name} ({user.id}) was closed by {interaction.user.mention} ({interaction.user.id})")
        else:
            await ch.send(
                f"verification ticket by unknown/Deleted user was closed by {interaction.user.mention} ({interaction.user.id})")

        await interaction.followup.send("Ticket Closed", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

    @discord.ui.button(label='ban', style=discord.ButtonStyle.red, custom_id='persistent_view:ban')
    async def ticket_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        data = await interaction.client.db_client.get_guild(interaction.guild.id)

        if not data:
            interaction.client.log.error("No data found for Ticket, this should not happen :/")
            return await interaction.followup.send("Something went wrong",
                                                   ephemeral=True)

        ticket = next((ticket for ticket in data.tickets if ticket.get("channel_id") == interaction.channel.id), None)

        if not ticket:
            return await interaction.followup.send('Ticket data not found', ephemeral=True)

        if ticket.get("user_id") == interaction.user.id:
            return await interaction.followup.send("You can't close this yourself, this is not your button.",
                                                   ephemeral=True)

        user_id = ticket.get("user_id")
        ticket["status"] = "banned"
        ticket["resolved_by"] = interaction.user.id
        ticket["resolved_at"] = datetime.utcnow()

        await interaction.client.db_client.update_ticket(interaction.guild.id, interaction.channel.id, ticket)
        ch = interaction.guild.get_channel(1142915549198823546)
        # Ban the user by ID
        try:
            await interaction.guild.ban(discord.Object(id=user_id), reason=f"Banned by {interaction.user.mention}")
        except discord.Forbidden:
            await ch.send(
                f"verification ticket by {user_id} was banned by {interaction.user.mention} but I don't have permissions to ban")
        except discord.NotFound:
            await ch.send(
                f"verification ticket by {user_id} was banned by {interaction.user.mention} but something went wrong")

        ch = interaction.guild.get_channel(1142915549198823546)
        user = await interaction.client.fetch_user(user_id)

        if user:
            await ch.send(
                f"verification ticket by {user.name} ({user.id}) was banned by {interaction.user.mention} ({interaction.user.id})")
        else:
            await ch.send(
                f"verification ticket by unknown {user_id} was banned by {interaction.user.mention} ({interaction.user.id})")

        await interaction.followup.send("Ticket Closed", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()
