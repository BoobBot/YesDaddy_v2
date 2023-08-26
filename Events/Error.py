import discord
from discord.ext import commands

from utils.checks import persistent_cooldown


class ErrorHandlerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_url = self.bot.config.error_webhook
        self.webhook_username = "Reeeeeeeeeeeeeeeeeeeee"
        self.logger = bot.log

    async def send_error_to_webhook(self, error_message):
        async with self.bot.web_client.post(self.webhook_url,
                                            json={"content": error_message, "username": self.webhook_username}):
            pass

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        error = args[0]
        if isinstance(error, discord.HTTPException):
            return
        self.logger.error(f"An error occurred: {event}")
        await self.send_error_to_webhook(f"An error occurred: {event}, {error}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if hasattr(ctx.command, 'on_error'):
            return  # Ignore if the command has its own error handler

        error = getattr(error, 'original', error)  # Unwrap nested errors

        if isinstance(error, commands.CommandNotFound):
            return  # Ignore if command not found

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument given.")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Too many arguments provided.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Invalid input.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error occurred while executing the command.")
            self.logger.error(f"An error occurred: {error}")
            await self.send_error_to_webhook(f"An error occurred: {error}")
        elif isinstance(error, commands.CheckFailure):
            return  # Ignore if the user doesn't have the required permissions
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds.")
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("This command is already in use. Please wait.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages.")
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("This command can only be used in private messages.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("This command is currently disabled.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Only the bot owner can use this command.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing required permissions to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("The bot is missing required permissions to execute this command.")
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send("Extension not found.")
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send("Extension is already loaded.")
        elif isinstance(error, commands.ExtensionFailed):
            await ctx.send("Extension failed to load.")
        elif isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send("Extension is not loaded.")
        elif isinstance(error, commands.NoEntryPointError):
            await ctx.send("Extension does not have a proper entry point.")
        elif isinstance(error, commands.CommandRegistrationError):
            await ctx.send("Error occurred while registering a command.")
        elif isinstance(error, commands.GuildNotFound):
            await ctx.send("Specified guild was not found.")
        elif isinstance(error, commands.MessageNotFound):
            await ctx.send("Specified message was not found.")
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send("Specified channel was not found.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Specified member was not found.")
        elif isinstance(error, commands.UserNotFound):
            await ctx.send("Specified user was not found.")
        else:
            # Handle other unexpected errors
            await ctx.send("An error occurred while processing the command.")
            self.logger.error(f"An error occurred: {error}")
            await self.send_error_to_webhook(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(ErrorHandlerCog(bot))
