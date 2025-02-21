import discord
import json
from discord.ext import commands
from pathlib import Path


class CountingCog(commands.Cog):
    def __init__(self, bot: commands.Bot, channel_id: int, data_file: str = "count_data.json"):
        """
        Initialize the cog.

        :param bot: The bot instance.
        :param channel_id: The ID of the channel where counting takes place.
        :param data_file: The file path for storing the count data.
        """
        self.bot = bot
        self.channel_id = channel_id
        self.data_file = Path(data_file)
        self.current_number = 0

        # Load the count from the file
        self.load_count()

    def load_count(self):
        """
        Loads the saved count from the file. Creates the file if it doesn't exist.
        """
        if self.data_file.exists():
            with self.data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.current_number = data.get(str(self.channel_id), 0)
        else:
            # Create the file if it doesn't exist
            with self.data_file.open("w", encoding="utf-8") as f:
                json.dump({}, f)

    def save_count(self):
        """
        Saves the current count to the file.
        """
        if not self.data_file.exists():
            data = {}
        else:
            with self.data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)

        # Update the count for the specific channel
        data[str(self.channel_id)] = self.current_number

        with self.data_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Listener to handle counting logic.
        Deletes messages that do not match the next number.
        Updates the channel topic with the current number.
        """
        # Ignore messages from bots or messages outside the specific channel
        if message.author.bot or message.channel.id != self.channel_id:
            return

        # Check if the message is a number
        if message.content.isdigit():
            number = int(message.content)
            if number == self.current_number + 1:
                # Update the count
                self.current_number = number
                #await self.update_channel_topic(message.channel)
                self.save_count()  # Persist the updated count

            else:
                # Delete incorrect message
                await message.delete()
        else:
            # Delete non-numeric messages
            await message.delete()

    async def update_channel_topic(self, channel: discord.TextChannel):
        """
        Updates the channel topic with the current number.
        """
        try:
            await channel.edit(topic=f"The current number is: {self.current_number}")
        except discord.Forbidden:
            # Lacks permission; log a warning
            self.bot.log.warning(f"Could not update topic in channel {channel.name}. Missing permissions.")

    @commands.command(name="resetcount")
    @commands.has_permissions(manage_channels=True)
    async def reset_count(self, ctx: commands.Context, start: int = 0):
        """
        Resets the count to a specific number.
        Only accessible by users with the `manage_channels` permission.
        """
        if ctx.channel.id != self.channel_id:
            return await ctx.send("This command can only be used in the counting channel.")

        self.current_number = start
        self.save_count()  # Persist the reset count
        await self.update_channel_topic(ctx.channel)
        await ctx.send(f"The count has been reset to {start}.")


async def setup(bot: commands.Bot):
    """
    Cog setup function to initialize CountingCog.

    :param bot: The bot instance
    """
    channel_id = 1342296986539528304  # Replace with your specific channel ID
    await bot.add_cog(CountingCog(bot, channel_id))
