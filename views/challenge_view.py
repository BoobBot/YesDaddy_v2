import discord
from discord.ui import View, Button, TextInput


class ChallengeView(View):
    def __init__(self, ctx, challenge, answer):
        super().__init__()
        self.ctx = ctx
        self.challenge = challenge
        self.answer = answer
        self.add_item(Button(style=discord.ButtonStyle.primary, label="Close", custom_id="close_button"))

    @discord.ui.button(label='Answer', style=discord.ButtonStyle.success)
    async def answer_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        input_field = TextInput(placeholder="Enter your answer", custom_id="answer_input")
        self.add_item(input_field)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Close', style=discord.ButtonStyle.danger)
    async def close_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)
        await interaction.message.delete()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        return False

    async def on_error(self, error, item, interaction):
        if isinstance(error, discord.errors.CheckFailure):
            await interaction.response.send_message("You cannot interact with this component.")

    @discord.ui.button(label='Submit', style=discord.ButtonStyle.primary, row=1)
    async def submit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_answer = interaction.data['values']['answer_input']

        if user_answer.lower() == self.answer.lower():
            await interaction.response.send_message("Your answer is correct! You win!")
        else:
            await interaction.response.send_message("Incorrect answer.")

