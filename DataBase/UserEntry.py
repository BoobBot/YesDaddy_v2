import math
import datetime


class User:
    def __init__(self, user_id, blacklist, last_seen, xp, level, premium, balance, bank_balance, cooldowns, messages, jail):
        self.user_id = user_id
        self.blacklist = blacklist
        self.last_seen = last_seen
        self.xp = xp
        self.level = level
        self.premium = premium
        self.balance = balance
        self.bank_balance = bank_balance
        self.cooldowns = cooldowns
        self.messages = messages
        self.jail = self.jail = jail if jail is not None else {}

    async def jail_user(self, hours, fine, bot):
        self.jail = {
            "start_time": datetime.datetime.now(datetime.timezone.utc),
            "duration_hours": hours,
            "fine": fine
        }
        await self.update_user({"jail": self.jail}, bot)

    def is_in_jail(self):
        if "jail" in self.jail:
            start_time = self.jail["start_time"].replace(tzinfo=datetime.timezone.utc)
            duration = self.jail["duration_hours"]
            end_time = start_time + datetime.timedelta(hours=duration)
            print("we did it")
            return end_time
        print("why are we working")
        return False

    async def add_xp(self, amount, bot):
        self.xp += amount
        await self.update_user({"xp": self.xp}, bot)

    async def update_level(self, amount, bot):
        self.level = amount
        await self.update_user({"level": self.level}, bot)

    async def add_balance(self, amount, bot):
        self.balance += amount
        await self.update_user({"balance": self.balance}, bot)

    async def subtract_balance(self, amount, bot):
        self.balance -= max(amount, 0)
        await self.update_user({"balance": self.balance}, bot)

    async def update_balance(self, amount, bot):
        self.balance = max(amount, 0)
        await self.update_user({"balance": self.balance}, bot)

    async def add_bank_balance(self, amount, bot):
        self.bank_balance += amount
        await self.update_user({"bank_balance": self.bank_balance}, bot)

    async def update_user(self, new_data, bot):
        await bot.db_client.update_user(self.user_id, new_data)

    async def update_last_seen(self, bot):
        self.last_seen = datetime.datetime.now(datetime.timezone.utc)
        await self.update_user({"last_seen": self.last_seen}, bot)

    # async def update_cool_down(self, bot):
    #     self.cooldowns = datetime.utcnow()
    #     await self.update_user({"cool_down": self.cool_down}, bot)

    async def update_messages(self, bot):
        self.messages += 1
        await self.update_user({"messages": self.messages}, bot)

    async def add_premium(self, bot):
        self.premium = True
        await self.update_user({"premium": self.premium}, bot)

    async def remove_premium(self, bot):
        self.premium = False
        await self.update_user({"premium": self.premium}, bot)

    async def add_blacklist(self, bot):
        self.blacklist = True
        await self.update_user({"blacklist": self.blacklist}, bot)

    async def remove_blacklist(self, bot):
        self.blacklist = False
        await self.update_user({"blacklist": self.blacklist}, bot)
