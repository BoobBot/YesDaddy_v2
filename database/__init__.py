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

    async def get_users_in_jail(self):
        users_in_jail = []
        async for guild in self.guild_collection.find({}):
            for user in guild.get("users", []):
                if user.get("jail", {}).get("start_time"):
                    users_in_jail.append(user.get("user_id"))
        return users_in_jail, guild

    ###########################################################
    # Guild operations                                        #
    ###########################################################

    async def get_all_guilds(self):
        all_guilds = []
        async for guild in self.guild_collection.find({},{"_id": 0}):
            guild.setdefault("lvl_roles", [])
            guild.setdefault("bonus_roles", [])
            guild.setdefault("shop_roles", {})
            all_guilds.append(Guild(self, **guild))
        return all_guilds

    async def add_guild(self, guild):
        await self.guild_collection.insert_one(guild.to_dict())

    async def get_guild(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id}, {"_id": 0})
        if guild_data:
            guild_data.setdefault("lvl_roles", [])
            guild_data.setdefault("bonus_roles", [])
            guild_data.setdefault("shop_roles", {})
            return Guild(self, **guild_data)
        guild = Guild(self, guild_id)
        await self.add_guild(guild)
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id}, {"_id": 0})
        guild_data.setdefault("lvl_roles", [])
        guild_data.setdefault("bonus_roles", [])
        guild_data.setdefault("shop_roles", {})
        return Guild(self, **guild_data)

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
