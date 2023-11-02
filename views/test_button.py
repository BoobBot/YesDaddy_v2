import asyncio
from typing import Optional

import discord


class TestButton(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.clicked = False

    async def on_timeout(self) -> None:
        await self.disable_buttons()

    async def disable_buttons(self):
        for item in self.children:
            item.style = discord.ButtonStyle.green if self.clicked else discord.ButtonStyle.red
            item.disabled = True

        await self.message.edit(view=self)

    @discord.ui.button(label="click me", style=discord.ButtonStyle.grey)
    async def reminder(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        self.clicked = True
        await self.disable_buttons()
        print(dir(self))
        self.stop()
