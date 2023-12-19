from datetime import datetime, timedelta, timezone
from typing import Optional

DEFAULT_DATA = {
    "blacklist": False,
    # "last_seen": f'{datetime.utcnow()}',
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


class User:
    __slots__ = (
        '__dict__', '_db', '_new', 'user_id', 'guild_id', 'blacklist', 'last_seen', 'xp', 'level', 'premium', 'balance',
        'bank_balance', 'cooldowns',
        'messages', 'jail', 'last_daily_claim', 'daily_streak', 'inventory', 'idiot', 'equipped_items', 'equipped_pets', 'equipped_title', 'stats')

    def __init__(self, db, user_id, guild_id, blacklist=False, last_seen=datetime.utcnow(), xp=0, level=0,
                 premium=False, balance=0, bank_balance=0,
                 cooldowns=None, messages=0, jail=None, last_daily_claim=None, daily_streak=0,
                 inventory=None,
                 idiot=None, equipped_items=None, equipped_pets=None, equipped_title=None, stats=None):
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
        self.cooldowns = cooldowns or {}
        self.messages = messages
        self.jail = jail or {}
        self.last_daily_claim = last_daily_claim
        self.daily_streak = daily_streak
        self.inventory = inventory or {}
        self.idiot = idiot or {}
        self.equipped_items = equipped_items or {}
        self.equipped_pets = equipped_pets or {}
        self.equipped_title = equipped_title or {}
        self.stats = stats or {}

        # ANY NEW FIELDS ADDED HERE *****MUST***** BE ADDED TO __slots__ TOO!!

        # Initialise with defaults (will not replace fields present with value 'None', however):
        # defaults = DEFAULT_DATA.copy()
        # defaults['last_seen'] = datetime.utcnow()
        # self.__dict__ = DEFAULT_DATA | self.__dict__

    def __getitem__(self, key):
        return super().__getattribute__(key)  # Allows for self['a']

    def __setitem__(self, key, value):
        return super().__setattr__(key, value)  # Allows for self['a'] = value

    @classmethod
    def create(cls, db, user_id, guild_id) -> 'User':
        """
        Creates an empty User object with default values.
        """
        user = cls(db, user_id=user_id, guild_id=guild_id)
        user._new = True
        return user
    
    @classmethod
    def from_existing(cls, db, data: dict):
        """
        Creates a user object from an existing dict.
        """
        expected_fields = cls.__slots__

        for field in data.copy():
            if field not in expected_fields:
                data.pop(field)

        return cls(db, **data)

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__slots__ if not attr.startswith('_')}

    async def save(self, guild_id: int):
        """
        This method stores the user within the database.
        This will not do anything if the user already exists.
        To update specific fields, you must use the applicable function or `update_fields`.
        """
        await self._db.set_user(guild_id, self)
        self._new = False

    async def update_fields(self, **kwargs):
        for key, value in kwargs.items():
            print(f"Updating {key} to {value}")
            self[key] = value

        if self._new:
            print("New user, saving...")
            await self.save(guild_id=self.guild_id)
        else:
            print("Existing user, updating...")
            for key, value in kwargs.items():
               await self._db.update_guild_user_data(self.guild_id, self.user_id, {key: value})
            #await self._db.update_guild_user(self.guild_id, self.user_id, self)

    def get_item_by_key(self, key, value, inventory_key):
        if inventory_key in self.inventory:
            for item in self.inventory[inventory_key]:
                if item.get(key) == value:
                    return item
        return None

    async def set_item_by_key(self, key, value, new_item, inventory_key):
        if inventory_key in self.inventory:
            for item in self.inventory[inventory_key]:
                if item.get(key) == value:
                    item.update(new_item)
                    await self.update_fields(inventory=self.inventory)
                    return
            # If the item with the specified key-value pair doesn't exist, add it.
            self.inventory[inventory_key].append(new_item)
            await self.update_fields(inventory=self.inventory)

        else:
            # If the inventory_key doesn't exist, create a new list with the new item.
            self.inventory[inventory_key] = [new_item]
            await self.update_fields(inventory=self.inventory)

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
        await self.update_fields(messages=self.messages + 1)

    async def set_premium(self, premium: bool):
        if self.premium == premium:
            return

        await self.update_fields(premium=premium)

    async def set_blacklist(self, blacklist: bool):
        if self.blacklist == blacklist:
            return

        await self.update_fields(blacklist=blacklist)

    async def claim_daily(self):
        now = datetime.utcnow()
        current_streak = self.daily_streak

        if not self.last_daily_claim:
            await self.update_fields(daily_streak=1, last_daily_claim=now)
            return False, self.daily_streak

        days_since_last_claim = (now.replace(tzinfo=timezone.utc) - self.last_daily_claim.replace(tzinfo=timezone.utc)).days
        print(days_since_last_claim)
        if days_since_last_claim > 2:
            await self.update_fields(daily_streak=1, last_daily_claim=now)
            return True, current_streak

        await self.update_fields(daily_streak=self.daily_streak + 1, last_daily_claim=now)
        return False, self.daily_streak

    def get_stat(self, stat):
        return self.stats.get(stat)

    async def update_stat(self, command: str, data: dict = None):
        if not self.stats.get(command):
            self.stats[command] = {
                "total_used": 0
            }
        if data:
            for key, value in data.items():
                if key in self.stats[command]:
                    self.stats[command][key] += value
                else:
                    self.stats[command][key] = value

                if key == "won":
                    if "win_streak" not in self.stats[command]:
                        self.stats[command]["win_streak"] = 0
                    if "longest_streak" not in self.stats[command]:
                        self.stats[command]["longest_streak"] = 0
                    self.stats[command]['win_streak'] += 1
                    if self.stats[command]['win_streak'] > self.stats[command]['longest_streak']:
                        self.stats[command]['longest_streak'] = self.stats[command]['win_streak']
                elif key == "lost" and "win_streak" in self.stats[command]:
                    self.stats[command]['win_streak'] = 0
        self.stats[command]["total_used"] += 1
        await self.update_fields(stats=self.stats)
