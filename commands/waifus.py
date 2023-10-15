import math
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


from common.functions.formats import is_emoji



class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.affinity_worth = 1.25
        self.overclaim = 1.10

    waifu = app_commands.Group(name="waifu", description="Manage your waifus")
    gift = app_commands.Group(parent=waifu, name="gift", description="Mange waifu gifts")

    async def sync_top_10(self):
        data = await self.bot.pool.fetch(
            "SELECT waifu AS id, waifu_value FROM waifus w FULL JOIN new_users nu on w.waifu = nu.id ORDER BY waifu_value DESC LIMIT 10")
        guild = self.bot.get_guild(1091163666071687168)
        role = guild.get_role(1128418391158427728)
        to_remove = [x.id for x in role.members]
        for waifu in data:
            member = guild.get_member(int(waifu["id"]))
            if not member:
                continue
            if role not in member.roles:
                await member.add_roles(role, reason="Top 10 waifu status achieved")
            if int(waifu["id"]) in to_remove:
                to_remove.remove(int(waifu["id"]))
        for waifu in to_remove:
            member = guild.get_member(waifu)
            if not member:
                continue
            if role not in member.roles:
                continue
            await member.remove_roles(role, reason="Top 10 waifu status lost")

    @waifu.command(name="set_affinity", description="Set your affinity, this users gifts/claims will be worth more!")
    async def waifu_set_affinity(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(thinking=True)
        author = interaction.user
        em = discord.Embed(color=0xF8C8DC)
        if user.id == interaction.user.id:
            em.colour = discord.Color.red()
            em.description = "You can't make yourself your waifu!"
            return await interaction.followup.send(embed=em)
        try:

            await self.bot.pool.execute(
                "UPDATE new_users SET affinity=$2, affinity_changes=affinity_changes+1 WHERE id=$1",
                str(author.id),
                str(user.id)
            )
        except Exception:
            em.colour = discord.Color.red()
            em.description = "Some kinda error idk let Kanin know"
            return await interaction.followup.send(embed=em, content=None)
        em.description = f"{author.mention} set {user.mention} as their affinity!"
        await interaction.followup.send(embed=em, content=None)

    @waifu.command(name="claim", description="Claim a waifu")
    async def waifu_claim(self, interaction: discord.Interaction, waifu: discord.Member,
                          value: app_commands.Range[int, 1]):
        await interaction.response.defer(thinking=True)
        author = interaction.user
        em = discord.Embed(color=0xF8C8DC)
        orig_value = value

        if author.id == waifu.id:
            em.colour = discord.Color.red()
            em.description = "That's weird... go make some friends."
            return await interaction.followup.send(embed=em)

        waifu_data = await self.bot.pool.fetchrow("SELECT * FROM waifus WHERE waifu=$1", str(waifu.id))
        if waifu_data and waifu_data["owner"] == str(author.id):
            em.colour = discord.Color.red()
            em.description = "You already own that waifu! Raise their value by giving them gifts!"
            return await interaction.followup.send(embed=em, content=None)

        balance = await self.bot.pool.fetchval("SELECT balance FROM new_users WHERE id=$1", str(author.id))
        if balance < value:
            em.colour = discord.Color.red()
            em.description = "You can't afford that whore, try again!"
            return await interaction.followup.send(embed=em, content=None)

        waifu_user_data = await self.bot.pool.fetchrow("SELECT * FROM new_users WHERE id=$1", str(waifu.id))
        if not waifu_user_data:
            em.colour = discord.Color.red()
            em.description = "That user isn't in my database... try claiming someone that exists"
            return await interaction.followup.send(embed=em)
        if waifu_user_data["affinity"] == str(author.id):
            value = int(value * self.affinity_worth)
            waifu_value = waifu_user_data["waifu_value"] + 1
        elif not waifu_data:
            waifu_value = waifu_user_data["waifu_value"] + 1
        else:
            waifu_value = waifu_user_data["waifu_value"] * self.overclaim
        waifu_value = int(math.ceil(round(waifu_value, 2)))
        if value < waifu_value:
            em.colour = discord.Color.red()
            em.description = f"That waifu costs {self.bot.emoji('currency.coin')} {waifu_value:,}, try again!"
            return await interaction.followup.send(embed=em, content=None)

        if waifu_data:
            await self.bot.pool.execute("DELETE FROM waifus WHERE waifu=$1", str(waifu.id))
        async with self.bot.pool.acquire() as con:
            async with con.transaction():
                await con.execute(
                    "INSERT INTO waifus (owner, waifu) VALUES ($1, $2)",
                    str(author.id),
                    str(waifu.id)
                )
                await con.execute(
                    "UPDATE new_users SET waifu_value=$2 WHERE id=$1",
                    str(waifu.id),
                    value
                )
                await con.execute(
                    "UPDATE new_users SET balance=balance-$2 WHERE id=$1", str(author.id), orig_value
                )
        em.description = f"{author.mention} claimed {waifu.mention} as their waifu for {self.bot.emoji('currency.coin')} {value:,}!"
        await interaction.followup.send(
            content=f"{author.mention} claimed {waifu.mention} as their waifu for {self.bot.emoji('currency.coin')} {value:,}!",
            allowed_mentions=discord.AllowedMentions.all())
        await self.sync_top_10()

    @waifu.command(name="transfer", description="Give someone else your waifu! You pay 10% of their value!")
    async def waifu_transfer(self, interaction: discord.Interaction, waifu: str, member: discord.Member):
        await interaction.response.defer(thinking=True)
        author = interaction.user
        em = discord.Embed(color=0xF8C8DC)
        waifu = await self.bot.pool.fetchrow("SELECT waifu AS id, username FROM waifus w FULL JOIN user_cache uc ON w.waifu = uc.id WHERE owner=$1 AND waifu=$2", str(author.id), waifu)
        if not waifu:
            em.colour = discord.Color.red()
            em.description = "That's not your waifu!"
            return await interaction.followup.send(embed=em, content=None)
        waifu_value = await self.bot.pool.fetchval("SELECT waifu_value FROM new_users WHERE id=$1", waifu["id"])
        fee = int(math.ceil(round(waifu_value * .1, 2)))
        balance = await self.bot.pool.fetchval("SELECT balance FROM new_users WHERE id=$1", str(author.id))
        if balance < fee:
            return await interaction.followup.send(f"You can't afford to transfer that waifu! You need {fee:,}!")
        async with self.bot.pool.acquire() as con:
            async with con.transaction():
                await con.execute("UPDATE new_users SET balance=balance-$2 WHERE id=$1", str(author.id), fee)
                await con.execute("UPDATE waifus SET owner=$1 WHERE waifu=$2", str(member.id), waifu['id'])
        await interaction.followup.send(f"{author.mention} has transferred <@{int(waifu['id'])}> to {member.mention}!")
        await log_transaction(self.bot, author, -1 * fee, "transfer", reason=f"Gave {waifu['username']} to {member}")

    @waifu_transfer.autocomplete("waifu")
    async def divorce_autocomplete(self, interaction: discord.Interaction, current: str):
        data = await self.bot.pool.fetch(
            "SELECT waifu AS waifu_id, uc.username FROM waifus w FULL JOIN user_cache uc ON uc.id=w.waifu WHERE w.owner=$1",
            str(interaction.user.id))
        waifus = [
            app_commands.Choice(name=waifu["username"], value=waifu["waifu_id"])
            for waifu in data
            if not current or current.lower() in waifu["username"].lower()
        ]
        return waifus[:25]

    @waifu.command(name="divorce", description="Divorce a waifu")
    async def waifu_divorce(self, interaction: discord.Interaction, waifu: str):
        await interaction.response.defer(thinking=True)
        author = interaction.user
        em = discord.Embed(color=0xF8C8DC)
        em.colour = discord.Color.red()
        data = await self.bot.pool.fetch("SELECT waifu FROM waifus WHERE owner=$1", str(author.id))
        waifus = [x["waifu"] for x in data]
        if waifu not in waifus:
            em.description = "That's not your waifu!"
            return await interaction.followup.send(embed=em, content=None)
        waifu_user = await self.bot.fetch_user(int(waifu))
        await self.bot.pool.execute("DELETE FROM waifus WHERE waifu=$1", waifu)
        await self.bot.pool.execute("UPDATE new_users SET divorces=divorces+1 WHERE id=$1", str(author.id))
        em.description = f"{author.mention} has divorced {waifu_user.mention}!"
        await interaction.followup.send(content=f"{author.mention} has divorced {waifu_user.mention}!",
                                        allowed_mentions=discord.AllowedMentions.all())

    @waifu_divorce.autocomplete("waifu")
    async def divorce_autocomplete(self, interaction: discord.Interaction, current: str):
        data = await self.bot.pool.fetch(
            "SELECT waifu AS waifu_id, uc.username FROM waifus w FULL JOIN user_cache uc ON uc.id=w.waifu WHERE w.owner=$1",
            str(interaction.user.id))
        waifus = [
            app_commands.Choice(name=waifu["username"], value=waifu["waifu_id"])
            for waifu in data
            if not current or current.lower() in waifu["username"].lower()
        ]
        return waifus[:25]

    @staticmethod
    def create_embed_fields(text, character_limit=1024):
        lines = text.split('\n\n')

        fields = []
        current_field = ""
        for line in lines:
            if len(current_field) + len(line) + 1 > character_limit:
                fields.append(current_field.strip())
                current_field = ""
            current_field += line + "\n\n"

        if current_field:
            fields.append(current_field.strip())

        return fields

    @gift.command(name="inventory", description="View your inventory of gifts")
    async def waifu_gift_inventory(self, interaction: discord.Interaction, waifu: Optional[discord.Member]):
        await interaction.response.defer(thinking=True)
        waifu = waifu or interaction.user
        data = await self.bot.pool.fetch(
            "SELECT * FROM waifu_gift_inventory wgi FULL JOIN waifu_gifts wg on wg.name = wgi.gift WHERE id=$1 ORDER BY wg.negative, wg.value",
            str(waifu.id)
        )
        em = discord.Embed(color=0xF8C8DC, title=f"{waifu}'s gift inventory")
        em.set_thumbnail(url=waifu.display_avatar.with_static_format("png"))
        if not data:
            em.colour = discord.Color.red()
            em.description = "It's empty in here..."
            return await interaction.followup.send(embed=em)

        gifts = []
        for gift in data:
            emoji = self.bot.emoji('waifu.minus') if gift["negative"] else self.bot.emoji('waifu.plus')
            gifts.append(
                f"{gift['emoji']} {gift['name']}: {gift['quantity']:,}\n{emoji} {self.bot.emoji('currency.coin')} {gift['value']:,}")

        fields = self.create_embed_fields('\n\n'.join(gifts))
        for field in fields:
            em.add_field(name="​", value=field)
        await interaction.followup.send(embed=em)

    @gift.command(name="create", description="Create a gift")
    @app_commands.checks.has_permissions(administrator=True)
    async def waifu_gift_create(self, interaction: discord.Interaction, name: str, value: app_commands.Range[int, 1],
                                negative: Optional[bool],
                                quantity: Optional[int], emoji: str):
        await interaction.response.defer(thinking=True)
        if not is_emoji(emoji):
            return await interaction.followup.send(content="That's an invalid emoji! Try again!")
        if quantity and quantity < 1:
            return await interaction.followup.send(
                content="You can't create a gift with a quantity less than 1!")
        if value < 1:
            return await interaction.followup.send(content="The value of a gift can't be less than 1!")
        negative = negative or False
        quantity = quantity or -1
        await self.bot.pool.execute(
            "INSERT INTO waifu_gifts (name, value, negative, available, emoji) VALUES ($1, $2, $3, $4, $5)",
            name, value, negative, quantity, emoji
        )
        await interaction.followup.send(content="Done!")

    @gift.command(name="shop", description="View the gift shop")
    async def waifu_gift_shop(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        data = await self.bot.pool.fetch(
            "SELECT * FROM waifu_gifts ORDER BY negative, value"
        )
        out = []
        for gift in data:
            if gift["name"] == "Goat":
                continue
            emoji = self.bot.emoji('waifu.minus') if gift["negative"] else self.bot.emoji('waifu.plus')
            out.append(
                f"{gift['emoji']} {gift['name']}:\n{emoji} {self.bot.emoji('currency.coin')} {gift['value']:,}\n")
        em = discord.Embed(color=0xF8C8DC, title="Waifu gift shop")
        em.set_thumbnail(url=interaction.guild.icon.url)
        pages = SimplePagesInteraction(out, interaction=interaction, embed=em, per_page=10)
        await pages.start()

    @gift.command(name="buy", description="Buy a gift")
    async def waifu_gift_buy(self, interaction: discord.Interaction, gift: str,
                             quantity: Optional[app_commands.Range[int, 1]]):
        await interaction.response.defer(thinking=True)
        author = interaction.user
        quantity = quantity or 1
        em = discord.Embed(color=0xF8C8DC)
        gifts = await self.bot.pool.fetch("SELECT * FROM waifu_gifts WHERE NOT name='Goat'")
        if gift not in [x['name'] for x in gifts]:
            em.colour = discord.Color.red()
            em.description = "That is not a valid gift!"
            return await interaction.followup.send(embed=em, content=None)
        gift = next((item for item in gifts if item["name"] == gift), None)
        value = gift['value'] * quantity
        balance = await self.bot.pool.fetchval("SELECT balance FROM new_users WHERE id=$1", str(author.id))
        if balance < value:
            em.colour = discord.Color.red()
            em.description = "You cannot afford that!"
            return await interaction.followup.send(embed=em, content=None)
        async with self.bot.pool.acquire() as con:
            async with con.transaction():
                await con.execute(
                    "INSERT INTO waifu_gift_inventory (id, gift, quantity) "
                    "VALUES ($1, $2, $3) ON CONFLICT (id, gift) DO UPDATE SET quantity=waifu_gift_inventory.quantity+$3",
                    str(author.id),
                    gift['name'],
                    quantity
                )
                await con.execute(
                    "UPDATE new_users SET balance=balance-$2 WHERE id=$1", str(author.id), value
                )
        em.description = f"{author.mention} has bought {quantity:,} {gift['emoji']} {gift['name']}!"
        await interaction.followup.send(embed=em, content=None)

    @waifu_gift_buy.autocomplete("gift")
    async def waifu_gift_buy_autocomplete(self, interaction: discord.Interaction, current: str):
        gifts = await self.bot.pool.fetch("SELECT * FROM waifu_gifts WHERE NOT name='Goat' ORDER BY name")
        valid_search = [
            app_commands.Choice(name=gift['name'], value=gift['name'])
            for gift in gifts
            if not current or current.lower() in gift['name'].lower()
        ]
        return valid_search[:25]

    @gift.command(name="give", description="Give a waifu some gifts!")
    async def waifu_gift_give(self, interaction: discord.Interaction, waifu: discord.Member,
                              gift: str, quantity: Optional[app_commands.Range[int, 1]]):
        await interaction.response.defer(thinking=True)
        author = interaction.user
        quantity = quantity or 1
        em = discord.Embed(color=0xF8C8DC)
        if author.id == waifu.id:
            em.colour = discord.Color.red()
            em.description = "You can't gift yourself, go make some friends!"
            return await interaction.followup.send(embed=em, content=None)
        gift = await self.bot.pool.fetchrow(
            "SELECT * FROM waifu_gift_inventory FULL JOIN waifu_gifts wg on waifu_gift_inventory.gift = wg.name WHERE id=$1 AND gift=$2",
            str(author.id),
            gift
        )
        if not gift:
            em.colour = discord.Color.red()
            em.description = "Either that is not a valid gift or you don't have any!"
            return await interaction.followup.send(embed=em, content=None)
        if quantity > gift["quantity"]:
            em.colour = discord.Color.red()
            em.description = "You don't have that many gifts to give away!"
            return await interaction.followup.send(embed=em, content=None)
        value = gift['value'] * quantity
        waifu_user_data = await self.bot.pool.fetchrow("SELECT * FROM new_users WHERE id=$1", str(waifu.id))
        if waifu_user_data["affinity"] == str(author.id):
            value = int(value * self.affinity_worth)
        if gift['negative']:
            new_waifu_value = waifu_user_data["waifu_value"] - value
        else:
            new_waifu_value = waifu_user_data["waifu_value"] + value
        new_waifu_value = max(new_waifu_value, 0)
        async with self.bot.pool.acquire() as con:
            async with con.transaction():
                await con.execute(
                    "UPDATE waifu_gift_inventory SET quantity=quantity-$3 WHERE id=$1 AND gift=$2",
                    str(author.id),
                    gift['name'],
                    quantity
                )
                await con.execute(
                    "INSERT INTO waifu_gifts_owned (waifu, gift, quantity) "
                    "VALUES ($1, $2, $3) ON CONFLICT (waifu, gift) DO UPDATE SET quantity=waifu_gifts_owned.quantity+$3",
                    str(waifu.id),
                    gift['name'],
                    quantity
                )
                await con.execute(
                    "UPDATE new_users SET waifu_value=$2 WHERE id=$1", str(waifu.id), new_waifu_value
                )
        await self.bot.pool.execute("DELETE FROM waifu_gift_inventory WHERE id=$1 AND quantity=0", str(author.id))
        em.description = f"{author.mention} has given {quantity:,} {gift['emoji']} {gift['name']} to {waifu}!"
        await interaction.followup.send(
            content=f"{author.mention} has given {quantity:,} {gift['emoji']} {gift['name']} to {waifu.mention}!",
            allowed_mentions=discord.AllowedMentions.all())
        await self.sync_top_10()

    @waifu_gift_give.autocomplete("gift")
    async def waifu_gift_give_autocomplete(self, interaction: discord.Interaction, current: str):
        gifts = await self.bot.pool.fetch("SELECT * FROM waifu_gift_inventory WHERE id=$1 ORDER BY gift",
                                          str(interaction.user.id))
        valid_search = [
            app_commands.Choice(name=gift['gift'], value=gift['gift'])
            for gift in gifts
            if not current or current.lower() in gift['gift'].lower()
        ]
        return valid_search[:25]

    @waifu.command(name="info", description="View someones waifu profile")
    async def waifu_info(self, interaction: discord.Interaction, waifu: Optional[discord.Member]):
        await interaction.response.defer(thinking=True)
        waifu = waifu or interaction.user
        em = discord.Embed(color=0xF8C8DC)
        claim_title = await self.get_claim_title(waifu)
        em.title = f"Waifu {str(waifu)} {claim_title}"
        em.set_thumbnail(url=waifu.display_avatar.with_static_format("png"))

        user_data = await self.bot.pool.fetchrow(
            "SELECT affinity, affinity_changes, waifu_value, divorces, uc.username FROM new_users nu FULL JOIN user_cache uc on uc.id=nu.affinity WHERE nu.id=$1",
            str(waifu.id)
        )
        waifu_data = await self.bot.pool.fetchrow(
            "SELECT * FROM waifus FULL JOIN user_cache uc ON waifus.owner = uc.id WHERE waifu=$1", str(waifu.id))
        owner = waifu_data["username"] if waifu_data else "Nobody"
        affinity = user_data["username"] or "Nobody"
        affinity_title = await self.get_affinity_title(waifu)
        if not waifu_data:
            waifu_value = user_data["waifu_value"] + 1
        else:
            waifu_value = user_data["waifu_value"]
        waifu_value = max(waifu_value, 1)
        waifu_price = int(math.ceil(round(waifu_value * self.overclaim, 2)))
        em.add_field(name="Value:", value=f"{self.bot.emoji('currency.coin')} {waifu_value:,}\n"
                                          f"**Price:**\n{self.bot.emoji('currency.coin')} {waifu_price:,}")
        em.add_field(name="Claimed by:", value=str(owner))
        em.add_field(name="Likes:", value=str(affinity))

        em.add_field(name="Changes of heart:", value=f"{user_data['affinity_changes']} - {affinity_title}")
        em.add_field(name="Divorces", value=str(user_data["divorces"]))
        fans = await self.bot.pool.fetch(
            "SELECT uc.username FROM new_users nu FULL JOIN user_cache uc on nu.id=uc.id WHERE affinity=$1",
            str(waifu.id))
        fans = "\n".join([x["username"] for x in fans]) if fans else "None"
        em.add_field(name="Fans:", value=fans)

        claimed = await self.bot.pool.fetch(
            "SELECT * FROM waifus w FULL JOIN user_cache uc ON w.waifu=uc.id WHERE owner=$1", str(waifu.id))
        claimed_count = len(claimed)
        claimed = [x["username"] for x in claimed]
        if claimed_count <= 15:
            claimed = "\n".join(claimed) if claimed_count > 0 else "Nobody"
        else:
            claimed = "\n".join(claimed[:15])
            claimed += f"\n... and {claimed_count - 15} more"
        em.add_field(name=f"Waifus ({claimed_count}):", value=claimed)
        good_gifts = await self.bot.pool.fetch(
            "SELECT * FROM waifu_gifts_owned "
            "FULL JOIN waifu_gifts wg on wg.name = waifu_gifts_owned.gift WHERE waifu=$1 AND negative=false ORDER BY value",
            str(waifu.id)
        )
        bad_gifts = await self.bot.pool.fetch(
            "SELECT * FROM waifu_gifts_owned "
            "FULL JOIN waifu_gifts wg on wg.name = waifu_gifts_owned.gift WHERE waifu=$1 AND negative=true ORDER BY value",
            str(waifu.id)
        )
        good_gifts = [f"{gift['emoji']}x{gift['quantity']:,}" for gift in good_gifts]
        bad_gifts = [f"{gift['emoji']}x{gift['quantity']:,}" for gift in bad_gifts]
        gifts = ["None"] if not good_gifts and not bad_gifts else good_gifts + bad_gifts
        formatted_gifts = ""
        for i, gift in enumerate(gifts, start=1):
            formatted_gifts += gift
            formatted_gifts += "\n" if i % 3 == 0 else " " * (8 - len(gift))
        em.add_field(name="Gifts:", value=formatted_gifts)
        await interaction.followup.send(embed=em, content=None)

    @waifu.command(name="top", description="View all of the top waifus")
    async def waifu_top(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        raw_data = await self.bot.pool.fetch(
            "SELECT nu.waifu_value, uc.username, uca.username as affinity, uco.username as owner "
            "FROM new_users nu "
            "FULL JOIN user_cache uc ON nu.id = uc.id "
            "FULL JOIN user_cache uca ON nu.affinity = uca.id "
            "FULL JOIN waifus w ON nu.id = w.waifu "
            "FULL JOIN user_cache uco ON w.owner = uco.id "
            "WHERE nu.waifu_value > 0 "
            "ORDER BY nu.waifu_value DESC"
        )

        out = []
        for index, row in enumerate(raw_data, start=1):
            line = f"**#{index} - {self.bot.emoji('currency.coin')} {row['waifu_value']:,}**\n" \
                   f"**{row['username']}** claimed by **{row['owner']}**\n"
            if not row["affinity"]:
                line += f"... but {row['username']}'s heart is empty"
            elif row["affinity"] == row["owner"]:
                line += f"... and {row['username']} likes {row['owner']} too <3"
            else:
                line += f"... but {row['username']} likes {row['affinity']}!"
            line += "\n"
            out.append(line)

        em = discord.Embed(color=0xF8C8DC, title="Top Waifus")
        if not out:
            em.colour = discord.Color.red()
            em.description = "There's nobody on this page!"
            return await interaction.followup.send(embed=em, content=None)
        pages = SimplePagesInteraction(out, interaction=interaction, embed=em, per_page=10)
        await pages.start()

    async def get_claim_title(self, user: discord.Member):
        waifus = await self.bot.pool.fetch("SELECT * FROM waifus WHERE owner=$1", str(user.id))
        waifus = len(waifus)
        return next(
            (
                label
                for rank, label in self.bot.config.waifu["claim_ranks"].items()
                if rank >= waifus
            ),
            "the harem god",
        )

    async def get_affinity_title(self, user: discord.Member):
        changes = await self.bot.pool.fetchval("SELECT affinity_changes FROM new_users WHERE id=$1", str(user.id))
        return next(
            (
                label
                for rank, label in self.bot.config.waifu["affinity_ranks"].items()
                if rank >= changes
            ),
            "Harlot",
        )

async def setup(bot):
    await bot.add_cog(Waifus(bot))
