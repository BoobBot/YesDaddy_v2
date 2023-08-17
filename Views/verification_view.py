import discord


class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Start verification', style=discord.ButtonStyle.green, custom_id='persistent_view:green', emoji='✔️')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(dir(interaction))
        await interaction.response.send_message(interaction.message)

