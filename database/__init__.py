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
        self.user_collection_name = user_collection_name
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.guild_collection = self.client[self.database_name][self.guild_collection_name]
        self.user_collection = self.client[self.database_name][self.user_collection_name]
        self.log = logging.getLogger()

    #############################################
    # User operations                           #
    #############################################

    async def get_user(self, guild_id: int, user_id: int):
        user_data = await self.user_collection.find_one({'guild_id': int(guild_id), 'user_id': int(user_id)})
        if user_data:
            user_data['guild_id'] = guild_id  # Insert guild_id into user_data if it doesn't already exist.
            return User.from_existing(self, user_data)
        user = User.create(self, user_id, guild_id)
        await user.save(guild_id=guild_id)
        return user

    async def set_user(self, user_data: dict):
        await self.user_collection.update_one({'guild_id': user_data['guild_id'], 'user_id': user_data['user_id']},
                                              {'$set': user_data}, upsert=True)

    async def update_guild_user(self, user_data: dict):
        await self.user_collection.update_one({'guild_id': user_data['guild_id'], 'user_id': user_data['user_id']},
                                              {'$set': user_data})

    async def update_guild_user_data(self, guild_id, user_id, updated_fields):
        await self.user_collection.update_one({'guild_id': guild_id, 'user_id': user_id},
                                              {'$set': updated_fields})

    async def get_users_in_guild(self, guild_id):
        users = await self.user_collection.find({'guild_id': int(guild_id)}).to_list(length=None)
        return [User.from_existing(self, user) for user in users]

    async def get_all_users(self):
        users = await self.user_collection.find({}).to_list(length=None)
        return [User.from_existing(self, user) for user in users]

    async def get_users_in_jail(self):
        users_in_jail = []
        all_users = await self.get_all_users()
        for user_data in all_users:
            user = await self.get_user(user_data["guild_id"], user_data["user_id"])
            if user.is_in_jail():
                users_in_jail.append(user)
        return users_in_jail

    async def get_top_users(self, guild_id, limit, sort_key):
        users = await self.get_users_in_guild(guild_id)
        sorted_users = sorted(users, key=sort_key, reverse=True)
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

    async def update_support_ticket(self, guild_id, channel_id, new_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id, "support_tickets.channel_id": channel_id},
            {"$set": {"support_tickets.$": new_data}}
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

    async def add_cash_role(self, guild_id, role_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$push": {"bonus_cash_roles": role_data}}
        )

    async def get_cash_roles(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id})
        if guild_data and "bonus_cash_roles" in guild_data:
            return guild_data["bonus_cash_roles"]
        return []

    async def update_cash_role(self, guild_id, role_id, new_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id, "bonus_cash_roles._id": role_id},
            {"$set": {"bonus_cash_roles.$": new_data}}
        )

    async def delete_cash_role(self, guild_id, role_id):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$pull": {"bonus_cash_roles": {"_id": role_id}}}
        )


    async def add_shop_gift(self, guild_id, gift_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$push": {"shop_gifts": gift_data}}
        )

    async def get_shop_gifts(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id})
        if guild_data and "shop_gifts" in guild_data:
            return guild_data["shop_gifts"]
        return []

    async def delete_shop_gift(self, guild_id, gift_id):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$pull": {"shop_gifts": {"_id": gift_id}}}
        )

    async def add_reminder(self, guild_id, reminder_data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$push": {"reminders": reminder_data}}
        )

    async def get_reminders(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id})
        if guild_data and "reminders" in guild_data:
            return guild_data["reminders"]
        return []

    async def get_all_reminders(self):
        all_reminders = []
        async for guild in self.guild_collection.find({}, {"_id": 0}):
            if "reminders" in guild:
                all_reminders.extend(guild["reminders"])
        return all_reminders

    async def delete_reminder(self, guild_id, reminder_id):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$pull": {"reminders": {"_id": reminder_id}}}
        )

    async def add_new_member(self, guild_id, data):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$push": {"new_role": data}}
        )

    async def get_new_member(self, guild_id):
        guild_data = await self.guild_collection.find_one({"guild_id": guild_id})
        if guild_data and "new_role" in guild_data:
            return guild_data["new_role"]
        return []

    async def get_all_new_members(self):
        new_members = []
        async for guild in self.guild_collection.find({}, {"_id": 0}):
            if "new_role" in guild:
                new_members.extend(guild["new_role"])
        return new_members

    async def delete_new_member(self, guild_id, member_id):
        await self.guild_collection.update_one(
            {"guild_id": guild_id},
            {"$pull": {"new_role": {"id": member_id}}}
        )


