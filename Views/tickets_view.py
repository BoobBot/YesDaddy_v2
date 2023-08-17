import discord


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='verify', style=discord.ButtonStyle.green, custom_id='persistent_view:verify')
    async def ticket_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(dir(interaction))
        # inc = await interaction.response.send_message(dir(interaction))
        # print(dir(inc))

        await interaction.response.send_message(interaction.message)
        await interaction.followup.edit(interaction.user)

    @discord.ui.button(label='close', style=discord.ButtonStyle.grey, custom_id='persistent_view:close')
    async def ticket_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('', ephemeral=True)

    @discord.ui.button(label='ban', style=discord.ButtonStyle.red, custom_id='persistent_view:ban')
    async def ticket_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('', ephemeral=True)
