import random


def get_all_items():
    return axes + pickaxes + fishing_rods


axes = [
    {
        "name": "Beginners Hatchet",
        "type": "Axe",
        "tier": 1,
        "description": "A basic woodcutter's friend. Effective on softwoods.",
        "multiplier": 2,
        "durability": 100,
        "required_level": 1,
        "emote": "<:axe1:1169395748870307921>",
        "equippable": True,
        "price": 10000,
        "rarity": "Common",
        "quantity": 1
    },
    {
        "name": "Oakbane Axe",
        "type": "Axe",
        "tier": 2,
        "description": "Crafted to tackle harder woods with ease.",
        "multiplier": 2.2,
        "durability": 100,
        "required_level": 10,
        "emote": "<:axe2:1169389638880866444>",
        "equippable": True,
        "price": 100000,
        "rarity": "Uncommon",
        "quantity": 1
    },
    {
        "name": "Ironwood Chopper",
        "type": "Axe",
        "tier": 3,
        "description": "A sturdy axe that makes chopping a breeze.",
        "multiplier": 2.4,
        "durability": 100,
        "required_level": 20,
        "emote": "<:axe3:1169388837563269170>",
        "equippable": True,
        "price": 150000,
        "rarity": "Rare",
        "quantity": 1
    }
]

pickaxes = [
    {
        "name": "Beginners Pickaxe",
        "type": "Pickaxe",
        "tier": 1,
        "description": "A basic miner's friend. Effective on soft rocks.",
        "multiplier": 2,
        "durability": 100,
        "required_level": 1,
        "emote": "<:pick1:1169395716574167210>",
        "equippable": True,
        "price": 10000,
        "rarity": "Common",
        "quantity": 1
    },
    {
        "name": "Stonecrusher Pickaxe",
        "type": "Pickaxe",
        "tier": 2,
        "description": "Crafted to tackle harder rocks with ease.",
        "multiplier": 2.2,
        "durability": 100,
        "required_level": 10,
        "emote": "<:pick2:1169390159842791525>",
        "equippable": True,
        "price": 100000,
        "rarity": "Uncommon",
        "quantity": 1
    },
    {
        "name": "Ironbreaker Pickaxe",
        "type": "Pickaxe",
        "tier": 3,
        "description": "A sturdy pickaxe that makes mining a breeze.",
        "multiplier": 2.4,
        "durability": 100,
        "required_level": 20,
        "emote": "<:pick3:1169389539228385350>",
        "equippable": True,
        "price": 150000,
        "rarity": "Rare",
        "quantity": 1
    }
]

fishing_rods = [
    {
        "name": "Guppy's Grip",
        "type": "Fishing Rod",
        "tier": 1,
        "description": "A beginner's rod for the casual fisher.",
        "multiplier": 2,
        "durability": 100,
        "required_level": 1,
        "emote": "<:fish1:1169401503577022474>",
        "equippable": True,
        "price": 10000,
        "rarity": "Common",
        "quantity": 1
    },
    {
        "name": "Tide Tamer",
        "type": "Fishing Rod",
        "tier": 2,
        "description": "Ideal for the aspiring angler, ready to face the challenges of the deep.",
        "multiplier": 2.2,
        "durability": 100,
        "required_level": 10,
        "emote": "<:fish2:1169389609797562501>",
        "equippable": True,
        "price": 100000,
        "rarity": "Uncommon",
        "quantity": 1
    },
    {
        "name": "Reel Ruler",
        "type": "Fishing Rod",
        "tier": 3,
        "description": "A rod that balances strength and flexibility for a great fishing experience.",
        "multiplier": 2.4,
        "durability": 100,
        "required_level": 20,
        "emote": "<:fish3:1169395693039911063>",
        "equippable": True,
        "price": 150000,
        "rarity": "Rare",
        "quantity": 1
    }
]

loot = [
    {
        "name": "Lumberlord's Cleaver",
        "type": "Axe",
        "tier": 4,
        "description": "For the serious woodcutter, efficiency and sharpness rolled into one.",
        "multiplier": 2.6,
        "durability": 100,
        "required_level": 30,
        "emote": "<:axe4:1169388835189305474>",
        "equippable": True,
        "price": 200000,
        "rarity": "Epic",
        "quantity": 1,
        "win_probability": 0.8
    },
    {
        "name": "Titanium Timberfeller",
        "type": "Axe",
        "tier": 5,
        "description": "Lightweight and razor-sharp, a true companion of the professional lumberjack.",
        "multiplier": 2.8,
        "durability": 100,
        "required_level": 40,
        "emote": "<:axe5:1169388830281969714>",
        "equippable": True,
        "price": 1000000,
        "rarity": "Legendary",
        "quantity": 1,
        "win_probability": 0.7
    },
    {
        "name": "Mythical Lumberblade",
        "type": "Axe",
        "tier": 6,
        "description": "Legends say trees fall at its mere presence.",
        "multiplier": 5,
        "durability": 100,
        "required_level": 55,
        "emote": "<:axe6:1169388832836300940>",
        "equippable": True,
        "price": 100000000,
        "rarity": "Mythical",
        "quantity": 1,
        "win_probability": 0.01
    },
    {
        "name": "Gemfinder's Pickaxe",
        "type": "Pickaxe",
        "tier": 4,
        "description": "For the serious miner, efficiency and sharpness rolled into one.",
        "multiplier": 2.6,
        "durability": 100,
        "required_level": 30,
        "emote": "<:pick4:1169389553593884822>",
        "equippable": True,
        "price": 200000,
        "rarity": "Epic",
        "quantity": 1,
        "win_probability": 0.8
    },
    {
        "name": "Titanium Terra-tapper",
        "type": "Pickaxe",
        "tier": 5,
        "description": "Lightweight and razor-sharp, a true companion of the professional miner.",
        "multiplier": 2.8,
        "durability": 100,
        "required_level": 40,
        "emote": "<:pick5:1169390617793663047>",
        "equippable": True,
        "price": 1000000,
        "rarity": "Legendary",
        "quantity": 1,
        "win_probability": 0.7
    },
    {
        "name": "Mythical Ore Oracle",
        "type": "Pickaxe",
        "tier": 6,
        "description": "Legends say mountains quake at its mere presence.",
        "multiplier": 5,
        "durability": 100,
        "required_level": 55,
        "emote": "<:pick6:1169390653982134313>",
        "equippable": True,
        "price": 100000000,
        "rarity": "Mythical",
        "quantity": 1,
        "win_probability": 0.01
    },
    {
        "name": "Aqua Adept Rod",
        "type": "Fishing Rod",
        "tier": 4,
        "description": "Expertly crafted for the seasoned angler, ready to reel in the big ones.",
        "multiplier": 2.6,
        "durability": 100,
        "required_level": 30,
        "emote": "<:fish4:1169401381191421982>",
        "equippable": True,
        "price": 200000,
        "rarity": "Epic",
        "quantity": 1,
        "win_probability": 0.8
    },
    {
        "name": "Titanium Tidalstaff",
        "type": "Fishing Rod",
        "tier": 5,
        "description": "A masterpiece in fishing gear, almost guaranteeing a good catch.",
        "multiplier": 2.8,
        "durability": 100,
        "required_level": 40,
        "emote": "<:fish5:1169401521763532911>",
        "equippable": True,
        "price": 1000000,
        "rarity": "Legendary",
        "quantity": 1,
        "win_probability": 0.7
    },
    {
        "name": "Mythical Marlinmancer",
        "type": "Fishing Rod",
        "tier": 6,
        "description": "Rumored to summon the lords of the ocean with a flick of the wrist.",
        "multiplier": 5,
        "durability": 100,
        "required_level": 55,
        "emote": "<:fish6:1169401476087562310>",
        "equippable": True,
        "price": 100000000,
        "rarity": "Mythical",
        "quantity": 1,
        "win_probability": 0.01
    }

]


def weighted_random_choice(items=None):
    """
    This function picks an item from 'items', each item having a chance to be
    picked proportional to its 'win_probability' field.
    """
    if items is None:
        items = loot
    total_probability = sum(item["win_probability"] for item in items)
    random_choice = random.uniform(0, total_probability)
    cumulative_probability = 0
    for item in items:
        cumulative_probability += item["win_probability"]
        if random_choice <= cumulative_probability:
            return item


def maybe_loot(items=None, call_probability=None):
    """
    This function calls 'weighted_random_choice' with a probability of 'call_probability'.
    If 'weighted_random_choice' is not called, 'None' is returned.
    """

    # A random number between 0 and 1
    if items is None:
        items = loot
    if call_probability is None:
        call_probability = 0.01

    random_choice = random.random()

    if random_choice < call_probability:
        return weighted_random_choice(items)
    else:
        return None

# This is the code I used to test the above functions.
# total_iterations = 100000
# output {'None': 90120, 'Legendary': 4649, 'Epic': 5173, 'Mythical': 58}
# odds {'None': 0.9012, 'Legendary': 0.04649, 'Epic': 0.05173, 'Mythical': 0.00058}

# counts = {}
# total_iterations = 100000
# for x in range(total_iterations):
#     i = maybe_won()
#     if i is not None:
#         counts[i.get("rarity")] = counts.get(i.get("rarity"), 0) + 1
#     else:
#         counts["None"] = counts.get("None", 0) + 1
# print(counts)
# odds = {key: (value / total_iterations) for key, value in counts.items()}
# print(odds)
