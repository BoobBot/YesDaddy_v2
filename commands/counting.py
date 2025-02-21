import discord
from discord.ext import commands


class CountingCog(commands.Cog):
    def __init__(self, bot: commands.Bot, channel_id: int):
        """
        Initialize the cog.

        :param bot: The bot instance.
        :param channel_id: The ID of the channel where counting takes place.
        """
        self.bot = bot
        self.channel_id = channel_id
        self.current_number = 0  # Tracks the current count
        self.collection = bot.db_client["discord_database"]["counting_data"]  # Replace with your DB/collection names

    async def cog_load(self):
        """
        Called when the cog is loaded.
        Retrieves the last known count from the database.
        """
        data = await self.collection.find_one({"channel_id": self.channel_id})
        if data:
            self.current_number = data.get("current_number", 0)
            self.bot.log.info(f"Resumed counting from {self.current_number} for channel {self.channel_id}.")
        else:
            self.current_number = 0
            await self.collection.insert_one({"channel_id": self.channel_id, "current_number": self.current_number})

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
                await self.update_channel_topic(message.channel)
                await self.save_count()  # Persist the updated count

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

    async def save_count(self):
        """
        Saves the current number to the database.
        """
        await self.collection.update_one(
            {"channel_id": self.channel_id},
            {"$set": {"current_number": self.current_number}},
            upsert=True
        )

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
        await self.save_count()  # Persist the reset count
        await self.update_channel_topic(ctx.channel)
        await ctx.send(f"The count has been reset to {start}.")


async def setup(bot: commands.Bot):
    """
    Cog setup function to initialize CountingCog.

    :param bot: The bot instance
    """
    channel_id = 1342296986539528304 # Replace with your specific channel ID
    await bot.add_cog(CountingCog(bot, channel_id))
