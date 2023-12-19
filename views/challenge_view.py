import discord
from discord.ui import View, Button, TextInput


class Challenge(discord.ui.Modal, title='daily challenge'):
    def __init__(self, ctx, challenge, answer):
        super().__init__()
        self.ctx = ctx
        self.challenge = challenge
        self.answer = answer
        self.label = challenge if len(challenge) <= 45 else f"Whats your answer?"
        self.guess = discord.ui.TextInput(
            label=challenge,
            style=discord.TextStyle.long,
            placeholder="Enter your answer",
            required=True,
            max_length=300,
            min_length=1
        )
        self.add_item(self.guess)

    async def on_submit(self, interaction: discord.Interaction):
        user_answer = self.guess.value
        if user_answer.lower() == self.answer.lower():
            await interaction.response.send_message("Your answer is correct! You win!")
        else:
            await interaction.response.send_message("Incorrect answer.")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        self.ctx.bot.log.exception('Error with feedback command.', exc_info=error)


class ChallengeView(View):
    def __init__(self, ctx, challenge, answer):
        super().__init__()
        self.ctx = ctx
        self.challenge = challenge
        self.answer = answer
        self.message = None

    async def on_timeout(self) -> None:
        await self.disable_buttons()

    async def disable_buttons(self) -> None:
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self)

    @discord.ui.button(label='Answer', style=discord.ButtonStyle.success)
    async def answer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Challenge(ctx=self.ctx, challenge=self.challenge, answer=self.answer))

    @discord.ui.button(label='Close', style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None)
        await interaction.message.delete()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        return False
