import asyncio
import logging
import logging.handlers
import sys
from typing import List, Optional

import discord
import openai
from aiohttp import ClientSession
from discord.ext import commands
from motor import motor_asyncio

from config.config import Config
from database import DiscordDatabase
from utils.logger import setup_logger
from views import tickets_view, support_view, support_channel_view
from views.rule_button_view import RuleButton
from views.sc_view import ReferralView
from views.verification_view import VerificationView

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
config = Config()
openai.api_key = config.open_ai_key
bot_token = config.token

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

logger = setup_logger()
logger.setLevel(logging.INFO)
log = logging.getLogger()

debug = any('debug' in arg.lower() for arg in sys.argv) or config.debug_mode
if debug:
    log.info("Debug mode is on")
    bot_token = config.debug_token
    # logger.setLevel(logging.DEBUG)


class Bot(commands.Bot):
    def __init__(self, *args, initial_extensions: List[str],
                 db_client: motor_asyncio.AsyncIOMotorClient,
                 web_client: ClientSession,
                 testing_guild_id: Optional[int] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = db_client
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        self.config = config
        self.log = logging.getLogger()
        self.debug = debug

    async def setup_hook(self) -> None:
        self.add_view(VerificationView())
        self.add_view(tickets_view.TicketView())
        self.add_view(RuleButton())
        self.add_view(support_view.SupportTicketView())
        self.add_view(support_channel_view.SupportChannelView())
        self.add_view(ReferralView())
        self.remove_command('help')

        for extension in self.initial_extensions:
            self.log.info(f"Loading {extension}")
            await self.load_extension(extension)

        if self.testing_guild_id and config.sync_testing_guild:
            self.log.info(f"Syncing commands for guild {self.testing_guild_id}")
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            # await self.tree.sync(guild=guild)
            self.log.info(f"Synced commands for guild {self.testing_guild_id}")


async def main():
    async with ClientSession() as our_client:
        discord_db = DiscordDatabase(config.mongo_uri, config.database_name, config.user_collection_name,
                                     config.guild_collection_name)
        async with Bot(commands.when_mentioned, db_client=discord_db, web_client=our_client,
                       initial_extensions=config.initial_extensions, intents=intents,
                       testing_guild_id=config.testing_guild_id) as bot:
            await bot.start(config.token)


if __name__ == "__main__":
    log.info("Starting bot")
    asyncio.run(main())
