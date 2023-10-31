from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DiscordDatabase


class Guild:
    def __init__(self, db, guild_id, member_data=None, tickets=None, support_tickets=None, config=None, lvl_roles=[],
                 bonus_roles=[], text_reactions=None, shop_roles=[], shop_gifts=None, shop_items=None, users=[],
                 bonus_cash_roles=[], waifus=[], ping_tags=[]):
        self._db: 'DiscordDatabase' = db
        self.guild_id = guild_id
        self.member_data = member_data if member_data else []
        self.tickets = tickets if tickets is not None else []
        self.support_tickets = support_tickets if support_tickets is not None else []
        self.config = config if config else {}
        self.lvl_roles = lvl_roles if lvl_roles else []
        self.bonus_roles = bonus_roles if bonus_roles else []
        self.text_reactions = text_reactions if text_reactions else []
        self.shop_roles = shop_roles if shop_roles else []
        self.shop_gifts = shop_gifts if shop_gifts else []
        self.shop_items = shop_items if shop_items else []
        self.users = users if users else []
        self.bonus_cash_roles = bonus_cash_roles if bonus_cash_roles else []
        self.waifus = waifus if waifus else []
        self.ping_tags = ping_tags if ping_tags else []

    def to_dict(self):
        return {k: v for k, v in self.__dict__ if not k.startswith('_')}

    @classmethod
    def create(cls, db, guild_id: int):
        return cls(db, guild_id)

    @classmethod
    def from_existing(cls, db, data: dict):
        data.setdefault("lvl_roles", [])
        data.setdefault("bonus_roles", [])
        data.setdefault("shop_roles", [])
        data.setdefault("users", [])
        data.setdefault("bonus_cash_roles", [])
        data.setdefault("ping_tags", [])
        return cls(db, **data)

    async def save(self):
        return await self._db.add_guild(self)

    async def get_config(self, key):
        return self.config.get(key)

    async def set_config(self, key, value):
        self.config[key] = value
        await self.save_config()

    async def update_config(self, key, value):
        if key in self.config:
            self.config[key] = value
            await self.save_config()
        else:
            await self.set_config(key, value)

    async def save_config(self):
        if self.guild_id is not None:
            new_data = {"config": self.config}
            await self._db.update_guild(self.guild_id, new_data)

    async def create_waifu(self, user_id):
        waifu_data = {"user_id": user_id,
                      "owner_id": None,
                      "value": 1,
                      "affinity": None,
                      "affinity_changes": 0,
                      "divorce_count": 0,
                      "claimed": [],
                      "gifts": [],
                      }
        self.waifus.append(waifu_data)
        await self._db.update_guild(self.guild_id, {"waifus": self.waifus})
        return waifu_data

    async def get_waifu(self, user_id):
        for waifu in self.waifus:
            if waifu.get("user_id") == user_id:
                return waifu
        waifu = await self.create_waifu(user_id)
        return waifu

    def get_waifus_by_owner(self, owner_id):
        owned = []
        for waifu in self.waifus:
            if waifu.get("owner_id") == owner_id:
                owned.append(waifu)
        return owned

    async def update_waifu(self, waifu):
        for i, w in enumerate(self.waifus):
            if w.get("user_id") == waifu.get("user_id"):
                self.waifus[i] = waifu
                await self._db.update_guild(self.guild_id, {"waifus": self.waifus})
                return




