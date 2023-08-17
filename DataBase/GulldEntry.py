class Guild:
    def __init__(self, guild_id, member_data=None, tickets=None, config=None):
        self.guild_id = guild_id
        self.member_data = member_data if member_data else []
        self.tickets = tickets if tickets is not None else []
        self.config = config if config else {}


