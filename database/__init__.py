import logging
from datetime import datetime, timezone
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

    async def get_top_users(self, field, limit):
        pipeline = [
            {"$sort": {field: -1}},
            {"$limit": limit},
            {"$project": {"_id": 0}}
        ]
        top_users = await self.user_collection.aggregate(pipeline).to_list(None)
        return top_users

    async def get_all_users(self):
        all_users = []
        async for user_data in self.user_collection.find({}, {"_id": 0}):
            user_data = self._provide_default_user_attributes(user_data)
            all_users.append(user_data)
        return all_users

    @staticmethod
    def _provide_default_user_attributes(user_data):
        defaults = {
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
            "last_daily_claim": None,
            "last_weekly_claim": None,
            "weekly_streak": 0,
            "daily_streak": 0,
        }
        user_data.update((key, value) for key, value in defaults.items() if key not in user_data)
        return user_data

    async def get_users_in_jail(self):
        users_in_jail = []
        all_users = await self.get_all_users()

        for user_data in all_users:
            user = User(**user_data)
            if user.is_in_jail():
                users_in_jail.append(user.user_id)

        return users_in_jail

    async def add_user(self, user):
        await self.user_collection.insert_one(user.__dict__)

    async def get_user(self, user_id):
        user_data = await self.user_collection.find_one({"user_id": user_id}, {"_id": 0})
        if user_data:
            user_data = self._provide_default_user_attributes(user_data)
            return User(**user_data)

        user = User(user_id, False, f'{datetime.utcnow()}', 0, 0, False, 0, 0, {}, 0, {})
        await self.add_user(user)
        user_data = await self.user_collection.find_one({"user_id": user_id}, {"_id": 0})
        return User(**user_data)

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
            return Guild(**guild_data)

        guild = Guild(guild_id)
        await self.add_guild(guild)
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id}, {"_id": 0})
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
