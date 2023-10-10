import datetime

from database.user_entry import User


class Guild:
    def __init__(self, db, guild_id, member_data=None, tickets=None, support_tickets=None, config=None, lvl_roles=None,
                 bonus_roles=None, text_reactions=None, shop_roles=None, shop_gifts=None, shop_items=None, users=None):
        self._db = db
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

    ###########################################################
    # Guild operations                                        #
    ###########################################################

    def to_dict(self):
        fields = self.__dict__
        return {k: v for k, v in fields.items() if not k.startswith('_')}

    async def update_guild(self):
        await self._db.update_guild(self.guild_id, self.to_dict())

###########################################################
    # User operations                                        #
    ###########################################################
    @staticmethod
    def initialize_default_user_data(user_data):
        default_data = {
            "blacklist": False,
            "last_seen": f'{datetime.datetime.utcnow()}',
            "xp": 0,
            "level": 0,
            "premium": False,
            "balance": 0,
            "bank_balance": 0,
            "cooldowns": {},
            "messages": 0,
            "jail": {},
            "idiot": {},
        }
        user_data = {**default_data, **user_data}
        user_data.pop("health", None)
        user_data.pop("idiot_data", None)
        user_data.pop("weekly_streak", None)
        return user_data

    # async def get_top_users_by_level(self, limit):
    #     pipeline = [
    #         {"$sort": {"level": -1}},
    #         {"$limit": limit},
    #         {"$project": {"_id": 0}}
    #     ]
    #     top_users = await self.user_collection.aggregate(pipeline).to_list(None)
    #     return top_users
    #
    # async def get_top_users_by_bank_balance(self, limit):
    #     pipeline = [
    #         {"$sort": {"bank_balance": -1}},
    #         {"$limit": limit},
    #         {"$project": {"_id": 0}}
    #     ]
    #     top_users = await self.user_collection.aggregate(pipeline).to_list(None)
    #     return top_users
    #
    # async def get_top_users_by_balance(self, limit):
    #     pipeline = [
    #         {"$sort": {"balance": -1}},
    #         {"$limit": limit},
    #         {"$project": {"_id": 0}}
    #     ]
    #     top_users = await self.user_collection.aggregate(pipeline).to_list(None)
    #     return top_users
    #
    # async def get_top_users_by_combined_balance(self, limit):
    #     pipeline = [
    #         {"$addFields": {"combined_balance": {
    #             "$add": ["$balance", "$bank_balance"]}}},
    #         {"$sort": {"combined_balance": -1}},
    #         {"$limit": limit},
    #         {"$project": {"_id": 0}}
    #     ]
    #     top_users = await self.user_collection.aggregate(pipeline).to_list(None)
    #     return top_users

    async def get_all_users(self):
        all_users = []
        for user_data in self.users.values():
            user_data = self.initialize_default_user_data(user_data)
            all_users.append(user_data)
        return all_users

    async def get_users_in_jail(self):
        users_in_jail = []
        all_users = await self.get_all_users()

        for user_data in all_users:
            user_data = self.initialize_default_user_data(user_data)
            user = User(self, **user_data)
            if user.is_in_jail():
                users_in_jail.append(user.user_id)

        return users_in_jail
    def get_top_users_by_level(self, limit):
        top_users = list(self.users.values())
        top_users.sort(key=lambda user: user.level, reverse=True)
        return top_users[:limit]

    def add_user(self, user):
        self.users[str(user.user_id)] = user.to_dict()

    def get_user(self, user_id):
        user_data = self.users.get(str(user_id))
        if user_data:
            user_data = self.initialize_default_user_data(user_data)
            return User(self, **user_data)
        user = User(self._db, user_id, False,
                    f'{datetime.datetime.utcnow()}', 0, 0, False, 0, 0, {}, 0, {})
        self.add_user(user)
        user_data = self.users.get(str(user_id))
        user_data = self.initialize_default_user_data(user_data)
        return User(self._db, **user_data)

    async def update_user(self, user_id, new_data):
        user = self.users.get(str(user_id))
        if user:
            for key, value in new_data.to_dict().items():
                setattr(user, key, value)
            await self.update_guild()

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]