from datetime import datetime, timedelta, timezone
from typing import Optional


class User:
    def __init__(self, db, user_id, guild_id, blacklist, last_seen, xp, level, premium, balance, bank_balance, cooldowns,
                 messages, jail, last_daily_claim=None, last_weekly_claim=None, daily_streak=0, inventory=None,
                 idiot=None):
        self._db = db
        self._new: bool = False  # Whether this User was retrieved from the database.
        self.user_id = user_id
        self.guild_id = guild_id
        self.blacklist = blacklist
        self.last_seen = last_seen
        self.xp = xp
        self.level = level
        self.premium = premium
        self.balance = balance
        self.bank_balance = bank_balance
        self.cooldowns = cooldowns
        self.messages = messages
        self.jail = jail or {}
        self.last_daily_claim = last_daily_claim
        self.last_weekly_claim = last_weekly_claim
        self.daily_streak = daily_streak
        self.inventory = inventory or {}
        self.idiot = idiot or {}

    def __getitem__(self, key):
        return super().__getattr__(key)  # Allows for self['a']

    def __setitem__(self, key, value):
        return super().__setattr__(key, value)  # Allows for self['a'] = value

    @classmethod
    def create(cls, db, user_id, guild_id) -> 'User':
        user = cls(db, user_id=user_id, guild_id=guild_id, blacklist=False, last_seen=datetime.utcnow(), xp=0, level=0,
                   premium=False, balance=0, bank_balance=0, cooldowns={}, messages=0, jail={})
        user._new = True
        return user

    def to_dict(self):
        fields = self.__dict__
        return {k: v for k, v in fields.items() if not k.startswith('_')}

    async def save(self):
        """
        This method stores the user within the database.
        This will not do anything if the user already exists.
        To update specific fields, you must use the applicable function or `update_field`.
        """
        await self._db.set_user(self)
        self._new = False

    async def update_fields(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

        if self._new:
            await self.save()
        else:
            # TODO SET IN DATABASE HERE
            ...

    async def jail_user(self, hours, fine):
        await self.update_fields(jail={'start_time': datetime.utcnow(), 'duration_hours': hours, 'fine': fine})

    def is_in_jail(self) -> Optional[datetime]:
        if not self.jail:
            return None

        start_time = self.jail["start_time"].replace(tzinfo=timezone.utc)
        duration = self.jail["duration_hours"]
        end_time = start_time + timedelta(hours=duration)
        return end_time

    async def add_xp(self, amount):
        await self.update_fields(xp=self.xp + amount)

    async def update_level(self, amount):
        await self.update_fields(level=amount)

    async def update_balance(self, amount):
        await self.update_fields(balance=max(amount, 0))

    async def add_balance(self, amount):
        await self.update_fields(balance=self.balance + max(amount, 0))

    async def subtract_balance(self, amount):
        await self.update_fields(balance=self.balance - max(amount, 0))

    async def update_bank_balance(self, amount):
        await self.update_fields(bank_balance=max(amount, 0))

    async def add_bank_balance(self, amount):
        await self.update_fields(bank_balance=self.bank_balance + max(amount, 0))

    async def update_last_seen(self):
        await self.update_fields(last_seen=datetime.utcnow())

    # async def update_cool_down(self):
    #     self.cooldowns = datetime.utcnow()
    #     await self.update_user({"cool_down": self.cool_down})

    async def update_messages(self):
        self.update_fields(messages=self.messages + 1)

    async def set_premium(self, premium: bool):
        if self.premium == premium:
            return

        await self.update_fields(premium=premium)

    async def set_blacklist(self, blacklist: bool):
        await self.update_fields(blacklist=blacklist)

    async def claim_daily(self):
        now = datetime.utcnow()

        if not self.last_daily_claim:
            await self.update_fields(daily_streak=1, last_daily_claim=now)
            return False, self.daily_streak

        days_since_last_claim = (now - self.last_daily_claim.replace(tzinfo=timezone.utc)).days

        if days_since_last_claim > 2:
            await self.update_fields(daily_streak=1, last_daily_claim=now)
            return True, self.daily_streak

        await self.update_fields(daily_streak=self.daily_streak + 1, last_daily_claim=now)
        return False, self.daily_streak

    async def claim_weekly(self):
        now = datetime.utcnow()
        if self.last_weekly_claim is None or (now - self.last_weekly_claim).days >= 7:
            # Check if the weekly streak is broken
            if (self.last_weekly_claim is not None and
                    (now - self.last_weekly_claim).days > 7):
                self.weekly_streak = 0  # Reset streak if broken

            # Claim the weekly reward
            money = 20000 + (self.weekly_streak * 5000)  # Add streak bonus
            self.last_weekly_claim = now
            self.weekly_streak += 1

            # Update user data and send an embed
            await self.update_fields(balance=money,
                                     weekly_streak=self.weekly_streak + 1,
                                     last_weekly_claim=now)
            return money, self.weekly_streak
        else:
            return 0, self.weekly_streak
