import asyncio
from typing import Optional

import discord


class TestButton(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.author = None
        self.message = None
        self.clicked = False

    async def on_timeout(self) -> None:
        await self.disable_buttons()

    async def disable_buttons(self):
        for item in self.children:
            item.style = discord.ButtonStyle.green if self.clicked else discord.ButtonStyle.red
            item.emoji = "👍" if self.clicked else "✖️"
            item.disabled = True

        await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("nope", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="click me", style=discord.ButtonStyle.grey, emoji="<:time:1169390997139095623>")
    async def reminder(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        self.clicked = True
        await self.disable_buttons()
        print(dir(self))
        await interaction.followup.send(f"Okay")
        self.stop()
