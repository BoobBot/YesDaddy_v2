class Guild:
    def __init__(self, guild_id, member_data=None, tickets=None,support_tickets=None, config=None, lvl_roles=None, bonus_roles=None):
        self.guild_id = guild_id
        self.member_data = member_data if member_data else []
        self.tickets = tickets if tickets is not None else []
        self.support_tickets = support_tickets if support_tickets is not None else []
        self.config = config if config else {}
        self.lvl_roles = lvl_roles if lvl_roles else []
        self.bonus_roles = bonus_roles if bonus_roles else []