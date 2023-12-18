
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
        "emote": "<:axe1:1169395748870307921>",
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
        "emote": "<:axe1:1169395748870307921>",
        "equippable": True,
        "price": 150000,
        "rarity": "Rare",
        "quantity": 1
    },
    {
        "name": "Lumberlord's Cleaver",
        "type": "Axe",
        "tier": 4,
        "description": "For the serious woodcutter, efficiency and sharpness rolled into one.",
        "multiplier": 2.6,
        "durability": 100,
        "required_level": 30,
        "emote": "<:axe1:1169395748870307921>",
        "equippable": True,
        "price": 200000,
        "rarity": "Epic",
        "quantity": 1
    },
    {
        "name": "Titanium Timberfeller",
        "type": "Axe",
        "tier": 5,
        "description": "Lightweight and razor-sharp, a true companion of the professional lumberjack.",
        "multiplier": 2.8,
        "durability": 100,
        "required_level": 40,
        "emote": "<:axe1:1169395748870307921>",
        "equippable": True,
        "price": 1000000,
        "rarity": "Legendary",
        "quantity": 1
    },
    {
        "name": "Mythical Lumberblade",
        "type": "Axe",
        "tier": 6,
        "description": "Legends say trees fall at its mere presence.",
        "multiplier": 5,
        "durability": 100,
        "required_level": 55,
        "emote": "<:axe1:1169395748870307921>",
        "equippable": True,
        "price": 100000000,
        "rarity": "Mythical",
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
        "emote": "<:pick1:1169395748744471041>",
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
        "emote": "<:pick1:1169395748744471041>",
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
        "emote": "<:pick1:1169395748744471041>",
        "equippable": True,
        "price": 150000,
        "rarity": "Rare",
        "quantity": 1
    },
    {
        "name": "Gemfinder's Pickaxe",
        "type": "Pickaxe",
        "tier": 4,
        "description": "For the serious miner, efficiency and sharpness rolled into one.",
        "multiplier": 2.6,
        "durability": 100,
        "required_level": 30,
        "emote": "<:pick1:1169395748744471041>",
        "equippable": True,
        "price": 200000,
        "rarity": "Epic",
        "quantity": 1
    },
    {
        "name": "Titanium Terra-tapper",
        "type": "Pickaxe",
        "tier": 5,
        "description": "Lightweight and razor-sharp, a true companion of the professional miner.",
        "multiplier": 2.8,
        "durability": 100,
        "required_level": 40,
        "emote": "<:pick1:1169395748744471041>",
        "equippable": True,
        "price": 1000000,
        "rarity": "Legendary",
        "quantity": 1
    },
    {
        "name": "Mythical Ore Oracle",
        "type": "Pickaxe",
        "tier": 6,
        "description": "Legends say mountains quake at its mere presence.",
        "multiplier": 5,
        "durability": 100,
        "required_level": 55,
        "emote": "<:pick1:1169395748744471041>",
        "equippable": True,
        "price": 100000000,
        "rarity": "Mythical",
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
        "emote": "<:fishingrod1:1169395748648895489>",
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
        "emote": "<:fishingrod1:1169395748648895489>",
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
        "emote": "<:fishingrod1:1169395748648895489>",
        "equippable": True,
        "price": 150000,
        "rarity": "Rare",
        "quantity": 1
    },
    {
        "name": "Aqua Adept Rod",
        "type": "Fishing Rod",
        "tier": 4,
        "description": "Expertly crafted for the seasoned angler, ready to reel in the big ones.",
        "multiplier": 2.6,
        "durability": 100,
        "required_level": 30,
        "emote": "<:fishingrod1:1169395748648895489>",
        "equippable": True,
        "price": 200000,
        "rarity": "Epic",
        "quantity": 1
    },
    {
        "name": "Titanium Tidalstaff",
        "type": "Fishing Rod",
        "tier": 5,
        "description": "A masterpiece in fishing gear, almost guaranteeing a good catch.",
        "multiplier": 2.8,
        "durability": 100,
        "required_level": 40,
        "emote": "<:fishingrod1:1169395748648895489>",
        "equippable": True,
        "price": 1000000,
        "rarity": "Legendary",
        "quantity": 1
    },
    {
        "name": "Mythical Marlinmancer",
        "type": "Fishing Rod",
        "tier": 6,
        "description": "Rumored to summon the lords of the ocean with a flick of the wrist.",
        "multiplier": 5,
        "durability": 100,
        "required_level": 55,
        "emote": "<:fishingrod1:1169395748648895489>",
        "equippable": True,
        "price": 100000000,
        "rarity": "Mythical",
        "quantity": 1
    }

]

job_descriptions = [
    "{0} is a professional cat juggler.",
    "{0} specializes in finding lost socks for a living.",
    "Meet {0}, the world's fastest typist... with their toes.",
    "{0} is a full-time bubble wrap popper and proud of it.",
    "When others go fishing, {0} fishes for compliments.",
    "Need a cloud whisperer? Look no further than {0}.",
    "{0} is a professional ice cream taster, certified in brain freeze prevention.",
    "Introducing {0}, the official snuggler of teddy bears.",
    "{0} moonlights as a professional unicorn groomer.",
    "As a certified professional nap-taker, {0} knows the best spots to snooze.",
    "Meet {0}, the world's greatest thumb wrestler.",
    "{0} turns pizza tossing into a mesmerizing art form.",
    "{0} can juggle flaming marshmallows blindfolded. It's a gift.",
    "Need someone to laugh at your jokes? {0} offers premium laughter services.",
    "{0} is a master in the delicate art of balloon animal psychology.",
    "Introducing {0}, a professional finger painter who's all grown up.",
    "When life gives lemons, {0} becomes a lemonade stand tycoon.",
    "{0} is a pro at avoiding cracks in the sidewalk, no really.",
    "{0} has achieved the world record for the most high-fives given in an hour.",
    "Meet {0}, the official tickler of funny bones worldwide.",
    "{0} is a professional bubble bath tester and takes their job seriously.",
    "Introducing {0}, a certified pirate treasure map interpreter.",
    "{0} is the reigning champion of extreme pillow fighting.",
    "When not busy, {0} practices interpretive dance for squirrels.",
    "{0} is a part-time cloud namer, adding personality to the sky.",
    "{0} moonlights as a professional bubble gum bubble blower.",
    "Introducing {0}, a master of assembling IKEA furniture... blindfolded.",
    "{0} offers premium services as a professional snowflake counter.",
    "Meet {0}, the world's fastest hopscotch skipper.",
    "{0} specializes in creating the most elaborate paper airplanes.",
    "When life gives them oranges, {0} makes orange juice. Clearly.",
    "{0} is a certified rainbow catcher, brightening days everywhere.",
    "Introducing {0}, the official jellybean sorter for the Candy Kingdom.",
    "{0} has perfected the art of parallel universe travel. Almost.",
    "Meet {0}, the world's greatest thumb war champion.",
    "{0} is a professional bubble wrap walker, making strides one pop at a time.",
    "{0} moonlights as a professional squirrel translator.",
    "Introducing {0}, a certified expert in untangling slinkies.",
    "{0} offers premium services as a professional hopscotch course designer.",
    "When not busy, {0} practices synchronized swimming with rubber duckies.",
    "{0} is a master at counting grains of sand on the beach. It's a talent.",
    "{0} is a professional ice cream cone juggler, cones and all.",
    "Meet {0}, the world's fastest snail racer.",
    "{0} specializes in alphabetizing soup cans with precision.",
    "When life gives them rubber ducks, {0} hosts epic bathtub regattas.",
    "Introducing {0}, a professional pillow fluffer for the most discerning sleepers.",
    "{0} has perfected the art of mind reading... well, almost.",
    "{0} is a certified expert in predicting the flavor of jellybeans by smell alone.",
    "Meet {0}, the official cloud shape cataloger.",
    "{0} moonlights as a professional hula hooper extraordinaire.",
    "Introducing {0}, a master at navigating through corn mazes with eyes closed.",
    "{0} offers premium services as a professional tic-tac-toe strategy consultant.",
    "When not busy, {0} practices extreme hula hooping for the Olympics.",
    "{0} is a certified bubble bath mixologist, creating bubbly wonders.",
    "{0} is a professional moonwalk tester and a smooth criminal at it.",
    "Meet {0}, the world's greatest marshmallow roaster, bonfires beware.",
    "{0} specializes in translating baby babble into eloquent speeches.",
    "When life gives them rubber bands, {0} becomes a rubber band guitar virtuoso.",
    "Introducing {0}, a professional bubble wrap popper with a black belt.",
    "{0} has perfected the art of invisibility... well, almost.",
    "{0} is a certified expert in reverse engineering pancakes.",
    "Meet {0}, the official tickle monster in residence.",
    "{0} moonlights as a professional kazoo symphony conductor.",
    "Introducing {0}, a master at building sandcastles in a hurricane.",
    "{0} offers premium services as a professional finger puppet therapist.",
    "When not busy, {0} practices synchronized skydiving with rubber chickens.",
    "{0} is a connoisseur of the finest invisible art, truly visionary.",
    "{0} is a professional paper airplane pilot, soaring to new heights.",
    "Meet {0}, the world's fastest turtle racer.",
    "{0} specializes in designing custom sock puppet wardrobes.",
    "When life gives them pineapples, {0} hosts extravagant tropical fruit fashion shows.",
    "Introducing {0}, a professional rubber duck wrangler for the world's toughest rodeos.",
    "{0} has perfected the art of speaking fluent penguin.",
    "{0} is a certified expert in deciphering the secret language of garden gnomes.",
    "Meet {0}, the official dragon tamer in training.",
    "{0} moonlights as a professional interpretive dance interpreter.",
    "Introducing {0}, a master of crafting paperclip sculptures of famous landmarks.",
    "{0} offers premium services as a professional kazoo karaoke coach.",
    "When not busy, {0} practices synchronized pogo sticking with kangaroos.",
    "{0} is a guru of potato chip fortune telling, a truly savory skill.",
    "{0} is a professional rubber band acrobat, stretching the limits of physics.",
    "Meet {0}, the world's fastest unicycle downhill racer.",
    "{0} specializes in creating avant-garde hairstyles for garden gnomes.",
    "When life gives them rubber chickens, {0} hosts sold-out stand-up comedy shows.",
    "Introducing {0}, a professional pancake flipper with Olympic aspirations.",
    "{0} has perfected the art of translating Morse code through interpretive dance.",
    "{0} is a certified expert in composing sonnets for squirrels.",
    "Meet {0}, the official bubble wrap ballet choreographer.",
    "{0} moonlights as a professional kite flyer in hurricane-prone areas.",
    "Introducing {0}, a master at knitting sweaters for cacti.",
    "{0} offers premium services as a professional interpretive cloud painter.",
    "{0} is a professional llama whisperer, communicating through stylish neckwear.",
    "Introducing {0}, a master at parallel parking monster trucks.",
    "{0} moonlights as a professional penguin personal trainer.",
    "{0} specializes in decoding the cryptic language of garden gnomes.",
    "{0} is a certified expert in teaching synchronized swimming to goldfish.",
    "Meet {0}, the official toe wrestler of the underground toe wrestling circuit.",
    "{0} offers premium services as a professional bubble wrap fashion designer.",
    "When not busy, {0} practices extreme origami with 2-inch square paper.",
    "{0} is a professional squirrel obstacle course designer, complete with tiny hurdles.",
    "Introducing {0}, a master at yodeling while underwater.",
    "{0} has perfected the art of solving Rubik's cubes with their nose.",
    "{0} is a certified expert in predicting the weather based on cloud formations in coffee.",
    "Meet {0}, the official under-the-bed monster negotiator.",
    "{0} moonlights as a professional pogo stick tester for aspiring kangaroos.",
    "{0} specializes in crafting intricate sand mandalas for crabs.",
    "{0} is a certified expert in interpretive dance for shy garden gnomes.",
    "{0} is a professional puddle jumper, leaping over rainwater with grace.",
    "Introducing {0}, a master at balancing tea cups on their nose.",
    "{0} offers premium services as a professional squirrel fashion consultant.",
    "When not busy, {0} practices extreme juggling with watermelons.",
    "{0} is a professional banana peel slip-and-fall stunt double.",
    "Meet {0}, the official napkin folding instructor for high-class squirrels.",
    "{0} moonlights as a professional hula hooper on unicycles.",
    "{0} specializes in composing epic ballads for garden gnomes.",
    "{0} is a certified expert in teaching breakdancing to flamingos.",
    "Introducing {0}, a master at interpretive dancing with their shadow.",
    "{0} offers premium services as a professional bubble gum sculpture artist.",
    "{0} is a professional snowflake catcher during summer heatwaves.",
    "When not busy, {0} practices synchronized swimming with rubber sharks.",
    "{0} is a certified expert in underwater basket weaving with jellyfish tentacles.",
    "Meet {0}, the official tickle tester for baby kittens.",
    "{0} moonlights as a professional moon bounce tester on trampolines.",
    "{0} specializes in coaching competitive pillow fight teams.",
    "{0} is a certified expert in teaching penguins to fly... in their dreams.",
    "{0} is a professional bubble wrap maze designer, challenging adventurers everywhere.",
    "Introducing {0}, a master at solving riddles in whale songs.",
    "{0} offers premium services as a professional squirrel language translator.",
    "When not busy, {0} practices tightrope walking with dental floss.",
    "{0} is a professional shadow puppeteer for sunsets.",
    "Meet {0}, the official fog sculptor, shaping mist into intricate designs.",
    "{0} moonlights as a professional unicycle juggler at stoplights.",
    "{0} specializes in crafting gourmet meals for action figures.",
    "{0} is a certified expert in teaching synchronized swimming to rubber ducks.",
    "{0} is a professional bubble wrap enthusiast, popping joy into the world.",
    "Introducing {0}, a master at underwater knitting with mermaids.",
    "{0} offers premium services as a professional squirrel life coach.",
    "When not busy, {0} practices synchronized ballet with flamingos.",
    "{0} is a certified expert in extreme teacup stacking.",
    "{0} is a professional fortune teller for garden gnomes.",
    "Meet {0}, the official squirrel wardrobe stylist, keeping tails fabulous.",
    "{0} moonlights as a professional rubber chicken ventriloquist.",
    "{0} specializes in composing operas for opera-singing whales.",
    "{0} is a certified expert in teaching squirrels to water ski.",
    "{0} is a professional moon rock polisher, making lunar bling shine.",
    "Introducing {0}, a master at interpretive dance with traffic signals.",
    "{0} offers premium services as a professional cloud whisperer.",
    "When not busy, {0} practices synchronized roller skating with roller derby queens.",
    "{0} is a professional bubble wrap castle architect.",
    "{0} moonlights as a professional stilt walker for garden gnomes.",
    "{0} specializes in training crows for synchronized sky performances.",
    "{0} is a certified expert in deciphering ancient hieroglyphs on candy wrappers.",
    "{0} is a professional rainbow chaser, painting the sky with vibrant hues.",
    "Meet {0}, the official rubber band orchestra conductor.",
    "{0} moonlights as a professional flamingo tamer.",
    "{0} offers premium services as a professional squirrel comedian.",
    "When not busy, {0} practices synchronized interpretive dance with wind turbines.",
    "{0} is a certified expert in teaching squirrels to dance the cha-cha.",
    "{0} is a professional cloud shape shifter, turning clouds into whimsical creatures.",
    "Introducing {0}, a master at interpretive dance with tumbleweeds.",
    "{0} specializes in composing symphonies for underwater harmonicas.",
    "{0} is a certified expert in training dolphins to moonwalk.",
    "{0} is a professional shadow puppeteer for campfires.",
    "Meet {0}, the official squirrel choreographer, mastering tree-bound routines.",
    "{0} moonlights as a professional bubble wrap composer.",
    "{0} offers premium services as a professional squirrel fashion designer.",
    "When not busy, {0} practices synchronized breakdancing with breakdancing beetles.",
    "{0} is a certified expert in teaching squirrels to do the limbo.",
    "{0} is a professional cloud surfer, riding waves through the sky.",
    "Introducing {0}, a master at interpretive dance with tumble dryers.",
    "{0} specializes in composing symphonies for underwater tubas.",
    "{0} is a certified expert in teaching seahorses to square dance.",
    "{0} is a professional firefly choreographer, creating mesmerizing light shows.",
    "Meet {0}, the official squirrel acrobat, flipping through trees with finesse.",
    "{0} moonlights as a professional bubble wrap sculptor.",
    "{0} offers premium services as a professional squirrel motivational speaker.",
    "When not busy, {0} practices synchronized interpretive dance with whirlwinds.",
    "{0} is a certified expert in training ants to perform synchronized swimming.",
    "{0} is a professional cloud graffiti artist, tagging the sky with creativity.",
    "Introducing {0}, a master at interpretive dance with tumbleweeds.",
    "{0} specializes in composing symphonies for underwater piccolos.",
    "{0} is a certified expert in teaching seals to tango.",
    "{0} is a professional shadow puppeteer for campfires."]

fake_robbery_scenarios = [
    ("{0} attempted to steal {1}'s collection of rubber duckies but got chased away by a squirrel,", False),
    ("In a daring heist, {0} tried to snatch {1}'s cookie jar, but it turned out to be a decoy filled with broccoli,",
     False),
    ("{0} disguised themselves as a penguin to swipe {1}'s snow cone, but slipped on a banana peel instead,", False),
    ("During the grand heist, {0} went after {1}'s invisible treasure chest and accidentally knocked over a lamp,",
     False),
    ("{0} dressed up as a ninja to nab {1}'s pillow, only to realize it was a marshmallow-filled decoy,", False),
    ("In an audacious move, {0} attempted to steal {1}'s fake gold coins, but they were just chocolate wrappers,",
     False),
    ("{0} plotted to take {1}'s invisible sandwich, but their getaway vehicle was a slow-moving turtle,", False),
    (
        "During the master plan, {0} aimed to snatch {1}'s secret banana stash, but got caught in a game of hide-and-seek,",
        False),
    ("{0} hatched a cunning scheme to steal {1}'s rubber chicken collection, but tripped over a feather,", False),
    ("In a comedic twist, {0} tried to take {1}'s invisible pet rock, only to discover it was made of air,", False),
    ("{0} schemed to nab {1}'s fake mustache collection, but got tangled in the disguise,", False),
    ("During the elaborate caper, {0} attempted to steal {1}'s bubble wrap, but ended up popping half of it,", False),
    ("{0} orchestrated a plan to take {1}'s toy spaceship, but got stuck in a pile of building blocks,", False),
    ("In a daring plot, {0} tried to snatch {1}'s invisible hat, but was foiled by a gust of wind,", False),
    ("{0} disguised themselves as a superhero to nab {1}'s rubber band ball, but it bounced away,", False),
    ("During the grand heist, {0} went after {1}'s pretend pirate treasure, only to find plastic coins,", False),
    ("{0} plotted to steal {1}'s cardboard castle, but got trapped in a cardboard dragon's jaws,", False),
    ("In an audacious move, {0} attempted to take {1}'s collection of invisible stamps, but lost their map,", False),
    ("{0} dressed up as a cowboy to snatch {1}'s imaginary lasso, but tripped over a tumbleweed,", False),
    ("During the master plan, {0} aimed to steal {1}'s toy crown, but got stuck in a toy robot's grip,", False),
    ("{0} hatched a cunning scheme to take {1}'s fake treasure map, but got lost in the crayon-drawn maze,", False),
    ("In a comedic twist, {0} tried to nab {1}'s invisible sunglasses, but couldn't find them,", False),
    ("{0} schemed to steal {1}'s toy race car, but accidentally triggered a toy car avalanche,", False),
    (
        "During the elaborate caper, {0} attempted to snatch {1}'s pretend detective kit, but left a trail of toy footprints,",
        False),
    ("{0} orchestrated a plan to take {1}'s collection of toy bugs, but they scattered everywhere,", False),
    ("In a daring plot, {0} tried to steal {1}'s imaginary friend's favorite toy, but it vanished,", False),
    ("{0} disguised themselves as a magician to nab {1}'s magic wand, but it turned into a rubber chicken,", False),
    ("During the grand heist, {0} went after {1}'s toy telescope, but saw only clouds,", False),
    ("{0} plotted to steal {1}'s invisible jetpack, but ended up floating away,", False),
    (
        "In an audacious move, {0} attempted to take {1}'s pretend crown, but got caught in a paper crown's strap,",
        False),
    ("{0} dressed up as a spy to snatch {1}'s toy spy gear, but triggered all the alarms,", False),
    (
        "During the master plan, {0} aimed to steal {1}'s collection of toy dinosaurs, but they came to life and chased them,",
        False),
    ("{0} hatched a cunning scheme to nab {1}'s invisible ninja sword, but it turned into a pool noodle,", False),
    ("In a comedic twist, {0} tried to steal {1}'s magic potion kit, but spilled it all over themselves,", False),
    ("{0} schemed to take {1}'s toy rocket, but got stuck in the launch pad,", False),
    ("During the elaborate caper, {0} attempted to snatch {1}'s superhero cape, but got tangled in it,", False),
    ("{0} orchestrated a plan to steal {1}'s collection of toy robots, but they rebelled against them,", False),
    ("In a daring plot, {0} tried to steal {1}'s invisible time machine, but ended up in a cardboard box,", False),
    ("{0} disguised themselves as a pirate to nab {1}'s toy treasure chest, but it was filled with candy,", False),
    ("During the grand heist, {0} went after {1}'s pretend chef kit, but ended up covered in toy spaghetti,", False),
    ("{0} plotted to steal {1}'s toy magic carpet, but it got caught on a doorknob,", False),
    (
        "In an audacious move, {0} attempted to take {1}'s collection of toy trains, but they went off the tracks,",
        False),
    ("{0} dressed up as a wizard to snatch {1}'s magic wand, but turned themselves into a frog,", False),
    ("During the master plan, {0} aimed to steal {1}'s invisible superhero suit, but it was too slippery,", False),
    ("{0} hatched a cunning scheme to nab {1}'s toy pirate ship, but it sailed away in a tub,", False),
    ("In a comedic twist, {0} tried to steal {1}'s toy detective magnifying glass, but looked the wrong way,", False),
    ("{0} schemed to take {1}'s collection of toy aliens, but they zapped them with toy ray guns,", False),
    ("During the elaborate caper, {0} attempted to snatch {1}'s pretend knight armor, but got stuck in it,", False),
    ("{0} orchestrated a plan to steal {1}'s toy space shuttle, but it crash-landed on a book,", False),
    ("In a daring plot, {0} tried to steal {1}'s invisible pirate treasure, but it was guarded by an invisible dragon,",
     False),
    ("{0} plotted to steal {1}'s toy race car track, but the cars kept crashing into each other,", False),
    (
        "In an audacious move, {0} attempted to take {1}'s collection of toy animals, but they all escaped to the backyard,",
        False),
    ("{0} dressed up as a pilot to snatch {1}'s toy airplane, but it got stuck in a tree,", False),
    ("During the master plan, {0} aimed to steal {1}'s invisible knight sword, but it was too heavy,", False),
    ("{0} hatched a cunning scheme to nab {1}'s toy firefighter hat, but got caught in a game of 'put out the fire,'",
     False),
    ("In a comedic twist, {0} tried to steal {1}'s toy doctor kit, but ended up with a toy thermometer in their ear,",
     False),
    ("{0} schemed to take {1}'s collection of toy construction vehicles, but they all started 'building' a sandcastle,",
     False),
    (
        "During the elaborate caper, {0} attempted to snatch {1}'s pretend scientist goggles, but they were stuck to their forehead,",
        False),
    ("{0} orchestrated a plan to steal {1}'s toy robot dog, but it kept chasing its tail,", False),
    ("In a daring plot, {0} tried to steal {1}'s invisible superhero cape, but it turned into a blanket,", False),
    ("{0} disguised themselves as a chef to nab {1}'s toy kitchen set, but got tangled in a spaghetti mess,", False),
    ("During the grand heist, {0} went after {1}'s pretend explorer backpack, but got lost in the living room,", False),
    ("{0} plotted to steal {1}'s toy spy glasses, but couldn't see a thing through them,", False),
    (
        "In an audacious move, {0} attempted to take {1}'s collection of toy musical instruments, but all they got was a kazoo,",
        False),
    ("{0} dressed up as a superhero to snatch {1}'s toy mask, but it got stuck on their head,", False),
    ("During the master plan, {0} aimed to steal {1}'s invisible pirate hat, but it vanished into thin air,", False),
    ("{0} hatched a cunning scheme to nab {1}'s toy firefighter hose, but it squirted them instead,", False),
    ("In a comedic twist, {0} tried to steal {1}'s toy magician's hat, but pulled out a rubber chicken,", False),
    ("{0} schemed to take {1}'s collection of toy sports equipment, but they all bounced away,", False),
    ("During the elaborate caper, {0} attempted to snatch {1}'s pretend artist beret, but it got stuck in their hair,",
     False),
    ("{0} orchestrated a plan to steal {1}'s toy chef apron, but got tangled in the strings,", False),
    ("In a daring plot, {0} tried to steal {1}'s invisible astronaut helmet, but it was just a clear bowl,", False),
    ("{0} disguised themselves as a spy to nab {1}'s toy magnifying glass, but it showed everything upside down,",
     False),
    (
        "During the grand heist, {0} went after {1}'s pretend scientist lab coat, but spilled fake potions all over themselves,",
        False),
    ("{0} plotted to steal {1}'s toy firefighter boots, but they were too big to fit,", False),
    ("In an audacious move, {0} attempted to take {1}'s collection of toy building blocks, but they toppled over,",
     False),
    ("{0} dressed up as a magician to snatch {1}'s toy wand, but it turned into a rubber chicken,", False),
    ("During the master plan, {0} aimed to steal {1}'s invisible explorer hat, but it was see-through,", False),
    ("{0} hatched a cunning scheme to nab {1}'s toy detective pipe, but blew bubbles instead,", False),
    ("In a comedic twist, {0} tried to steal {1}'s toy rock collection, but they all rolled away,", False),
    ("{0} schemed to take {1}'s collection of toy animal figures, but they all went on strike,", False),
    ("During the elaborate caper, {0} attempted to snatch {1}'s pretend chef spoon, but stirred up a mess,", False),
    ("{0} orchestrated a plan to steal {1}'s toy astronaut helmet, but it got stuck on their foot,", False),
    ("In a daring plot, {0} tried to steal {1}'s invisible scientist glasses, but they couldn't see through them,",
     False),
    ("{0} disguised themselves as a superhero to nab {1}'s toy cape, but it was too short,", False),
    ("During the grand heist, {0} went after {1}'s pretend artist paintbrush, but ended up with colorful fingers,",
     False),
    ("{0} plotted to steal {1}'s toy pirate hat, but it blew away in the wind,", False),
    ("In an audacious move, {0} attempted to take {1}'s toy firefighter helmet, but got stuck with their head inside,",
     False),
    ("{0} dressed up as a pirate to snatch {1}'s toy treasure chest, but it was filled with costume jewelry,", False),
    (
        "During the master plan, {0} aimed to steal {1}'s invisible doctor stethoscope, but it tickled their ears,",
        False),
    ("{0} hatched a cunning scheme to nab {1}'s pretend explorer map, but it led them in circles,", False),
    ("In a comedic twist, {0} tried to steal {1}'s collection of toy vehicles, but they all had flat tires,", False),
    ("{0} schemed to take {1}'s toy astronaut gloves, but they were too slippery to hold,", False),
    (
        "During the elaborate caper, {0} attempted to snatch {1}'s pretend scientist test tubes, but they were filled with glitter,",
        False),
    ("{0} orchestrated a plan to steal {1}'s toy detective notebook, but it was full of doodles,", False),
    ("In a daring plot, {0} tried to steal {1}'s invisible chef hat, but it turned into a feather boa,", False),
    ("{0} disguised themselves as a scientist to nab {1}'s toy lab coat, but got caught in the sleeves,", False),
    ("During the grand heist, {0} went after {1}'s pretend superhero belt, but it was too tight,", False),
    ("{0} plotted to steal {1}'s toy construction helmet, but it fell over their eyes,", False),
    ("{0} managed to stealthily swipe {1}'s collection of rubber duckies and escaped without a trace,", True),
    ("In a daring heist, {0} successfully nabbed {1}'s cookie jar and left behind a trail of crumbs,", True),
    ("{0} disguised themselves as a penguin and skillfully snatched {1}'s snow cone before melting away,", True),
    ("During the grand heist, {0} managed to unlock {1}'s invisible treasure chest and made off with the loot,", True),
    ("{0} dressed up as a ninja and swiftly took {1}'s pillow without leaving a sound,", True),
    (
        "In an audacious move, {0} pulled off a heist to steal {1}'s fake gold coins, leaving behind a note that said 'chocolate wrappers won't fool me,'",
        True),
    ("{0} successfully swiped {1}'s invisible sandwich and left a note saying 'thanks for the air,'", True),
    (
        "During the master plan, {0} cleverly outwitted {1} in a game of hide-and-seek and claimed their secret banana stash,",
        True),
    ("{0} managed to snatch {1}'s rubber chicken collection with finesse and disappeared in a puff of feathers,", True),
    (
        "In a comedic twist, {0} swiftly nabbed {1}'s invisible pet rock and left a note saying 'now I have an imaginary friend,'",
        True),
    ("{0} schemed to steal {1}'s cardboard castle, but used their cunning to outsmart the cardboard dragon,", True),
    ("In an audacious move, {0} successfully navigated through the invisible stamp collection and secured the loot,",
     True),
    ("During the elaborate caper, {0} carefully swiped {1}'s bubble wrap, leaving behind a symphony of pops,", True),
    ("{0} orchestrated a plan to take {1}'s toy spaceship and embarked on a cosmic adventure,", True),
    (
        "In a daring plot, {0} aimed to steal {1}'s toy telescope and gazed at the stars from the comfort of their hideout,",
        True),
    (
        "{0} disguised themselves as a superhero and skillfully snatched {1}'s rubber band ball before it could bounce away,",
        True),
    (
        "During the grand heist, {0} managed to outwit {1} and claimed the pretend pirate treasure, leaving behind a trail of laughter,",
        True),
    (
        "{0} plotted to steal {1}'s invisible jetpack and soared through the imaginary skies, leaving a trail of 'invisible' contrails,",
        True),
    (
        "In an audacious move, {0} successfully nabbed {1}'s pretend crown and declared themselves the ruler of the playroom,",
        True),
    ("During the master plan, {0} skillfully outmaneuvered {1}'s toy dinosaurs and made off with the prehistoric loot,",
     True),
    ("{0} hatched a cunning scheme to steal {1}'s invisible ninja sword and vanished like a shadow,", True),
    ("In a comedic twist, {0} slyly swiped {1}'s magic potion kit and concocted laughter-inducing mixtures,", True),
    ("{0} schemed to take {1}'s toy rocket and launched it on a high-flying adventure,", True),
    (
        "During the elaborate caper, {0} cleverly nabbed {1}'s pretend detective kit and left behind a trail of toy footprints as a diversion,",
        True),
    (
        "{0} orchestrated a plan to steal {1}'s collection of toy bugs, leaving behind a miniature 'bug-sized' thank-you note,",
        True),
    (
        "In a daring plot, {0} managed to outsmart {1} and secured the invisible friend's favorite toy, leaving behind a friendly wink,",
        True),
    (
        "{0} disguised themselves as a magician and skillfully swiped {1}'s magic wand, leaving behind a bouquet of rubber chickens,",
        True),
    (
        "During the grand heist, {0} cleverly swiped {1}'s toy telescope and left a note saying 'now I can see the universe,'",
        True),
    ("{0} plotted to steal {1}'s toy magic carpet and whisked themselves away on an enchanted ride,", True),
    (
        "In an audacious move, {0} successfully nabbed {1}'s collection of toy aliens and declared themselves the new extraterrestrial leader,",
        True),
    ("{0} dressed up as a knight and managed to secure {1}'s pretend knight armor, leaving behind a trail of chivalry,",
     True),
    (
        "During the master plan, {0} skillfully swiped {1}'s toy space shuttle and embarked on a mission to explore the playroom galaxy,",
        True),
    (
        "In a daring plot, {0} managed to outwit {1} and claimed the invisible pirate treasure, leaving behind a note that said 'x marks the spot,'",
        True),
    (
        "{0} disguised themselves as a chef and successfully nabbed {1}'s toy kitchen set, leaving behind a gourmet imaginary feast,",
        True),
    (
        "During the grand heist, {0} cleverly swiped {1}'s pretend explorer backpack and embarked on an imaginary adventure of their own,",
        True),
    ("{0} plotted to steal {1}'s toy spy glasses and left a cryptic note that said 'I spy with my little eye,'", True),
    (
        "In an audacious move, {0} successfully secured {1}'s collection of toy musical instruments and orchestrated a playful symphony,",
        True),
    (
        "{0} dressed up as a superhero and skillfully swiped {1}'s toy mask, leaving behind a note that said 'now I have the power,'",
        True),
    (
        "During the master plan, {0} managed to outwit {1} and claimed the invisible explorer hat, leaving behind an 'invisible' thank-you note,",
        True),
    ("{0} hatched a cunning scheme to steal {1}'s toy firefighter hose and extinguished imaginary fires all around,",
     True),
    (
        "In a comedic twist, {0} slyly swiped {1}'s toy magician's hat and left behind a trail of floating rabbits,",
        True),
    ("{0} schemed to take {1}'s collection of toy sports equipment and organized an epic playroom championship,", True),
    (
        "During the elaborate caper, {0} skillfully nabbed {1}'s pretend artist beret and created a masterpiece of silliness,",
        True),
    ("{0} orchestrated a plan to steal {1}'s toy chef apron and cooked up a feast of imagination,", True),
    (
        "In a daring plot, {0} managed to secure {1}'s invisible astronaut helmet and embarked on an intergalactic adventure,",
        True),
    (
        "{0} disguised themselves as a spy and successfully nabbed {1}'s toy magnifying glass, leaving behind a trail of mystery,",
        True),
    (
        "During the grand heist, {0} cleverly swiped {1}'s pretend scientist lab coat and concocted laughter-inducing 'potions,'",
        True),
    ("{0} plotted to steal {1}'s toy firefighter boots and left behind a trail of imaginary 'footprints,'", True),
    (
        "In an audacious move, {0} skillfully managed to secure {1}'s collection of toy building blocks and constructed a tower of imagination,",
        True),
    (
        "{0} dressed up as a magician and skillfully swiped {1}'s toy wand, leaving behind a flurry of magically appearing rubber chickens,",
        True),
    (
        "During the master plan, {0} outwitted {1} and claimed the invisible explorer hat, leaving behind an 'invisible' thank-you note,",
        True),
    ("{0} hatched a cunning scheme to steal {1}'s toy firefighter hose and extinguished imaginary fires all around,",
     True),
    (
        "In a comedic twist, {0} slyly swiped {1}'s toy magician's hat and left behind a trail of floating rabbits,",
        True),
    ("{0} schemed to take {1}'s collection of toy sports equipment and organized an epic playroom championship,", True),
    (
        "During the elaborate caper, {0} skillfully nabbed {1}'s pretend artist beret and created a masterpiece of silliness,",
        True),
    ("{0} orchestrated a plan to steal {1}'s toy chef apron and cooked up a feast of imagination,", True),
    (
        "In a daring plot, {0} managed to secure {1}'s invisible astronaut helmet and embarked on an intergalactic adventure,",
        True),
    (
        "{0} disguised themselves as a spy and successfully nabbed {1}'s toy magnifying glass, leaving behind a trail of mystery,",
        True),
    (
        "During the grand heist, {0} cleverly swiped {1}'s pretend scientist lab coat and concocted laughter-inducing 'potions,'",
        True),
    ("{0} plotted to steal {1}'s toy firefighter boots and left behind a trail of imaginary 'footprints,'", True),
    (
        "In an audacious move, {0} skillfully managed to secure {1}'s collection of toy building blocks and constructed a tower of imagination,",
        True),
    (
        "{0} dressed up as a magician and skillfully swiped {1}'s toy wand, leaving behind a flurry of magically appearing rubber chickens,",
        True),
    (
        "During the master plan, {0} skillfully managed to secure {1}'s collection of toy animals, creating a zoo of imagination,",
        True),
    ("{0} orchestrated a plan to steal {1}'s toy airplane and took an imaginary flight to new heights,", True),
    (
        "In a daring plot, {0} managed to outwit {1} and claimed the invisible knight sword, becoming the champion of the playroom,",
        True),
    (
        "{0} disguised themselves as a scientist and skillfully swiped {1}'s toy volcano, conducting 'eruptions' of laughter,",
        True),
    (
        "During the grand heist, {0} cleverly nabbed {1}'s pretend superhero mask and left behind a note saying 'I'm now the masked giggler,'",
        True),
    ("{0} plotted to steal {1}'s toy race car track and raced away with imaginary speed,", True),
    (
        "In an audacious move, {0} skillfully secured {1}'s collection of toy musical instruments, orchestrating a symphony of silliness,",
        True),
    (
        "{0} dressed up as a superhero and successfully swiped {1}'s toy cape, leaving behind a trail of invisible heroics,",
        True),
    (
        "During the master plan, {0} managed to outwit {1} and claimed the invisible pirate hat, leaving a note that said 'Arrr, I've got it now,'",
        True),
    (
        "{0} hatched a cunning scheme to steal {1}'s toy firefighter hat and extinguished imaginary blazes throughout the playroom,",
        True),
    ("In a comedic twist, {0} skillfully swiped {1}'s toy doctor kit and administered laughter-inducing 'checkups,'",
     True),
    ("{0} schemed to take {1}'s collection of toy construction vehicles and embarked on a whimsical building project,",
     True),
    (
        "During the elaborate caper, {0} cleverly nabbed {1}'s pretend scientist goggles and examined a world of silliness,",
        True),
    ("{0} orchestrated a plan to steal {1}'s toy robot dog and played fetch with an invisible ball,", True),
    (
        "In a daring plot, {0} managed to secure {1}'s invisible superhero cape and became the guardian of imaginative adventures,",
        True),
    (
        "{0} disguised themselves as a chef and skillfully swiped {1}'s toy kitchen set, creating a feast of pretend delicacies,",
        True),
    ("During the grand heist, {0} cleverly swiped {1}'s pretend explorer backpack and embarked on an imaginary quest,",
     True),
    ("{0} plotted to steal {1}'s toy spy glasses and left a note that said 'I've got my eyes on the fun,'", True),
    (
        "In an audacious move, {0} successfully secured {1}'s collection of toy musical instruments and orchestrated a symphony of silliness,",
        True),
    ("{0} dressed up as a superhero and skillfully swiped {1}'s toy mask, leaving behind a trail of invisible heroics,",
     True),
    (
        "During the master plan, {0} managed to outwit {1} and claimed the invisible explorer hat, leaving a note that said 'Discovering laughter,'",
        True),
    (
        "{0} hatched a cunning scheme to steal {1}'s toy firefighter hose and extinguished imaginary blazes throughout the playroom,",
        True),
    ("In a comedic twist, {0} skillfully swiped {1}'s toy magician's hat and left behind a trail of floating laughter,",
     True),
    ("{0} schemed to take {1}'s collection of toy sports equipment and organized an epic playroom championship,", True),
    (
        "During the elaborate caper, {0} cleverly nabbed {1}'s pretend artist beret and created a masterpiece of silliness,",
        True),
    ("{0} orchestrated a plan to steal {1}'s toy chef apron and cooked up a feast of imagination,", True),
    (
        "In a daring plot, {0} managed to secure {1}'s invisible astronaut helmet and embarked on an intergalactic adventure,",
        True),
    (
        "{0} disguised themselves as a spy and successfully nabbed {1}'s toy magnifying glass, leaving behind a trail of mystery,",
        True),
    (
        "During the grand heist, {0} cleverly swiped {1}'s pretend scientist lab coat and concocted laughter-inducing 'potions,'",
        True),
    ("{0} plotted to steal {1}'s toy firefighter boots and left behind a trail of imaginary 'footprints,'", True),
    (
        "In an audacious move, {0} skillfully managed to secure {1}'s collection of toy building blocks and constructed a tower of imagination,",
        True),
    (
        "{0} dressed up as a magician and skillfully swiped {1}'s toy wand, leaving behind a flurry of magically appearing rubber chickens,",
        True), (
        "During the master plan, {0} skillfully swiped {1}'s toy pirate hat and left a note saying 'Ahoy, matey, the caper was a success!'",
        True),
    ("{0} managed to outsmart {1} and secured the invisible superhero belt, becoming the champion of imagination,",
     True),
    ("In a daring plot, {0} skillfully nabbed {1}'s toy construction helmet and became the 'chief architect' of fun,",
     True),
    ("{0} disguised themselves as a scientist and managed to secure {1}'s toy volcano, creating eruptions of laughter,",
     True),
    (
        "During the grand heist, {0} successfully swiped {1}'s pretend artist paintbrush, leaving behind a trail of colorful creativity,",
        True),
    ("{0} plotted to steal {1}'s toy pirate hat and set sail on an imaginary treasure-seeking adventure,", True),
    (
        "In an audacious move, {0} skillfully secured {1}'s toy firefighter helmet and became the hero of playroom safety,",
        True),
    ("{0} managed to outwit {1} and claimed the pretend pirate treasure, leaving behind a map of laughter,", True),
    ("During the master plan, {0} skillfully nabbed {1}'s invisible jetpack and soared through their imagination,",
     True),
    (
        "{0} disguised themselves as a king and managed to secure {1}'s toy crown, declaring themselves the ruler of playroom fun,",
        True),
    (
        "In a daring plot, {0} skillfully swiped {1}'s collection of toy dinosaurs, leading them on an epic prehistoric adventure,",
        True),
    ("{0} orchestrated a plan to steal {1}'s toy knight armor and became the defender of the playroom kingdom,", True),
    (
        "During the grand heist, {0} cleverly managed to outwit {1} and claimed the toy space shuttle, launching their creativity into orbit,",
        True),
    (
        "{0} plotted to steal {1}'s invisible treasure chest and left behind a note that said 'I've uncovered a chest of laughter,'",
        True),
    (
        "In an audacious move, {0} skillfully secured {1}'s toy magic carpet and embarked on an imaginary journey to magical lands,",
        True),
    (
        "{0} managed to outsmart {1} and claimed the collection of toy aliens, declaring themselves the new commander of the toy universe,",
        True),
    (
        "During the master plan, {0} skillfully nabbed {1}'s pretend knight sword and became the legendary swordmaster of playroom legends,",
        True),
    (
        "{0} disguised themselves as a scientist and successfully secured {1}'s toy rocket, launching a mission to explore the unknown,",
        True),
    (
        "In a daring plot, {0} skillfully swiped {1}'s invisible pirate treasure and left behind an 'invisible' thank-you note,",
        True),
    (
        "{0} managed to outwit {1} and claimed the toy firefighter hat, becoming the fearless guardian of imaginative adventures,",
        True),
    (
        "During the grand heist, {0} cleverly swiped {1}'s toy doctor kit and left behind a note that said 'Doctor {0} reporting for fun duty!'",
        True),
    (
        "{0} plotted to steal {1}'s collection of toy construction vehicles and created a bustling playroom construction site,",
        True),
    (
        "In an audacious move, {0} skillfully secured {1}'s pretend scientist goggles and discovered a world of laughter and curiosity,",
        True),
    (
        "{0} orchestrated a plan to steal {1}'s toy robot dog and embarked on a robotic adventure through their imagination,",
        True),
    (
        "During the master plan, {0} managed to outsmart {1} and claimed the invisible superhero cape, becoming the playroom's true hero,",
        True),
    (
        "{0} disguised themselves as a chef and skillfully swiped {1}'s toy kitchen set, creating a feast of imaginative delights,",
        True),
    (
        "In a daring plot, {0} skillfully secured {1}'s pretend explorer backpack and embarked on an adventure of pretend discoveries,",
        True),
    ("{0} plotted to steal {1}'s toy spy glasses and left a note saying 'I've got my eyes on the fun!'", True),
    (
        "In an audacious move, {0} skillfully nabbed {1}'s collection of toy musical instruments and orchestrated a symphony of playroom joy,",
        True),
    ("{0} dressed up as a superhero and managed to secure {1}'s toy mask, becoming the mysterious playroom guardian,",
     True),
    (
        "During the master plan, {0} skillfully swiped {1}'s invisible explorer hat and embarked on a journey of laughter and adventure,",
        True),
    (
        "{0} managed to outwit {1} and claimed the toy firefighter hose, extinguishing imaginary fires with playful flair,",
        True),

]

funny_crime_scenarios = [(
    "In an imaginative endeavor, {0} tried to steal the concept of 'daydreaming,' leaving everyone lost in thought,",
    False), (
    "In a quirky move, {0} tried to steal all the 'lost socks' in town, causing laundry day chaos,",
    False), (
    '{0} Attempted to rob a comedy movie marathon, but got caught up in the hilarity on screen,',
    False), (
    "{0} Successfully organized a 'whoopie cushion' heist during an event, leaving everyone laughing in surprise,",
    True), (
    "{0} Successfully organized a 'prank war' heist, turning an ordinary day into a hilarious battleground,",
    True), (
    "In a light-hearted move, {0} tried to steal the concept of 'Monday blues,' but got stuck in a loop of fun instead,",
    False), (
    "In a playful move, {0} attempted to steal the 'Recipe for Happiness,' but it required too many ingredients,",
    False), (
    "{0} Attempted to steal the Eiffel Tower during a vacation, claiming it as a 'souvenir,'",
    False), (
    "In a playful move, {0} tried to steal the 'Recipe for Happiness,' but it required too many ingredients,",
    False), (
    "{0} Attempted to rob a tickle fight tournament, but got caught up in the laughter and couldn't continue,",
    False), (
    '{0} Attempted to steal the moon from the night sky, but ended up with a handful of stardust,',
    False), (
    "In an audacious twist, {0} tried to steal a clown's horn, leading to a parade of honking cars,",
    False), (
    "In a daring scheme, {0} tried to steal a rainbow's end, only to find a pot of glitter instead of gold,",
    False), (
    "{0} Successfully organized a 'pillow pet' parade during their attempt to steal a pillow factory's inventory,",
    True), (
    "In a quirky move, {0} attempted to steal the 'Lost and Found' box, claiming it as their own treasure chest,",
    False), (
    "In a whimsical move, {0} tried to steal a mime's invisible props, but ended up pretending to be trapped in a box,",
    False), (
    "In a playful twist, {0} tried to steal a magician's top hat, but pulled out endless amounts of scarves instead,",
    False), (
    "{0} Attempted to steal the concept of 'personal space,' but got too close to everyone's comfort zone,",
    False), (
    "In a daring move, {0} tried to steal the concept of 'good vibes,' leaving behind a trail of positivity,",
    False), (
    "{0} Successfully organized a 'silly string' heist during a parade, coating the entire route in colorful chaos,",
    True), (
    "{0} Successfully organized a 'slow-motion' heist at a snail racing event, leaving everyone in stitches,",
    True), (
    'In a whimsical twist, {0} tried to steal all the clown noses in town, causing a wave of laughter,',
    False), (
    "In a mischievous move, {0} tried to steal a street performer's hat full of tips, but it was filled with rubber ducks,",
    False), (
    "{0} Successfully organized a 'laughter yoga' heist, leaving everyone in fits of laughter,",
    True), (
    "{0} Successfully staged a 'silly string' heist, leaving the entire city covered in vibrant chaos,",
    True), (
    "In an audacious twist, {0} tried to steal the concept of 'good vibes,' but got caught in a wave of positivity,",
    False),
    ("{0} Successfully staged a 'tug-of-war' heist, pitting laughter against seriousness,", True),
    (
        "{0} Successfully staged a 'hot dog eating contest' heist, leaving everyone with full bellies and laughter,",
        True),
    ('{0} Attempted to rob a laughter yoga class, but left feeling lighter than air,', False), (
        "In a playful move, {0} tried to steal the world's largest rubber band ball, but it bounced back,",
        False), (
        '{0} Attempted to rob a pillow fight flash mob, but got caught in a flurry of feathers,',
        False), (
        "In a quirky move, {0} attempted to steal all the 'lost socks' in town, causing laundry day chaos,",
        False), (
        '{0} Attempted to rob a joke shop, but ended up setting off a chain reaction of laughter instead,',
        False), (
        "{0} Successfully staged a 'giant bubble' heist, leaving the streets filled with floating fun,",
        True), (
        "In a playful move, {0} tried to steal the 'last slice of pizza,' igniting a pizza-loving frenzy,",
        False), (
        "{0} Successfully staged a 'giant whoopie cushion' heist, leaving the city's landmarks with surprise sound effects,",
        True), (
        "{0} Successfully organized a 'pie throwing' event during their attempt to rob a bakery,",
        True), (
        "In a whimsical move, {0} attempted to steal a magician's top hat, but pulled out endless amounts of scarves instead,",
        False), (
        "In a playful move, {0} attempted to steal a mime's invisible props, but got tangled in imaginary ropes,",
        False), (
        "{0} Successfully organized a 'carnival game' heist, leaving the fairgrounds buzzing with laughter,",
        True), (
        "In a light-hearted twist, {0} attempted to steal a street performer's tip jar, but ended up juggling coins instead,",
        False), (
        '{0} Tried to steal a cloud shaped like a treasure chest, but got rained on and lost their loot,',
        False), (
        "{0} Attempted to rob a comedy club's open mic night, but got caught up in the laughter of the audience,",
        False), (
        "In a daring heist, {0} tried to steal the concept of 'awkward silence,' but ended up in an endless loop of conversations,",
        False),
    ('{0} Attempted to rob a laughter yoga class, but left laughing too hard to continue,', False),
    (
        "In a creative move, {0} tried to steal the 'last piece of cake' from a birthday party, leading to a cake war,",
        False), (
        "In a whimsical move, {0} attempted to steal a magician's wand, but could only produce rubber chickens,",
        False), (
        "{0} Tried to steal the town's supply of ice cream, but the ice cream truck drove away before they could escape,",
        False), (
        "In an imaginative move, {0} tried to steal the concept of 'daylight saving time,' leaving everyone an hour behind,",
        False), (
        "In a whimsical scheme, {0} tried to steal the concept of 'daydreaming,' leaving everyone lost in thought,",
        False), (
        "In a playful twist, {0} attempted to steal the 'Do Not Disturb' signs from a hotel, claiming to be the master of solitude,",
        False), (
        '{0} Attempted to rob a pillow fight tournament, but got caught up in the feather frenzy,',
        False), (
        "{0} Successfully staged a 'reverse robbery' where they handed out candy and balloons to bank customers,",
        True), (
        "In a hilarious twist, {0} tried to steal the concept of 'Monday blues,' but everyone celebrated instead,",
        False), (
        "{0} Tried to steal the concept of 'personal space,' but got too close to everyone's comfort zone,",
        False), (
        "{0} Attempted to rob a tickle fight tournament, but couldn't stop laughing long enough to execute the plan,",
        False), (
        "In a daring endeavor, {0} tried to steal the concept of 'tickling,' leaving everyone giggling uncontrollably,",
        False), (
        "In a creative scheme, {0} tried to steal the 'Do Not Disturb' signs from a hotel, only to be caught napping,",
        False), (
        'In a daring heist, {0} tried to steal the scent of freshly baked cookies, but ended up smelling like vanilla,',
        False), (
        "In an audacious scheme, {0} tried to steal the concept of 'Monday blues,' but ended up with a case of bad luck,",
        False), (
        "{0} Successfully staged a 'banana peel' heist, leaving a trail of hilarious slip-ups in their wake,",
        True), (
        "In an audacious twist, {0} tried to steal the concept of 'awkward silence,' leaving everyone speechless,",
        False), (
        "{0} Successfully organized a 'silly walk' heist, turning the streets into a whimsical parade,",
        True), (
        "{0} Attempted to rob a 'bad joke' stand, but all the jokes were so bad that they gave up,",
        False), (
        "In a mischievous endeavor, {0} tried to steal a street performer's hat full of tips, but it was filled with rubber ducks,",
        False), (
        '{0} Tried to steal a cloud shaped like a treasure chest, but it slipped through their fingers like watercolor paint,',
        False), (
        '{0} Attempted to rob a balloon animal convention, but got caught in a balloon animal knot,',
        False), (
        "{0} Successfully staged a 'chocolate fountain' heist, turning a party into a sweet mess,",
        True), (
        '{0} Attempted to rob a music store, but ended up leading an impromptu dance party instead,',
        False), (
        "In a playful endeavor, {0} tried to steal the concept of 'smiles,' leaving everyone grinning from ear to ear,",
        False), (
        "In a daring heist, {0} tried to steal the concept of 'awkward silence,' but ended up in an endless loop of conversation,",
        False), (
        "{0} Successfully organized a 'tug-of-war' heist, pitting laughter against seriousness,",
        True), (
        "In an audacious move, {0} tried to steal the world's largest rubber chicken, but it turned out to be an 'egg-streme' decoy,",
        False), (
        "In a whimsical twist, {0} tried to steal the concept of 'rainbows,' leaving everyone searching the sky for colors,",
        False), (
        "In a comedic twist, {0} tried to steal a comedian's microphone, but all they got was feedback,",
        False), (
        'In a creative plot, {0} tried to rob a bubblegum factory, only to end up in a sticky situation,',
        False), (
        '{0} Tried to rob a balloon animal convention, but ended up with a room full of inflated animals instead,',
        False), (
        '{0} Tried to steal a cloud shaped like a treasure chest, but it drifted away like a dream,',
        False), (
        '{0} Attempted to rob a circus, but got distracted by juggling and tightrope walking,', False),
    (
        'In a hilarious move, {0} tried to rob a hair salon, but got tangled up in their own wig collection,',
        False), (
        "{0} Successfully staged a 'whoopie cushion' heist during a formal event, leading to unexpected bursts of laughter,",
        True), (
        "In a playful plot, {0} tried to steal the 'recipe for laughter' from a comedy club, but it was too secret to find,",
        False), (
        'In a playful twist, {0} attempted to rob a prank store, but got pranked by the employees instead,',
        False), (
        "In an ambitious endeavor, {0} tried to steal the concept of 'good vibes,' leaving behind a trail of positivity,",
        False), (
        '{0} Attempted to rob a rubber duck store, but their escape plan involved floating away in a giant rubber ducky,',
        False), (
        "{0} Attempted to rob a 'bad joke' stand, but all the jokes were so bad that they ran away instead,",
        False), (
        "In a lighthearted plot, {0} tried to steal all the 'lost socks' in town, leaving everyone puzzled,",
        False), (
        "{0} Attempted to rob a 'cheesy joke' competition, but the puns proved too much to handle,",
        False), (
        "{0} Successfully organized a 'silly string' heist, leaving the entire city covered in vibrant chaos,",
        True), (
        "In a quirky move, {0} attempted to steal a street musician's tambourine, but it ended up leading a parade,",
        False), (
        'In a mischievous twist, {0} tried to steal the spotlight at a comedy show, but became the punchline instead,',
        False), (
        "In a mischievous twist, {0} tried to steal the 'Recipe for Disaster,' but it was too complicated to follow,",
        False)]

adv_scenarios = [
    (
        "{0} bravely enters a dark cave, but is suddenly attacked by {1}! With determination and skill, {0} manages to defeat the fearsome creature and emerges victorious. The cave's walls tremble as the echoes of {0}'s triumph resound, and the air is thick with a sense of accomplishment and newfound strength.",
        True),
    (
        "While exploring a forgotten temple, {0} accidentally awakens {1}, an ancient guardian. A fierce battle ensues, leaving the temple in ruins and a sense of urgency to restore it before its mystical power is lost forever. With every clash of sword against stone, the temple's history seems to reverberate through time, leaving {0} to ponder the consequences of their actions.",
        False),
    (
        "In a mystical realm, {0} encounters a mischievous {1} who offers a riddle. Solving the riddle earns {0} a valuable reward, and the {1} disappears in a burst of laughter, leaving a trail of sparkles behind. As the trail fades, {0} reflects on the whimsical encounter and wonders about the secrets that lie hidden within the realm's enchanting boundaries.",
        True),
    (
        "{0} is transported to a magical land where {1}, a legendary and rare creature, challenges them to a duel. A clash of powers ensues as {0} fights valiantly, channeling their inner strength and determination to claim victory against all odds. The land itself seems to hold its breath as {0}'s actions shape the outcome of the battle, leaving behind an undeniable mark of heroism.",
        True),
    (
        "Amidst a haunted forest, {0} encounters an {1}. With bravery and skill, {0} banishes the malevolent spirit, bringing peace back to the land and earning the respect and gratitude of forest creatures who had long lived in fear. As sunlight filters through the once-dense canopy, {0} finds solace in knowing they've broken the chains of darkness that gripped the forest's heart.",
        True),
    (
        "{0} discovers an ancient prophecy involving {1}. Through unwavering courage and steadfast determination, {0} fulfills the prophecy, overcoming insurmountable challenges and ensuring a bright future for their realm. The wind seems to carry whispers of {0}'s tale across the lands, inspiring hope and igniting a fire of change that will be remembered for generations to come.",
        True),
    (
        "{0} stumbles upon an ancient forest where {1}, a guardian of nature, tests their bond with the land. Through feats of strength, wisdom, and humility, {0} earns the guardian's blessing and a deeper connection with the natural world.",
        True
    ),
    (
        "A legendary tournament is held in a distant realm, and {0} is invited to compete. Facing powerful opponents and enduring grueling challenges, {0} fights their way to the finals, where a showdown with {1} awaits.",
        True
    ),
    (
        "{0} discovers an abandoned observatory that once belonged to a renowned astronomer. Inside, they find a celestial map that leads to a constellation-linked quest. With each constellation they decipher, they uncover a piece of forgotten lore.",
        True
    ),
    (
        "In the heart of a desert, {0} uncovers an ancient temple dedicated to {1}, the God of Sandstorms. A trial of endurance and perseverance awaits them as they navigate treacherous sand dunes and face the wrath of the desert.",
        True
    ),
    (
        "A magical relic is said to grant the power to control time. {0} embarks on a journey to retrieve the relic from a hidden sanctuary. Guided by clues and ancient writings, they solve puzzles that challenge their intellect and wit.",
        True
    ),
    (
        "{0} receives a mysterious map from a stranger, leading them to an island shrouded in mist. On the island, they find {1}, a keeper of forgotten stories. To earn their respect, {0} must share a tale of their own that carries a lesson.",
        True
    ),
    (
        "An enchanted forest is in peril as {1} threatens to consume its magic. {0} must embark on a quest to restore balance by seeking the guidance of forest spirits and uncovering the secret to calming the raging elemental forces.",
        True
    ),
    (
        "{0} becomes entangled in a rivalry between two rival factions: one seeking to unlock the power of {1}, and the other striving to protect it. {0} must choose a side and navigate a complex web of alliances and betrayals.",
        True
    ), (
        "{0} stumbles upon an ancient ritual site where {1} is about to be summoned. With quick thinking and resourcefulness, {0} disrupts the ritual just in time, preventing a catastrophe and earning the gratitude of the spirits.",
        True
    ),
    (
        "The moon's glow reveals a hidden waterfall in the enchanted forest. As {0} approaches, {1} emerges from the water, offering a choice: share a secret to gain a treasure, or remain silent and face a challenge. {0} makes their decision, and the journey unfolds.",
        True
    ),
    (
        "A long-forgotten prophecy speaks of {0} as the chosen one to face {1}, a formidable foe threatening the realm. The encounter is epic and intense, leaving both sides exhausted. But in the end, it is {0} who emerges victorious, fulfilling their destiny.",
        True
    ),
    (
        "{0} enters a magical carnival that appears in the realm once a century. The carnival is a realm of illusions and enchantments. After navigating through a series of whimsical challenges, {0} wins a prize that holds a hidden power.",
        True
    ),
    (
        "A mysterious portal transports {0} to a realm of dreams, where reality shifts and twists. {1} is the guardian of this realm, and they challenge {0} to embrace the dreamlike nature and solve enigmatic puzzles to return home.",
        True
    ),
    (
        "{0} sails to a remote island where {1} is said to dwell. The island is shrouded in mist and mystery. {0} must decipher ancient runes and prove their respect for the island's spirits to be granted an audience with {1}.",
        True
    ),
    (
        "A celestial event causes stars to fall to the earth, each carrying a fragment of {1}. {0} embarks on a quest to collect these fragments, facing trials that test their courage, intelligence, and kindness.",
        True
    ),
    (
        "During a storm, {0} finds refuge in an abandoned castle. Within, they encounter {1}, a spirit cursed to wander. To break the curse, {0} must piece together the spirit's past and help them find closure.",
        True
    ),

    (
        "{0} bravely enters a dark cave, but is suddenly attacked by {1}! With determination and skill, {0} manages to defeat the fearsome creature and emerges victorious. The cave's walls tremble as the echoes of {0}'s triumph resound, and the air is thick with a sense of accomplishment and newfound strength.",
        True),
    (
        "While exploring a forgotten temple, {0} accidentally awakens {1}, an ancient guardian. A fierce battle ensues, leaving the temple in ruins and a sense of urgency to restore it before its mystical power is lost forever. With every clash of sword against stone, the temple's history seems to reverberate through time, leaving {0} to ponder the consequences of their actions.",
        False),
    (
        "In a mystical realm, {0} encounters a mischievous {1} who offers a riddle. Solving the riddle earns {0} a valuable reward, and the {1} disappears in a burst of laughter, leaving a trail of sparkles behind. As the trail fades, {0} reflects on the whimsical encounter and wonders about the secrets that lie hidden within the realm's enchanting boundaries.",
        True),
    (
        "{0} is transported to a magical land where {1}, a legendary and rare creature, challenges them to a duel. A clash of powers ensues as {0} fights valiantly, channeling their inner strength and determination to claim victory against all odds. The land itself seems to hold its breath as {0}'s actions shape the outcome of the battle, leaving behind an undeniable mark of heroism.",
        True),
    (
        "Amidst a haunted forest, {0} encounters an {1}. With bravery and skill, {0} banishes the malevolent spirit, bringing peace back to the land and earning the respect and gratitude of forest creatures who had long lived in fear. As sunlight filters through the once-dense canopy, {0} finds solace in knowing they've broken the chains of darkness that gripped the forest's heart.",
        True),
    (
        "{0} discovers an ancient prophecy involving {1}. Through unwavering courage and steadfast determination, {0} fulfills the prophecy, overcoming insurmountable challenges and ensuring a bright future for their realm. The wind seems to carry whispers of {0}'s tale across the lands, inspiring hope and igniting a fire of change that will be remembered for generations to come.",
        True),

    (
        "{0} discovers an ancient library guarded by {1}. They delve into its tomes and gain a wealth of knowledge, uncovering secrets that shape their destiny.",
        True),
    (
        "A sudden earthquake traps {0} in a cave with {1}. Working together, they find a way to escape, forging an unlikely bond in the process.",
        True),
    (
        "While crossing a rickety bridge, {0} encounters {1}, a mischievous trickster. A battle of wits ensues, leaving {0} questioning the nature of reality.",
        False),
    (
        "A long-lost artifact said to possess untold power lies within a treacherous maze. {0} navigates the labyrinth, but finds only disappointment as the artifact proves to be a myth.",
        False),
    (
        "{0} stumbles upon an ancient artifact that holds a curse. They must solve riddles and break a complex enchantment to free themselves from its grip.",
        True),
    (
        "In the heart of a snow-covered forest, {0} encounters {1}, a guardian of winter. They must prove their respect for nature before being granted a glimpse of the guardian's power.",
        True),
    (
        "A peculiar door appears in the midst of a meadow. {0} opens it and is transported to a realm of dreams, where they confront {1}'s illusions.",
        False),
    (
        "{0} is challenged to a friendly cooking contest by {1}, a culinary master. The dishes are exquisite, but ultimately, the competition ends in a draw.",
        False),
    (
        "A luminous comet passes overhead, and {0} follows its trail to discover a hidden grove. {1} appears, offering them a chance to make a wish.",
        True),
    (
        "{0} encounters a pack of wild creatures led by {1}. To earn their trust, {0} must navigate the delicate balance of nature and prove themselves as a friend, not a foe.",
        True),
    (
        "A celestial alignment reveals a secret portal. {0} enters and faces {1}, a cosmic guardian who tests their understanding of the universe's mysteries.",
        False),
    (
        "{0} stumbles upon an ancient puzzle that, when solved, opens a portal to a realm of forgotten legends. In this realm, they must choose between aiding {1} or pursuing their own desires.",
        True),
    (
        "A legend speaks of {0} as the hero who will tame {1}, a mythical beast of the skies. Through courage and compassion, they forge a bond that transcends species.",
        True),
    (
        "While exploring a cave system, {0} disturbs a nest of creatures, including {1}. They must navigate darkness and danger to escape the cavern's depths.",
        False),
    (
        "{0} finds themselves in a twisted mirror world where they encounter an alternate version of {1}. They must solve the mystery of this doppelgänger to restore balance.",
        True),
    (
        "The realm is plagued by an eternal winter caused by {1}. {0} embarks on a journey to end the curse, facing frosty landscapes and formidable ice guardians.",
        True),
    (
        "{0} becomes trapped in a labyrinth created by {1}, a trickster spirit. They must solve riddles to navigate the maze's shifting walls and escape its grasp.",
        False),
    (
        "A massive tree reveals itself as {1}, a guardian of nature. {0} must seek its wisdom to heal a blighted forest and prove their commitment to preservation.",
        True),
    (
        "In a forgotten ruin, {0} encounters a time-traveling artifact. They witness historical events involving {1} and must decide whether to alter the past.",
        False),
    (
        "{0} is chosen by the spirits to retrieve {1}, an elemental gem stolen by thieves. Their journey leads them through desolate deserts and treacherous mountains.",
        True),
    (
        "A mysterious rift opens, connecting {0}'s world to an alternate realm ruled by {1}. The two must collaborate to close the rift and restore balance.",
        False),
    (
        "A magical storm sweeps {0} to a realm where {1} reigns. They face elemental trials to prove their worthiness and return home with newfound power.",
        True),
    (
        "A forgotten prophecy tells of {0}'s encounter with {1}. The outcome shapes the balance between light and darkness, as well as their own path.",
        True),
    (
        "{0} discovers a hidden underwater cavern guarded by {1}. To earn passage through the cavern, they must solve riddles that test their mental agility.",
        True),
    (
        "During a lunar eclipse, {0} encounters {1}, a guardian of dreams. They journey through surreal landscapes and uncover hidden truths about themselves.",
        False),
    (
        "A mystical portal transports {0} to a realm where they must challenge {1} to a game of wit and strategy. The outcome determines their fate in the realm.",
        False),
    (
        "{0} encounters {1}, a reclusive sage known for their wisdom. To gain their guidance, {0} must solve riddles and answer thought-provoking questions.",
        True),
    (
        "A traveling carnival appears, led by {1}, the enigmatic ringmaster. {0} must navigate illusions and choose whether to pursue the carnival's mysteries.",
        False),
    (
        "In a city plagued by corruption, {0} teams up with {1}, a rogue thief seeking redemption. Together, they uncover a conspiracy that threatens the realm.",
        True),
    (
        "A sudden portal whisks {0} to an alternate dimension ruled by {1}. They must navigate this distorted realm to find a way back to their own world.",
        False),
    (
        "{0} encounters an ancient spirit of chaos, {1}, who offers them a choice: embrace chaos or restore balance to the realm.",
        True),
    (
        "A shimmering portal opens in the night sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    (
        "During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}, a cosmic guardian of wisdom.",
        True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy foretells {0}'s duel with {1}, a legendary warrior. Their clash of swords shapes the destiny of both the realm and their own.",
        True),
    (
        "During a meteor shower, {0} encounters {1}, a celestial being. They must decipher the language of the stars to earn the being's guidance.",
        False),
    (
        "A mysterious door appears in the midst of a dense forest. {0} opens it and enters a surreal realm where they must confront {1}'s illusions.",
        False),
    (
        "{0} receives an ancient map leading to a hidden island inhabited by {1}. They must solve riddles and navigate dangerous waters to find the island.",
        False),
    (
        "A cursed gem has transformed {1} into a monstrous creature. {0} embarks on a quest to break the curse and restore the gem's true power.",
        True),
    (
        "{0} discovers an abandoned laboratory where {1}, a scientist, once conducted experiments. They must solve puzzles to uncover the scientist's legacy.",
        True),
    (
        "During a celestial alignment, {0} encounters {1}, a guardian of starlight. They must prove their understanding of the cosmos to earn the guardian's blessing.",
        True),
    (
        "An enchanted forest reveals its mysteries to {0}, including a pact with {1}, the spirit of the land. Together, they restore balance to the realm.",
        True),
    (
        "{0} stumbles upon an ancient prophecy involving {1}. Through a series of trials, they determine whether the prophecy leads to glory or deception.",
        False),
    (
        "A hidden realm opens its doors to {0}, revealing a city shaped by {1}'s magic. They must navigate illusions and uncover the city's true nature.",
        True),
    (
        "{0} discovers a time-worn book containing the story of {1}, a forgotten hero. They must solve riddles to bring the hero's legacy to life once more.",
        False),
    (
        "A mysterious portal transports {0} to a realm of dreams, where they face {1}, the guardian of illusions. Their journey tests the boundaries of reality.",
        False),
    (
        "{0} receives a summons to a realm ruled by {1}, a monarch of shadows. To prove their worth, they must navigate a labyrinth of darkness and despair.",
        True),
    (
        "A legendary creature, {1}, is rumored to inhabit a secluded valley. {0} embarks on a journey to find the creature and learn its ancient wisdom.",
        True),
    (
        "{0} awakens in a realm between dreams and reality, where they encounter {1}, a guardian of the mind. They must face their inner fears to escape.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     ", a cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     ", a cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True),
    (
        "In the heart of a forgotten forest, {0} discovers an altar dedicated to {1}, the spirit of nature. They must prove their respect to gain its favor.",
        True),
    (
        "{0} stumbles upon an abandoned laboratory where {1}, a brilliant inventor, once created marvels. Solving puzzles unveils the inventor's legacy.",
        True),
    (
        "A labyrinthine cave system leads {0} to a hidden chamber, where they face {1}, a guardian of memories. Solving riddles triggers visions of the past.",
        False),
    (
        "{0} encounters a sentient forest, guided by {1}, the spirit of growth. They must navigate the forest's heart and earn the spirit's wisdom.",
        True),
    (
        "A secret society led by {1} offers {0} a choice: join their ranks and gain power, or defy them and face the consequences of their defiance.",
        False),
    (
        "During a solar eclipse, {0} is transported to a realm of shadows, where {1} challenges them to solve enigmatic puzzles and escape the darkness.",
        False),
    (
        "{0} finds an ancient map leading to a forgotten city where {1} is said to reside. They must navigate the city's maze-like streets and face trials.",
        True),
    (
        "A mysterious portal transports {0} to a realm where {1}, the keeper of dreams, tests their imagination and creativity through intricate puzzles.",
        True),
    (
        "{0} enters a realm of floating islands where they face {1}, a guardian of the skies. They must solve riddles to prove their aerial prowess.",
        False),
    (
        "A legendary artifact said to control the weather is rumored to be hidden in a thunderous realm. {0} faces lightning storms to uncover its secrets.",
        False),
    (
        "{0} discovers a hidden garden tended by {1}, the spirit of life. They must nurture the garden and prove their dedication to restoration.",
        True),
    (
        "In a mystical forest, {0} encounters {1}, a guardian of the wild. They must navigate the forest's trials and show their respect for its inhabitants.",
        True),
    (
        "{0} becomes trapped in an endless mirror maze created by {1}, a trickster spirit. They must solve riddles to escape its maze of illusions.",
        False),
    (
        "A prophecy speaks of {0}'s encounter with {1}, a figure cloaked in darkness. Their meeting shapes the fate of the realm and tests {0}'s resolve.",
        True),
    (
        "While exploring a hidden cave, {0} disturbs a colony of creatures, including {1}. They must find a way to escape the cave's depths and darkness.",
        False),
    (
        "{0} is chosen by the moon goddess to seek {1}, a guardian of lunar secrets. Their journey tests their intuition and affinity with the night sky.",
        True),
    (
        "A shimmering portal opens in the sky, revealing {1}'s realm. {0} enters, facing trials that test their resolve and challenge their perceptions.",
        False),
    (
        "The stars align, revealing a hidden path that leads {0} to a fabled city. Here, they face trials determined by {1}'s influence over the city's fate.",
        True),
    (
        "A forgotten prophecy speaks of {0} as the one who will unlock the power of {1}. Their journey is fraught with challenges, leading to an unexpected destiny.",
        True),
    (
        "An enchanted forest is plagued by a curse cast by {1}. {0} embarks on a quest to restore the forest's magic and break the curse's hold.",
        True),
    (
        "{0} comes across a hidden society led by {1}. To gain their trust, they must prove themselves through a series of trials and earn a place among the society.",
        True),
    (
        "A long-lost artifact said to grant wishes is rumored to be buried in a forgotten city. {0} embarks on a perilous journey to uncover the truth.",
        False),
    (
        "{0} is lured into a realm of illusions by {1}, a trickster spirit. They must outwit the spirit's deceptions to find their way back to reality.",
        False),
    ("During a celestial event, {0} is transported to a realm where they must solve puzzles created by {1}",
     " the cosmic guardian of wisdom.", True),
    (
        "{0} encounters a living embodiment of {1}, a creature of fire and lava. They must navigate an erupting volcano to gain its trust and knowledge.",
        True),
    (
        "An ancient curse has turned {1} into a fearsome beast. {0} must journey to a hidden temple and break the curse through a series of trials.",
        False),
    (
        "{0} finds a magical mirror that transports them to a parallel world. Here, they encounter {1}, a reflection that challenges their perceptions.",
        False),
    (
        "A relic that can shape reality is rumored to be hidden in a treacherous desert. {0} navigates the dunes and faces sandstorms to uncover its secrets.",
        False),
    (
        "While exploring a lost city, {0} awakens {1}, an ancient guardian. They must solve riddles and challenges to restore the guardian's power.",
        True),
    (
        "{0} receives a letter inviting them to a masquerade ball hosted by {1}, a enigmatic figure. At the ball, secrets and identities are revealed.",
        True),
    (
        "A rare celestial alignment opens a portal to {1}'s realm. {0} must solve riddles and decipher constellations to navigate this astral world.",
        False),
    (
        "{0} enters an abandoned alchemist's laboratory, awakening {1}, an experimental creation. They must find a way to free the creation from its chains.",
        False),
    (
        "In a land of eternal night, {0} encounters {1}, a guardian of shadows. They must prove their ability to blend into the darkness to earn the guardian's favor.",
        True),
    (
        "A hidden oasis holds the key to awakening {1}, a slumbering guardian of life. {0} must solve puzzles and nurture the land to restore its vitality.",
        True),
    (
        "{0} discovers a portal to a realm governed by {1}, the keeper of time. They must navigate past, present, and future challenges to prove their worth.",
        False),
    (
        "A forgotten prophecy reveals {0} as the one destined to confront {1}, an ancient force threatening the world's harmony. Their clash shapes the outcome.",
        True)
]

adv_success_strings = [
    "{0} discovers a treasure chest hidden beneath the ancient oak tree, filled with priceless artifacts and gems.",
    "{0} solves the mystery of the enchanted labyrinth and is rewarded with a legendary weapon of immense power.",
    "{0} wins the favor of the mystical spirits and is granted the ability to communicate with animals for a day.",
    "By outwitting the cunning {1}, {0} claims victory and earns a rare amulet with protective enchantments.",
    "{0} befriends a mischievous {1} who rewards their kindness with a map leading to a secret sanctuary.",
    "{0} uncovers a hidden library, where they find a book of forgotten spells that grant them newfound magic.",
    "{0} forges an unbreakable bond with the {1} they encounter, gaining a loyal companion for their journeys.",
    "In a dramatic duel, {0} defeats {1} and receives a mystical gem that enhances their natural abilities.",
    "{0} wins a contest of wits against a clever trickster, earning a cloak of invisibility as their prize.",
    "{0} proves their valor by facing down a fearsome beast, receiving a shield said to deflect even dragonfire.",
    "{0} discovers a forgotten shrine and proves their devotion, receiving a blessing that enhances their strength.",
    "{0} overcomes a series of trials set by ancient guardians, earning a medallion that grants them wisdom.",
    "{0} helps a group of forest creatures, and in return, they gift {0} with a magical amulet of protection.",
    "{0} aids a lost spirit in finding peace, and as gratitude, the spirit bestows them with ethereal wings.",
    "{0} unlocks the power of a hidden crystal, gaining the ability to manipulate the elements for a limited time.",
    "{0} assists a group of researchers in their quest, and they gift {0} with a charm that enhances their intellect.",
    "Through a series of challenges, {0} impresses the rulers of a mystical city and is granted their favor.",
    "{0} saves a celestial creature from a dire fate, and in gratitude, they receive a gift of starlit armor.",
    "{0} helps a cursed soul find redemption, and as a reward, they gain the power to heal wounds with a touch.",
    "{0} solves the riddles of a forgotten tomb, and their reward is a gem that grants them glimpses of the future.",
    "{0} restores balance to a sacred grove, earning the respect of ancient tree spirits and a druid's blessing.",
    "{0} befriends a reclusive sage and gains access to their knowledge, enhancing their understanding of the arcane.",
    "{0} shows exceptional empathy towards a lost spirit, and in return, they receive a necklace that grants visions.",
    "{0} aids a group of adventurers in a perilous quest, and they gift {0} with a pendant that boosts their courage.",
    "{0} outsmarts a cunning trickster, gaining a mystical mask that allows them to adopt different personas.",
    "{0} successfully navigates a series of traps in an ancient tomb and is rewarded with a gem of eternal life.",
]

adv_failure_strings = [
    "{0} underestimates the challenges posed by the treacherous terrain and returns empty-handed.",
    "Despite their efforts, {0} is unable to decipher the ancient riddle, missing out on the promised reward.",
    "{0}'s attempt to tame the wild {1} proves futile, leaving them without the desired connection to nature.",
    "The tricks of {1} prove too much for {0} to handle, and they leave the encounter without a prize.",
    "{0} fails to gain the trust of the forest spirits and misses the opportunity to learn their ancient secrets.",
    "{0} becomes lost in the mystical labyrinth, unable to reach the treasure rumored to be at its heart.",
    "The {1} that {0} encounters proves too powerful to defeat, and they retreat without the expected reward.",
    "{0} is unable to unlock the mysteries of an ancient relic, leaving its powers undiscovered.",
    "Despite their efforts, {0} is unable to solve the enigmatic puzzles set by the ancient guardians.",
    "{0}'s attempt to persuade a powerful entity ends in failure, leaving them without a promised boon.",
    "{0} faces the fearsome beast but is ultimately forced to retreat, missing out on the reward.",
    "The ancient forest's challenges prove too much for {0}, who leaves without the hoped-for prize.",
    "{0} is unable to complete the trials of the shrine, and the blessing remains out of their grasp.",
    "{0}'s attempt to aid the lost spirit falls short, leaving them without the ethereal wings.",
    "{0} is unable to harness the elemental crystal's power, and their attempts to manipulate the elements fail.",
    "Despite their best efforts, {0} is unable to aid the researchers and misses out on the gift of intellect.",
    "{0} impresses the rulers of the mystical city, but they ultimately choose another champion, leaving {0} empty-handed.",
    "{0} fails to save the celestial creature from its fate, and the gift of starlit armor remains unearned.",
    "{0}'s efforts to heal wounds with a touch are in vain, as the cursed soul remains unredeemed.",
    "{0} is unable to solve the tomb's riddles, and the gem that grants glimpses of the future remains out of reach.",
    "{0} is unable to restore balance to the sacred grove, and the druid's blessing remains beyond their grasp.",
    "{0} is unable to access the sage's knowledge, missing out on the enhancement of their understanding.",
    "{0}'s attempts to communicate with the lost spirit are in vain, and the necklace that grants visions eludes them.",
    "{0} is unable to aid the group of adventurers successfully, missing out on the pendant that boosts courage.",
    "{0} falls victim to the trickster's cunning, and the mystical mask that changes personas remains unclaimed.",
    "{0} is caught by the traps in the ancient tomb and fails to obtain the gem of eternal life.",
]
