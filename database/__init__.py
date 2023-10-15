import logging
from datetime import datetime

import motor.motor_asyncio

from database.guild_entry import Guild
from database.user_entry import User


class DiscordDatabase:
    def __init__(self, mongo_uri, database_name, user_collection_name, guild_collection_name):
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.guild_collection_name = guild_collection_name
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.guild_collection = self.client[self.database_name][self.guild_collection_name]
        self.log = logging.getLogger()

    #############################################
    # User operations                           #
    #############################################

    async def get_user(self, guild_id: int, user_id: int):
        guild_data = await self.guild_collection.find_one(
            {
                'guild_id': int(guild_id),
                'users.user_id': int(user_id)
            },
            projection={'users.$': 1}
        )

        if guild_data and 'users' in guild_data:
            user_data = guild_data['users'][0]
            user_data['guild_id'] = guild_id  # Insert guild_id into user_data if it doesn't already exist.
            return User.from_existing(user_data)

        user = User.create(self, user_id, guild_id)
        await user.save(guild_id=guild_id)
        return user

    async def set_user(self, guild_id: int, user_data: User):
        await self.guild_collection.update_one(
             # Insert into guilds where _id = guild_id, if there are no existing user documents with user_id
            {'guild_id': guild_id, 'users.user_id': {'$ne': user_data.user_id}},
            {'$addToSet': {'users': user_data.to_dict()}}
        )

    async def update_guild_user(self, guild_id, user_id, user_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id, "users.user_id": user_id},  # prev: users: user_id
            {"$set": {"users.$": user_data.to_dict()}}
        )

    async def get_users_in_guild(self, guild_id):
        guild_data = await self.guild_collection.find_one({'guild_id': int(guild_id)})

        if guild_data and 'users' in guild_data:
            return list(map(lambda user: User.from_existing(self, user), guild_data['users']))

        return []

    async def get_all_users(self):
        all_users = []

        async for guild in self.guild_collection.find({}, {"_id": 0}):
            if "users" in guild:
                all_users.extend(guild["users"])

        return all_users

    async def get_users_in_jail(self):
        users_in_jail = []
        all_users = await self.get_all_users()
        for user_data in all_users:
            # TODO: This could be optimised
            user = await self.get_user(user_data["guild_id"], user_data["user_id"])
            if user.is_in_jail():
                users_in_jail.append(user)
        return users_in_jail

    async def get_top_users(self, guild_id, limit, sort_key):
        users = await self.get_users_in_guild(guild_id)
        print(users)
        sorted_users = sorted(users, key=sort_key, reverse=True)
        print(sorted_users)
        return sorted_users[:limit]

    #############################################
    # Guild operations                          #
    #############################################
    async def add_guild(self, guild: Guild):
        await self.guild_collection.insert_one(guild.to_dict())

    async def get_guild(self, guild_id: int):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id}, {"_id": 0})

        if guild_data:
            return Guild.from_existing(self, guild_data)

        guild = Guild.create(self, guild_id)
        await guild.save()

        return guild

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
