from discord import Embed

emoji_payouts = {
    "⚽": 5,
    "🎱": 10,
    "🎰": 20,
    "🍀": 50,
    "🎮": 100,
    "<a:coins:1146124100369137666>": 200  # Jackpot payout is handled separately
}

jackpot_emoji = "<a:coins:1146124100369137666>"
jackpot_payout = 500
bonus_multiplier = 2

fish_info = {
    'Salmon': '<:salmon:1146118005273677904>',
    'Trout': '<:trout:1146116187600715946>',
    'Bass': '<:bass:1146117268690960436>',
    'Tuna': '<:tuna:1146115466503409696>',
    'Mackerel': '<:mackerel:1146118655889912030>',
    'Cod': '<:cod:1146119455215194132>'
}

mine_resource_info = {
    'Coal': {'emote': '<:coal:1146120671949226045>', 'min_value': 5, 'max_value': 15, 'rarity': 0.6},
    'Iron': {'emote': '<:Iron:1146120977114222633>', 'min_value': 10, 'max_value': 20, 'rarity': 0.5},
    'Gold': {'emote': '<:gold:1146121325912522785>', 'min_value': 15, 'max_value': 25, 'rarity': 0.4},
    'Diamond': {'emote': '<:diamond:1146121876381384744>', 'min_value': 50, 'max_value': 500, 'rarity': 0.2},
    'Emerald': {'emote': '<:Emerald:1146121911986819073>', 'min_value': 20, 'max_value': 250, 'rarity': 0.3}
}

chop_resource_info = {
    'Wood': {'emote': '<:wood:1146123952662515832>', 'min_value': 5, 'max_value': 15, 'rarity': 0.7},
    'Oak': {'emote': '<:oak:1146125043550650399>', 'min_value': 10, 'max_value': 20, 'rarity': 0.6},
    'Maple': {'emote': '<:maple:1146126198901047366>', 'min_value': 15, 'max_value': 25, 'rarity': 0.4},
    'Birch': {'emote': '<:birch:1146125694313697330>', 'min_value': 20, 'max_value': 30, 'rarity': 0.3},
}

monsters = [
    {"emoji": "The Dragon <a:dragon:1146865445547278457>",
     "value": 100, "success_rate": 0.7, "rarity": 0.4},  # Legendary
    {"emoji": "a Kitsune <:kitsune:1146865719502442667>",
     "value": 50, "success_rate": 0.9, "rarity": 0.5},  # Rare
    {"emoji": "The Ancient Spirit <:spirit:1146869866599555082>",
     "value": 80, "success_rate": 0.6, "rarity": 0.3},  # Epic
    {"emoji": "a Rogue Bandit <:bandit:1146870790344683530>",
     "value": 20, "success_rate": 0.95, "rarity": 0.9},  # Common
    {"emoji": "a Pixie <:pixie:1146872679866044467>", "value": 30,
     "success_rate": 0.85, "rarity": 0.7},  # Uncommon
    {"emoji": "The Shapeshifter <:shifter:1146874237387284580>",
     "value": 70, "success_rate": 0.75, "rarity": 0.5},  # Rare
    {"emoji": "a Rock Golem <:golem:1146874710186008676>",
     "value": 90, "success_rate": 0.5, "rarity": 0.7},  # Uncommon
    {"emoji": "The Haunted Spirit <:ghost:1146867993461133403>",
     "value": 60, "success_rate": 0.8, "rarity": 0.9},  # Common
    {"emoji": "an Interdimensional Entity <:entity:1146875640675573810>",
     "value": 120, "success_rate": 0.4, "rarity": 0.2},  # Mythical
    {"emoji": "a Band of Bandits <:bandit_group:1146870972301979658>",
     "value": 40, "success_rate": 0.9, "rarity": 0.9}  # Common
]


def calculate_payout(result):
    total_payout = 0
    is_jackpot = False
    is_bonus = False
    if len(set(result)) == 1:  # All three slots are the same
        is_bonus = True
        emoji = result[0]
        if emoji in emoji_payouts:
            total_payout = emoji_payouts[emoji] * bonus_multiplier
    else:
        for emoji in result:
            if emoji in emoji_payouts:
                total_payout += emoji_payouts[emoji]
            if emoji == jackpot_emoji:
                is_jackpot = True
    if is_jackpot:
        return jackpot_payout, True, False
    return total_payout, False, is_bonus


def create_leaderboard_pages(sorted_users, title):
    pages = []
    chunk_size = 10

    for page_number, i in enumerate(range(0, len(sorted_users), chunk_size), start=1):
        chunk = sorted_users[i:i + chunk_size]
        embed = create_leaderboard_embed(title, chunk, page_number)
        pages.append(embed)

    return pages


def create_leaderboard_embed(title, entries, page_number):
    embed = Embed(title=f"{title} {page_number}")

    for index, (user, member) in enumerate(entries, start=page_number * 10 - 9):
        emoji = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f"{index}"

        if title == "Leaderboard - Levels: Page":
            value = f"{emoji} {member.display_name}: {user.level}"
        elif title == "Leaderboard - Balance: Page":
            value = f"{emoji} {member.display_name}: {user.balance}"
        elif title == "Leaderboard - Bank Balance: Page":
            value = f"{emoji} {member.display_name}: {user.bank_balance}"
        else:
            value = f"{emoji} {member.display_name}: {user.balance + user.bank_balance}"

        value = value.replace(f"#{index} ", "")

        embed.add_field(name=f"{emoji}", value=value, inline=False)

    return embed
