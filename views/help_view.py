import datetime

import discord


class Help(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [
            # add more options here
            discord.SelectOption(label="Core", emoji="<a:core:1158418275559022674>", description="Core Commands"),
            discord.SelectOption(label="Option 2", emoji="✨", description="This is option 2!"),
            discord.SelectOption(label="Option 3", emoji="🎭", description="This is option 3!")
        ]
        super().__init__(placeholder="Select an Category", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # set the embed
        em = discord.Embed(title="Commands List", colour=discord.Colour.blue())
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%I:%M %p')
        em.set_author(
            name="Help Command",
            icon_url=self.bot.user.display_avatar.with_static_format("png"),
            url="https://discord.gg/invite/tailss")
        em.set_footer(
            text=f"Command ran by {self.ctx.author.display_name} at {timestamp}",
            icon_url=self.ctx.author.display_avatar.with_static_format("png"))

        if self.values[0] == "Core":
            # overwrite the embed
            em.description = "</github:1146802715511492670>: view the bots github repo\n</invite:1146802715511492668>: invite the bot to your server\n</ping:1145445177092231339>: show bot and API latency\n</support:1146802715511492669>: join the support server\n",
            em.title = "Core Commands"
            await interaction.response.edit_message(embed=em)

        elif self.values[0] == "Option 2":
            #handle more options
            pass

        elif self.values[0] == "Option 3":
            pass


class HelpView(discord.ui.View):
    def __init__(self, ctx, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Help(ctx=ctx))
