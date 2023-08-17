import discord

from Views.tickets_view import TicketView


class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Start verification', style=discord.ButtonStyle.green,
                       custom_id='persistent_view:verification', emoji='✔️')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if 694641646821703741 in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("You are already verified!", ephemeral=True)

        if interaction.user.id in temp_data:
            return await interaction.response.send_message("You are already have a ticket", ephemeral=True)

        await interaction.response.send_message("opened ticket", ephemeral=True)

        category = discord.utils.get(interaction.guild.categories, name="🆘 Tickets")
        if category:
            print("Category found")
            new_channel = await interaction.guild.create_text_channel(interaction.user.name, category=category)
            temp_data[interaction.user.id] = {'channel_id': new_channel.id, 'user_name': interaction.user.name}

            await new_channel.set_permissions(interaction.guild.default_role, send_messages=False, read_messages=False)
            # Allow permissions for the specified user
            await new_channel.set_permissions(interaction.user, send_messages=True, read_messages=True)
            await new_channel.send(f"Welcome {interaction.user.mention}! Please wait for a staff member to assist you.",
                                   view=TicketView())


