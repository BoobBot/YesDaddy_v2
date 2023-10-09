class Guild:
    def __init__(self, guild_id, member_data=None, tickets=None, support_tickets=None, config=None, lvl_roles=None,
                 bonus_roles=None, text_reactions=None, shop_roles=None, shop_gifts=None, shop_items=None, users=None):
        self.guild_id = guild_id
        self.member_data = member_data if member_data else []
        self.tickets = tickets if tickets is not None else []
        self.support_tickets = support_tickets if support_tickets is not None else []
        self.config = config if config else {}
        self.lvl_roles = lvl_roles if lvl_roles else []
        self.bonus_roles = bonus_roles if bonus_roles else []
        self.text_reactions = text_reactions if text_reactions else []
        self.shop_roles = shop_roles if shop_roles else {}
        self.shop_gifts = shop_gifts if shop_gifts else {}
        self.shop_items = shop_items if shop_items else {}
        self.users = users if users else {}

    def add_user(self, user):
        self.users[user.id] = user

    # Add a method to get a user from the guild's user dictionary
    def get_user(self, user_id):
        return self.users.get(user_id)

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
