import logging
from datetime import datetime

import motor.motor_asyncio

from database.guild_entry import Guild
from database.user_entry import User


class DiscordDatabase:
    def __init__(self, mongo_uri, database_name, user_collection_name, guild_collection_name):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.user_collection_name = user_collection_name
        self.guild_collection_name = guild_collection_name
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.user_collection = self.client[self.database_name][self.user_collection_name]
        self.guild_collection = self.client[self.database_name][self.guild_collection_name]
        self.log = logging.getLogger()

    async def get_user(self, guild_id: int, user_id: int):
        # TODO: Figure out if MongoDB has a way of just returning the user document directly
        guild_data = await self.guild_collection.find_one({'guild_id': int(guild_id), 'users.user_id': int(user_id)})
        if guild_data:
            user_data = next((user for user in guild_data['users'] if user['user_id'] == user_id), None)
            #print(f'found user: {user_data}')
            if user_data:
                user_data.update({'guild_id': guild_id})  # Insert guild_id into user_data if it doesn't already exist.
                expected_fields = User.__slots__

                for field in user_data:
                    if field not in expected_fields:
                        user_data.pop(field)

                return User(self, **user_data)
        
        user = User.create(self, user_id, guild_id)
        await user.save(guild_id=guild_id)
        return user

    async def set_user(self, guild_id: int, user_data: User):
        await self.guild_collection.update_one(
             # Insert into guilds where _id = guild_id, if there are no existing user documents with user_id
            {'guild_id': guild_id, 'users.user_id': {'$ne': user_data.user_id}},
            {'$addToSet': {'users': user_data.to_dict()}}
        )

    async def retrieve_user(self, guild_id, user_id):
        ...

    async def update_guild_user(self, guild_id, user_id, user_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id, "users.user_id": user_id},  # prev: users: user_id
            {"$set": {"users.$": user_data.to_dict()}}
        )

    # User operations
    def initialize_default_user_data(self, user_data):
        default_data = {
            "blacklist": False,
            "last_seen": f'{datetime.utcnow()}',
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
        # Create a new dictionary with default values and update it with existing data
        user_data = {**default_data, **user_data}
        user_data.pop("health", None)
        user_data.pop("idiot_data", None)
        user_data.pop("weekly_streak", None)
        return user_data

    async def get_top_users_by_level(self, limit):
        pipeline = [
            {"$sort": {"level": -1}},
            {"$limit": limit},
            {"$project": {"_id": 0}}
        ]
        top_users = await self.user_collection.aggregate(pipeline).to_list(None)
        return top_users

    async def get_top_users_by_bank_balance(self, limit):
        pipeline = [
            {"$sort": {"bank_balance": -1}},
            {"$limit": limit},
            {"$project": {"_id": 0}}
        ]
        top_users = await self.user_collection.aggregate(pipeline).to_list(None)
        return top_users

    async def get_top_users_by_balance(self, limit):
        pipeline = [
            {"$sort": {"balance": -1}},
            {"$limit": limit},
            {"$project": {"_id": 0}}
        ]
        top_users = await self.user_collection.aggregate(pipeline).to_list(None)
        return top_users

    async def get_top_users_by_combined_balance(self, limit):
        pipeline = [
            {"$addFields": {"combined_balance": {
                "$add": ["$balance", "$bank_balance"]}}},
            {"$sort": {"combined_balance": -1}},
            {"$limit": limit},
            {"$project": {"_id": 0}}
        ]
        top_users = await self.user_collection.aggregate(pipeline).to_list(None)
        return top_users

    async def get_all_users(self):
        all_users = []
        async for guild in self.guild_collection.find({}, {"_id": 0}):
            for user_data in guild["users"]:
                # Provide default values for missing attributes
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

    async def add_user(self, user):
        await self.user_collection.insert_one(user.to_dict())

    # async def get_user(self, user_id):
    #     user_data = await self.user_collection.find_one({"user_id": user_id}, {"_id": 0})
    #     if user_data:
    #         user_data = self.initialize_default_user_data(user_data)
    #         return User(self, **user_data)
    #     user = User(self, user_id, False,
    #                 f'{datetime.utcnow()}', 0, 0, False, 0, 0, {}, 0, {})
    #     await self.add_user(user)
    #     user_data = await self.user_collection.find_one({"user_id": user_id}, {"_id": 0})
    #     user_data = self.initialize_default_user_data(user_data)
    #     return User(self, **user_data)

    async def update_user(self, user_id, new_data):
        await self.user_collection.update_one({"user_id": user_id}, {"$set": new_data})

    async def delete_user(self, user_id):
        await self.user_collection.delete_one({"user_id": user_id})

    # Guild operations
    async def add_guild(self, guild):
        await self.guild_collection.insert_one(guild.__dict__)

    async def get_guild(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id}, {"_id": 0})
        if guild_data:
            guild_data.setdefault("lvl_roles", [])
            guild_data.setdefault("bonus_roles", [])
            guild_data.setdefault("shop_roles", {})
            guild_data.setdefault("users", [])
            return Guild(**guild_data)
        guild = Guild(guild_id)
        await self.add_guild(guild)
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id}, {"_id": 0})
        guild_data.setdefault("lvl_roles", [])
        guild_data.setdefault("bonus_roles", [])
        guild_data.setdefault("shop_roles", {})
        guild_data.setdefault("users", [])
        return Guild(**guild_data)

    async def update_guild(self, guild_id, new_data):
        await self.guild_collection.update_one({"guild_id": guild_id}, {"$set": new_data})

    async def delete_guild(self, guild_id):
        await self.guild_collection.delete_one({"guild_id": guild_id})

    async def add_ticket(self, guild_id, ticket_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$push": {"tickets": ticket_data}}
        )

    async def add_support_ticket(self, guild_id, ticket_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$push": {"support_tickets": ticket_data}}
        )

    async def get_tickets(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id})
        if guild_data and "tickets" in guild_data:
            return guild_data["tickets"]
        return []

    async def update_ticket(self, guild_id, channel_id, new_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id, "tickets.channel_id": channel_id},
            {"$set": {"tickets.$": new_data}}
        )

    async def delete_ticket(self, guild_id, channel_id):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$pull": {"tickets": {"channel_id": channel_id}}}
        )

    async def add_shop_role(self, guild_id, role_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$push": {"shop_roles": role_data}}
        )

    async def get_shop_roles(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id})
        if guild_data and "shop_roles" in guild_data:
            return guild_data["shop_roles"]
        return []

    async def update_shop_role(self, guild_id, role_id, new_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id, "shop_roles._id": role_id},
            {"$set": {"shop_roles.$": new_data}}
        )

    async def delete_shop_role(self, guild_id, role_id):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$pull": {"shop_roles": {"_id": role_id}}}
        )
