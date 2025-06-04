import asyncio
import random
from datetime import datetime

import discord

class ReferralView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label="Join Star Citizen 🌌",
            url="https://www.robertsspaceindustries.com/enlist?referral=STAR-9YPL-WBP9"
        ))