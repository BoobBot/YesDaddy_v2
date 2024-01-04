import datetime

import discord


class Stats(discord.ui.Select):
    def __init__(self, ctx, options):
        self.ctx = ctx
        options = options
        super().__init__(placeholder="Select an Category", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # set the embed
        em = discord.Embed(title="Stats", colour=discord.Colour.blue())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Stats Command",
            icon_url=self.ctx.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {self.ctx.author.display_name} at {timestamp}",
            icon_url=self.ctx.author.display_avatar.with_static_format("png"))

        # set the embed description based on the selected option
        choice = self.values[0]
        user = await self.ctx.bot.db_client.get_user(user_id=self.ctx.author.id, guild_id=self.ctx.guild.id)
        stats = user.get_stat(choice)
        if stats is None:
            return await interaction.response.send_message("invalid category.", ephemeral=True)
        stats_response = '\n'.join(f'{key.replace("_", " ")}: {value}' for key, value in stats.items())
        em.description = f"**{stats_response}**\n"
        await interaction.response.edit_message(embed=em, view=None)


class StatsView(discord.ui.View):
    def __init__(self, ctx, timeout=180):
        super().__init__(timeout=timeout)
        user_data = ctx.bot.db_client.get_user(user_id=ctx.author.id, guild_id=ctx.guild.id)
        options = []
        for key, value in user_data.stats.items():
            options.append(discord.SelectOption(label=key, description=f"stats for {key}"))
        self.add_item(Stats(ctx=ctx, options=options))
