import discord


class RuleButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='I accept the rules', style=discord.ButtonStyle.green,
                       custom_id='memberrole', emoji='✔️')
    async def ruleaccept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        # for testing await interaction.client.db_client.delete_guild(interaction.guild.id)
        # Check if the user already has the member role
        if any(r.id == 694641646780022826 for r in interaction.user.roles):
            return await interaction.response.send_message("You already have the member role!", ephemeral=True)

        await interaction.user.add_roles(interaction.guild.get_role(694641646780022826))  # Member
        await interaction.followup.send("You have received the member role!", ephemeral=True)
