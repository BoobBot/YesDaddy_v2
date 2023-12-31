import traceback

import discord
from discord.ext import commands


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

    @staticmethod
    def extract_traceback_info(traceback_obj):
        traceback_info = {
            'error_type': traceback_obj.__class__.__name__,
            'error_message': str(traceback_obj),
            'file_name': '',
            'line_number': 0,
            'function_calls': [],
            'local_variables': {},
            'stack_context': '',
        }

        if traceback_obj.__traceback__:
            tb = traceback_obj.__traceback__
            tb_frame = tb.tb_frame
            traceback_info['file_name'] = tb_frame.f_code.co_filename
            traceback_info['line_number'] = tb.tb_lineno

            # Extract function calls
            while tb_frame:
                traceback_info['function_calls'].append(
                    tb_frame.f_code.co_name)
                tb_frame = tb_frame.f_back

            # Extract local variables from the most recent frame
            if traceback_info['function_calls']:
                locals_dict = traceback_info['local_variables']
                locals_dict.update(tb.tb_frame.f_locals)

        return traceback_info

    @staticmethod
    def format_traceback_info(traceback_info):
        calls = '\n'.join(traceback_info['function_calls'])
        variables = '\n'.join([f'{var_name}: {var_value}' for var_name,
        var_value in traceback_info['local_variables'].items()])
        error_message = f"**Error Type:** {traceback_info['error_type']}\n**Error Message:** {traceback_info['error_message']}\n"
        error_message += f"**File:** {traceback_info['file_name']}, Line: {traceback_info['line_number']}\n\n"
        error_message += f"**Function Calls:**\n{calls}\n\n"
        error_message += f"**Local Variables:**\n{variables}\n\n"
        error_message += f"**Stack Context:** {traceback_info['stack_context']}\n\n"
        return error_message

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
            await ctx.send("An error occurred while processing the command.")
            traceback_info = self.extract_traceback_info(traceback_obj=error)
            error_message = self.format_traceback_info(traceback_info)
            traceback_info = traceback.format_exc()
            self.logger.error(f"An error occurred: {error}")
            self.logger.error(f"Traceback:\n{traceback_info}")
            self.logger.error(f"Traceback:\n{error_message}")
            # Get the traceback information as a formatted string
            traceback_info = "".join(traceback.format_exception(type(error), error, error.__traceback__))
            self.logger.error(traceback_info)
            await self.send_error_to_webhook(f'```{traceback_info}```')
            await self.send_error_to_webhook(f"An error occurred: {error}\n\nTraceback:```\n{error_message}```")


async def setup(bot):
    await bot.add_cog(ErrorHandlerCog(bot))
