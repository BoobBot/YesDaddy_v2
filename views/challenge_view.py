import datetime

import discord
from discord.ui import View, Button, TextInput

from config.items import maybe_loot
from utils.utilities import calculate_level, is_today_weekend_or_holiday, amount_on_level_up, generate_embed_color


class Challenge(discord.ui.Modal, title='daily challenge'):
    def __init__(self, ctx, challenge, answer):
        super().__init__()
        self.bot = ctx.bot
        self.ctx = ctx
        self.challenge = challenge
        self.answer = answer
        self.label = challenge if len(challenge) <= 45 else f"Whats your answer?"
        self.placeholder = challenge if len(challenge) > 45 else f"Enter your answer"
        self.guess = discord.ui.TextInput(
            label=self.label,
            style=discord.TextStyle.long,
            placeholder=self.placeholder,
            required=True,
            max_length=300,
            min_length=1
        )
        self.add_item(self.guess)

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        color = await generate_embed_color(user)
        embed = discord.Embed(title=f"{self.ctx.author.display_name}'s Daily Challenge", color=color)
        embed.set_author(
            name="Daily Challenge",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        embed.set_footer(
            text=f"Command ran by {self.ctx.author.display_name} at {timestamp}",
            icon_url=self.ctx.author.display_avatar.with_static_format("png")
        )
        user_answer = self.guess.value
        if user_answer.lower() == self.answer.lower():
            user_data = await self.ctx.bot.db_client.get_user(user_id=interaction.user.id, guild_id=self.ctx.guild.id)
            user_balance = user_data.balance
            new_user_balance = user_balance + 2000
            xp = 2000
            msg = "✅ Your answer is correct! You win!\n"
            msg += f"You also got ${2000:,}!\n"
            if is_today_weekend_or_holiday():
                xp *= 2
                msg += f"It's a weekend/holiday, so you get double XP for a total of {xp}!\n"
            else:
                msg += f"You also got {xp} XP!\n"
            lvl = calculate_level(user_data.xp + xp)
            if lvl > user_data.level:
                lvl_up_bonus = amount_on_level_up(lvl, 100, 1.05)
                msg += f"You also leveled up to level {lvl} and got ${lvl_up_bonus}!\n"
                await user_data.update_fields(level=lvl, balance=new_user_balance + lvl_up_bonus)
            check_loot = maybe_loot()
            if check_loot is not None:
                item = check_loot
                owned_item = user_data.get_item_by_key("name", item.get("name"), "items")
                if owned_item is not None:
                    owned_item["quantity"] += 1
                    await user_data.set_item_by_key("name", item.get("name"), owned_item, "items")
                else:
                    item["quantity"] = 1
                    await user_data.set_item_by_key("name", item.get("name"), item, "items")
                msg += f"You also found a {check_loot.get('rarity')} {item.get('emote')} {item.get('name')}!\n"
            await user_data.update_fields(balance=new_user_balance, xp=user_data.xp + xp)
            embed.description = msg
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            msg = ":x: Incorrect answer, fucking dummy."
            embed.description = msg
            await interaction.response.edit_message(embed=embed, view=None)

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
