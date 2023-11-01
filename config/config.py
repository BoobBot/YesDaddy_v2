import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from ..env file


class Config:
    def __init__(self):
        self.token = os.getenv('DISCORD_TOKEN',
                               "")  # Use environment variable as token
        # Use environment variable as debug_mode
        self.debug_mode = os.getenv('DEBUG_MODE', False)
        self.debug_token = os.getenv('DEBUG_TOKEN',
                                     "")  # Use environment variable as debug_token
        self.sync_testing_guild = os.getenv('SYNC_TESTING_GUILD',
                                            False)  # Use environment variable as sync_testing_guild_id
        # Use environment variable as mongo_uri
        self.mongo_uri = os.getenv('MONGO_URI', "")
        # Use environment variable as database_name
        self.database_name = os.getenv('DATABASE_NAME', "")
        self.user_collection_name = os.getenv('USER_COLLECTION_NAME',
                                              "users")  # Use environment variable as user_collection_name
        self.guild_collection_name = os.getenv('GUILD_COLLECTION_NAME',
                                               "guilds")  # Use environment variable as guild_collection_name
        self.testing_guild_id = os.getenv('TESTING_GUILD_ID',
                                          "")  # Use environment variable as testing_guild_id
        self.initial_extensions = ['commands.core', 'events.ready', 'events.message', 'events.loops', 'events.error',
                                   'commands.currency', 'commands.gambling', 'commands.profile',
                                   'commands.transactions', 'commands.dev', 'commands.moderation',
                                   'events.on_member_update', 'events.on_member_join',
                                   'events.on_command', 'commands.race']  # List of initial extensions
        # Use environment variable as prefix
        self.prefix = os.getenv('PREFIX', "")
        # Use environment variable as owner_ids
        self.owner_ids = os.getenv('OWNER_IDS', "")
        # Use environment variable as open_ai_key
        self.open_ai_key = os.getenv('OPEN_AI_KEY', "")
        # Use environment variable as member_role_id
        self.member_role_id = os.getenv('MEMBER_ROLE_ID', "")
        self.verification_image = os.getenv('VERIFICATION_IMAGE',
                                            "")  # Use environment variable as verification_image
        # Use environment variable as error_webhook
        self.error_webhook = os.getenv('ERROR_WEBHOOK', "")

    def get_token(self, debug=False):  # Get token
        if self.debug_mode or debug:  # If debug_mode is True
            return self.debug_token  # Return debug_token
        return self.token  # Return token

    # TODO scrub tokens
    def __repr__(self):  # Representation of Config
        return f"<Config token={self.token} debug_mode={self.debug_mode} debug_token={self.debug_token} " \
               f"mongo_uri={self.mongo_uri} database_name={self.database_name} " \
               f"user_collection_name={self.user_collection_name} " \
               f"guild_collection_name={self.guild_collection_name} " \
               f"testing_guild_id={self.testing_guild_id} " \
               f"initial_extensions={self.initial_extensions} prefix={self.prefix} owner_ids={self.owner_ids}>"

    # TODO scrub tokens
    def __str__(self):  # String representation of Config
        return f"Config(token={self.token}, debug_mode={self.debug_mode}, debug_token={self.debug_token}, " \
               f"mongo_uri={self.mongo_uri}, database_name={self.database_name}, " \
               f"user_collection_name={self.user_collection_name}, " \
               f"guild_collection_name={self.guild_collection_name}, " \
               f"testing_guild_id={self.testing_guild_id}, " \
               f"initial_extensions={self.initial_extensions}, prefix={self.prefix}, " \
               f"owner_ids={self.owner_ids})"  # Return string representation of Config
