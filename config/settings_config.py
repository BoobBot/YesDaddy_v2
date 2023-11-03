from discord import Embed

monopoly_game_settings = {
  "doMention": True,
  "startCash": 1500,
  "incomeValue": 200,
  "luxuryValue": 100,
  "doAuction": True,
  "bailValue": 50,
  "maxJailRolls": 3,
  "doDoubleGo": True,
  "goValue": 200,
  "freeParkingValue": "tax",
  "hotelLimit": 12,
  "houseLimit": 32,
  "timeoutValue": 60,
  "minRaise": 1,
  "darkMode": True,
  "useThreads": True,
}

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

racers = (
    (":rabbit2:", "fast"),
    (":monkey:", "fast"),
    (":cat2:", "fast"),
    (":mouse2:", "slow"),
    (":chipmunk:", "fast"),
    (":rat:", "fast"),
    (":dove:", "fast"),
    (":bird:", "fast"),
    (":dromedary_camel:", "steady"),
    (":camel:", "steady"),
    (":dog2:", "steady"),
    (":poodle:", "steady"),
    (":racehorse:", "steady"),
    (":ox:", "abberant"),
    (":cow2:", "abberant"),
    (":elephant:", "abberant"),
    (":water_buffalo:", "abberant"),
    (":ram:", "abberant"),
    (":goat:", "abberant"),
    (":sheep:", "abberant"),
    (":leopard:", "predator"),
    (":tiger2:", "predator"),
    (":dragon:", "special"),
    (":unicorn:", "special"),
    (":turtle:", "slow"),
    (":bug:", "slow"),
    (":rooster:", "slow"),
    (":snail:", "slow"),
    (":scorpion:", "slow"),
    (":crocodile:", "slow"),
    (":pig2:", "slow"),
    (":turkey:", "slow"),
    (":duck:", "slow"),
    (":baby_chick:", "slow"),
)

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
    'Birch': {'emote': '<:birch:1146125694313697330>', 'min_value': 20, 'max_value': 40, 'rarity': 0.3},
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

claim_titles = {
    1: "The Solo Admirer",
    5: "The Companion Collector",
    10: "The Waifu Enthusiast",
    25: "The Devoted Admirer",
    50: "The Harem Builder",
    75: "The Waifu Master",
    100: "The Harem God",
    150: "The Ultimate Waifu Overlord",
    200: "The Supreme Harem Monarch",
    250: "The Grand Waifu Sovereign",
    300: "The Waifu Connoisseur Extraordinaire",
    350: "The Waifu Dominator",
    400: "The Celestial Harem Emperor",
    450: "The Infinite Waifu Overlord",
    500: "The Waifu Universe Creator",
    550: "The Legendary Harem Deity",
    600: "The Omniscient Waifu Almighty",
    1000: "The Waifu Divinity",
}

divorce_titles = {
    1: "The Heartbroken",
    5: "The Divorce Novice",
    10: "The Relationship Tester",
    25: "The Unlucky Lover",
    50: "The Breakup Survivor",
    75: "The Divorce Expert",
    100: "The Resilient Heart",
    150: "The Eternal Optimist",
    200: "The Battle-Hardened Heart",
    300: "The Divorce Veteran",
}

affinity_titles = {
    1: "The Affinity Explorer",
    5: "The Ever-Shifting Heart",
    10: "The Change Enthusiast",
    25: "The Adaptable Soul",
    50: "The Affinity Chameleon",
    75: "The Heart in Flux",
    100: "The Eternal Wanderer",
    150: "The Ever-Evolving Spirit",
    300: "The Boundless Heart",
}

TILENAME = [
    'Go', 'Mediterranean Avenue',
    'Community Chest', 'Baltic Avenue',
    'Income Tax', 'Reading Railroad',
    'Oriental Avenue', 'Chance',
    'Vermont Avenue', 'Connecticut Avenue',
    'Jail', 'St. Charles Place',
    'Electric Company', 'States Avenue',
    'Virginia Avenue', 'Pennsylvania Railroad',
    'St. James Place', 'Community Chest',
    'Tennessee Avenue', 'New York Avenue',
    'Free Parking', 'Kentucky Avenue',
    'Chance', 'Indiana Avenue',
    'Illinois Avenue', 'B&O Railroad',
    'Atlantic Avenue', 'Ventnor Avenue',
    'Water Works', 'Marvin Gardens',
    'Go To Jail', 'Pacific Avenue',
    'North Carolina Avenue', 'Community Chest',
    'Pennsylvania Avenue', 'Short Line',
    'Chance', 'Park Place',
    'Luxury Tax', 'Boardwalk'
]
PRICEBUY = [
    -1, 60, -1, 60, -1,
    200, 100, -1, 100, 120,
    -1, 140, 150, 140, 160,
    200, 180, -1, 180, 200,
    -1, 220, -1, 220, 240,
    200, 260, 260, 150, 280,
    -1, 300, 300, -1, 320,
    200, -1, 350, -1, 400
]
RENTPRICE = [
    -1, -1, -1, -1, -1, -1,
    2, 10, 30, 90, 160, 250,
    -1, -1, -1, -1, -1, -1,
    4, 20, 60, 180, 360, 450,
    -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1,
    6, 30, 90, 270, 400, 550,
    -1, -1, -1, -1, -1, -1,
    6, 30, 90, 270, 400, 550,
    8, 40, 100, 300, 450, 600,
    -1, -1, -1, -1, -1, -1,
    10, 50, 150, 450, 625, 750,
    -1, -1, -1, -1, -1, -1,
    10, 50, 150, 450, 625, 750,
    12, 60, 180, 500, 700, 900,
    -1, -1, -1, -1, -1, -1,
    14, 70, 200, 550, 750, 950,
    -1, -1, -1, -1, -1, -1,
    14, 70, 200, 550, 750, 950,
    16, 80, 220, 600, 800, 1000,
    -1, -1, -1, -1, -1, -1,
    18, 90, 250, 700, 875, 1050,
    -1, -1, -1, -1, -1, -1,
    10, 90, 250, 700, 875, 1050,
    20, 100, 300, 750, 925, 1100,
    -1, -1, -1, -1, -1, -1,
    22, 110, 330, 800, 975, 1150,
    22, 110, 330, 800, 975, 1150,
    -1, -1, -1, -1, -1, -1,
    24, 120, 360, 850, 1025, 1200,
    -1, -1, -1, -1, -1, -1,
    26, 130, 390, 900, 1100, 1275,
    26, 130, 390, 900, 1100, 1275,
    -1, -1, -1, -1, -1, -1,
    28, 150, 450, 1000, 1200, 1400,
    -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1,
    35, 175, 500, 1100, 1300, 1500,
    -1, -1, -1, -1, -1, -1,
    50, 200, 600, 1400, 1700, 2000
]
RRPRICE = [0, 25, 50, 100, 200]
CCNAME = [
    'Advance to Go (Collect $200)',
    'Bank error in your favor\nCollect $200',
    'Doctor\'s fee\nPay $50',
    'From sale of stock you get $50',
    'Get Out of Jail Free',
    'Go to Jail\nGo directly to jail\nDo not pass Go\nDo not collect $200',
    'Grand Opera Night\nCollect $50 from every player for opening night seats',
    'Holiday Fund matures\nReceive $100',
    'Income tax refund\nCollect $20',
    'It is your birthday\nCollect $10',
    'Life insurance matures\nCollect $100',
    'Pay hospital fees of $100',
    'Pay school fees of $150',
    'Receive $25 consultancy fee',
    'You are assessed for street repairs\n$40 per house\n$115 per hotel',
    'You have won second prize in a beauty contest\nCollect $10',
    'You inherit $100'
]
CHANCENAME = [
    'Advance to Go (Collect $200)',
    'Advance to Illinois Ave\nIf you pass Go, collect $200.',
    'Advance to St. Charles Place\nIf you pass Go, collect $200',
    (
        'Advance token to nearest Utility. If unowned, you may buy it from the Bank. '
        'If owned, throw dice and pay owner a total ten times the amount thrown.'
    ), (
        'Advance token to the nearest Railroad and pay owner twice the rental to which '
        'he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.'
    ),
    'Bank pays you dividend of $50',
    'Get Out of Jail Free',
    'Go Back 3 Spaces',
    'Go to Jail\nGo directly to Jail\nDo not pass Go\nDo not collect $200',
    'Make general repairs on all your property\nFor each house pay $25\nFor each hotel $100',
    'Pay poor tax of $15',
    'Take a trip to Reading Railroad\nIf you pass Go, collect $200',
    'Take a walk on the Boardwalk\nAdvance token to Boardwalk',
    'You have been elected Chairman of the Board\nPay each player $50',
    'Your building and loan matures\nCollect $150',
    'You have won a crossword competition\nCollect $100'
]
MORTGAGEPRICE = [
    -1, 30, -1, 30, -1,
    100, 50, -1, 50, 60,
    -1, 70, 75, 70, 80,
    100, 90, -1, 90, 100,
    -1, 110, -1, 110, 120,
    100, 130, 130, 75, 140,
    -1, 150, 150, -1, 160,
    100, -1, 175, -1, 200
]
TENMORTGAGEPRICE = [
    -1, 33, -1, 33, -1,
    110, 55, -1, 55, 66,
    -1, 77, 83, 77, 88,
    110, 99, -1, 99, 110,
    -1, 121, -1, 121, 132,
    110, 143, 143, 83, 154,
    -1, 165, 165, -1, 176,
    110, -1, 188, -1, 220
]
HOUSEPRICE = [
    -1, 50, -1, 50, -1,
    -1, 50, -1, 50, 50,
    -1, 100, -1, 100, 100,
    -1, 100, -1, 100, 100,
    -1, 150, -1, 150, 150,
    -1, 150, 150, -1, 150,
    -1, 200, 200, -1, 200,
    -1, -1, 200, -1, 200
]
PROPGROUPS = {
    'Brown': [1, 3], 'Light Blue': [6, 8, 9],
    'Pink': [11, 13, 14], 'Orange': [16, 18, 19],
    'Red': [21, 23, 24], 'Yellow': [26, 27, 29],
    'Green': [31, 32, 34], 'Dark Blue': [37, 39]
}
PROPCOLORS = {
    1: 'Brown', 3: 'Brown',
    6: 'Light Blue', 8: 'Light Blue', 9: 'Light Blue',
    11: 'Pink', 13: 'Pink', 14: 'Pink',
    16: 'Orange', 18: 'Orange', 19: 'Orange',
    21: 'Red', 23: 'Red', 24: 'Red',
    26: 'Yellow', 27: 'Yellow', 29: 'Yellow',
    31: 'Green', 32: 'Green', 34: 'Green',
    37: 'Dark Blue', 39: 'Dark Blue',
    5: 'Railroad', 15: 'Railroad', 25: 'Railroad', 35: 'Railroad',
    12: 'Utility', 28: 'Utility'
}


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
        emoji = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f""

        if title == "Leaderboard - Levels: Page":
            value = f"{emoji} {member.display_name}: {user.level}"
        elif title == "Leaderboard - Balance: Page":
            value = f"{emoji} {member.display_name}: {user.balance}"
        elif title == "Leaderboard - Bank Balance: Page":
            value = f"{emoji} {member.display_name}: {user.bank_balance}"
        else:
            value = f"{emoji} {member.display_name}: {user.balance + user.bank_balance}"

        value = value.replace(f"#{index} ", "")

        embed.add_field(name=f"", value=value, inline=False)

    return embed
