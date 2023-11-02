import asyncio
import datetime
from typing import Optional

import discord


class Reminder(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.bot = None
        self.seconds = None
        self.author = None
        self.message = None
        self.set = False
        self.type = None

    async def add_reminder(self):
        reminder = {
            "guild_id": self.message.guild.id,
            "user_id": self.author.id,
            "channel_id": self.message.channel.id,
            "timestamp": self.message.created_at.timestamp(),
            "reminder_type": self.type,
            "interval": self.seconds,
            "_id": self.type+str(self.author.id)
        }
        await self.bot.db_client.add_reminder(guild_id=self.message.guild.id, reminder_data=reminder)

    async def on_timeout(self) -> None:
        await self.disable_buttons()

    async def disable_buttons(self):
        for item in self.children:
            item.style = discord.ButtonStyle.green if self.set else discord.ButtonStyle.red
            item.emoji = "👍" if self.set else ":x:"
            item.disabled = True

        await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("This is not your button!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Remind Me!", style=discord.ButtonStyle.grey, emoji="<:time:1169390997139095623>")
    async def reminder(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        self.set = True
        await self.disable_buttons()
        await self.add_reminder()
        now = datetime.datetime.now(datetime.timezone.utc)
        target_time = now + datetime.timedelta(seconds=self.seconds)
        remaining_timestamp = discord.utils.format_dt(target_time, style="R")
        await interaction.followup.send(f"Okay I will remind you {remaining_timestamp}")
        self.stop()
