import asyncio
import logging
from datetime import datetime

import motor.motor_asyncio

from database.gulld_entry import Guild
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

    # User operations

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
        async for user_data in self.user_collection.find({}, {"_id": 0}):
            # Provide default values for missing attributes
            user_data.setdefault("blacklist", False)
            user_data.setdefault("last_seen", f'{datetime.utcnow()}')
            user_data.setdefault("xp", 0)
            user_data.setdefault("level", 0)
            user_data.setdefault("premium", False)
            user_data.setdefault("balance", 0)
            user_data.setdefault("bank_balance", 0)
            user_data.setdefault("cooldowns", {})
            user_data.setdefault("messages", 0)
            # Provide a default value for 'jail' attribute
            user_data.setdefault("jail", {})
            user_data.setdefault("idiot", {})
            user_data.pop("health", None)
            user_data.pop("idiot_data", None)
            all_users.append(user_data)
        return all_users

    async def get_users_in_jail(self):
        users_in_jail = []
        all_users = await self.get_all_users()

        for user_data in all_users:
            user_data.setdefault("blacklist", False)
            user_data.setdefault("last_seen", f'{datetime.utcnow()}')
            user_data.setdefault("xp", 0)
            user_data.setdefault("level", 0)
            user_data.setdefault("premium", False)
            user_data.setdefault("balance", 0)
            user_data.setdefault("bank_balance", 0)
            user_data.setdefault("cooldowns", {})
            user_data.setdefault("messages", 0)
            # Provide a default value for 'jail' attribute
            user_data.setdefault("jail", {})
            user_data.setdefault("idiot", {})
            user_data.pop("health", None)
            user_data.pop("idiot_data", None)

            user = User(self, **user_data)
            if user.is_in_jail():
                users_in_jail.append(user.user_id)

        return users_in_jail

    async def add_user(self, user):
        await self.user_collection.insert_one(user.to_dict())

    async def get_user(self, user_id):
        user_data = await self.user_collection.find_one({"user_id": user_id}, {"_id": 0})
        if user_data:
            # Provide default values for missing attributes
            user_data.setdefault("blacklist", False)
            user_data.setdefault("last_seen", f'{datetime.utcnow()}')
            user_data.setdefault("xp", 0)
            user_data.setdefault("level", 0)
            user_data.setdefault("premium", False)
            user_data.setdefault("balance", 0)
            user_data.setdefault("bank_balance", 0)
            user_data.setdefault("cooldowns", {})
            user_data.setdefault("messages", 0)
            # Provide a default value for 'jail' attribute
            user_data.setdefault("jail", {})
            user_data.setdefault("last_daily_claim", {})
            user_data.setdefault("last_weekly_claim", {})
            user_data.setdefault("weekly_streak", {})
            user_data.setdefault("daily_streak", {})
            user_data.setdefault("idiot", {})
            user_data.pop("health", None)
            user_data.pop("idiot_data", None)
            return User(self, **user_data)
        user = User(self, user_id, False,
                    f'{datetime.utcnow()}', 0, 0, False, 0, 0, {}, 0, {})
        await self.add_user(user)
        user_data = await self.user_collection.find_one({"user_id": user_id}, {"_id": 0})
        user_data.pop("health", None)
        user_data.pop("idiot_data", None)

        return User(self, **user_data)

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
            return Guild(**guild_data)
        guild = Guild(guild_id)
        await self.add_guild(guild)
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id}, {"_id": 0})
        guild_data.setdefault("lvl_roles", [])
        guild_data.setdefault("bonus_roles", [])
        guild_data.setdefault("shop_roles", {})
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
