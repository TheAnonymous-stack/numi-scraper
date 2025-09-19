import json
import random
import copy

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_18_E3
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_18_E3':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_18_E3")

# Need to generate 49 variations (51 total - 2 templates = 49)
variations = []

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate least common multiple"""
    return abs(a * b) // gcd(a, b)

def get_factors(n):
    """Get all factors of n"""
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

# Pop culture themes for GCF problems (distributing items evenly)
gcf_themes = [
    ("preparing for the Chunin exams", "Naruto", "kunai", "shuriken"),
    ("setting up for a Quidditch match", "Harry", "Quaffles", "Bludgers"),
    ("organizing the Avengers training", "Tony", "repulsor units", "arc reactors"),
    ("preparing Pokemon battles", "Ash", "Pokeballs", "potions"),
    ("setting up Jedi training", "Luke", "lightsabers", "training remotes"),
    ("organizing Survey Corps equipment", "Levi", "blades", "gas canisters"),
    ("preparing for UA Sports Festival", "Deku", "headbands", "point cards"),
    ("setting up Demon Slayer training", "Tanjiro", "wooden swords", "breathing masks"),
    ("organizing Soul Reaper stations", "Ichigo", "spirit ribbons", "soul candy"),
    ("preparing Fairy Tail guild hall", "Natsu", "job requests", "magic lacrimas"),
    ("setting up One Piece crew supplies", "Luffy", "meat portions", "cola bottles"),
    ("organizing Jujutsu High training", "Gojo", "cursed tools", "talismans"),
    ("preparing Hunter exam stations", "Gon", "badges", "maps"),
    ("setting up Black Clover grimoire ceremony", "Asta", "grimoires", "magic stones"),
    ("organizing Death Note investigation", "L", "evidence folders", "surveillance cameras"),
    ("preparing Attack on Titan gear check", "Eren", "gear sets", "spare blades"),
    ("setting up My Hero Academia rescue training", "All Might", "rescue mannequins", "first aid kits"),
    ("organizing Spirited Away bathhouse", "Chihiro", "bath tokens", "herbal soaps"),
    ("preparing Studio Ghibli festival", "Totoro", "acorns", "umbrellas"),
    ("setting up Fullmetal Alchemist lab", "Edward", "transmutation circles", "research notes"),
    ("organizing Cowboy Bebop bounties", "Spike", "bounty posters", "tracking devices"),
    ("preparing Code Geass strategy room", "Lelouch", "chess pieces", "battle maps"),
    ("setting up Steins;Gate lab", "Okabe", "phone microwave parts", "bananas"),
    ("organizing Tokyo Ghoul cafe", "Kaneki", "coffee cups", "sugar cubes"),
    ("preparing Mob Psycho office", "Mob", "spirit tags", "salt packets")
]

# Pop culture themes for LCM problems (scheduling/grouping)
lcm_themes = [
    ("Konoha Ninja Academy", "training sessions", "genin", "chunin"),
    ("Hogwarts School", "Defence Against Dark Arts classes", "Gryffindors", "Slytherins"),
    ("Xavier's School", "Danger Room sessions", "X-Men trainees", "junior mutants"),
    ("Pokemon Center", "healing appointments", "regular Pokemon", "legendary Pokemon"),
    ("Jedi Temple", "meditation sessions", "Padawans", "Knights"),
    ("Survey Corps HQ", "expedition briefings", "new recruits", "veterans"),
    ("UA High School", "hero training", "Class 1-A students", "Class 1-B students"),
    ("Demon Slayer Corps", "breathing technique practice", "Mizunoto rank", "Kinoe rank"),
    ("Soul Society", "kido training", "academy students", "seated officers"),
    ("Fairy Tail Guild", "job assignments", "S-Class wizards", "regular members"),
    ("Thousand Sunny", "watch duties", "Straw Hat crew", "guest pirates"),
    ("Jujutsu High", "curse exorcism practice", "first years", "second years"),
    ("Hunter Association", "license renewals", "rookie hunters", "veteran hunters"),
    ("Clover Kingdom", "magic knight trials", "commoners", "nobles"),
    ("Task Force HQ", "Kira investigation meetings", "detectives", "analysts"),
    ("Scout Regiment", "wall patrol shifts", "inner wall guards", "outer wall guards"),
    ("Hero Agency", "patrol schedules", "sidekicks", "pro heroes"),
    ("Bathhouse", "spirit customer slots", "river spirits", "radish spirits"),
    ("Central Command", "alchemy evaluations", "state alchemists", "research alchemists"),
    ("Bebop Ship", "bounty hunting shifts", "main crew", "Ein's walk times"),
    ("Black Knights HQ", "strategy meetings", "commanders", "soldiers"),
    ("Future Gadget Lab", "time leap experiments", "lab members", "assistants"),
    ("Anteiku Cafe", "ghoul meetings", "regular ghouls", "one-eyed ghouls"),
    ("Spirits and Such", "exorcism appointments", "weak spirits", "strong spirits"),
    ("Death Weapon Academy", "soul resonance training", "meisters", "weapons")
]

# Generate GCF variations (25 based on template 1)
for i in range(25):
    template = copy.deepcopy(templates[0])
    theme = random.choice(gcf_themes)

    # Generate numbers with interesting GCF
    gcf = random.randint(3, 12)
    mult1 = random.randint(2, 6)
    mult2 = random.randint(3, 7)
    if mult1 == mult2:
        mult2 += 1

    item1_count = gcf * mult1
    item2_count = gcf * mult2

    # Update question
    template['question_number'] = f"3_{i + 3}"
    template['question_text'] = f"In {theme[0]}, {theme[1]} is setting up some stations where people can practice. They have {item1_count} {theme[2]} and {item2_count} {theme[3]}, which they want to distribute evenly among the training stations with none left over. \n\nWhat is the greatest number of training stations that {theme[1]} can set up?\n\n"

    # Update correct answer
    template['correct_answers'] = [str(gcf)]

    # Get factors
    factors1 = get_factors(item1_count)
    factors2 = get_factors(item2_count)

    # Update solution
    template['solution'][0][1] = f"{theme[1]} wants to divide {item1_count} {theme[2]} and {item2_count} {theme[3]} into equal groups with no extras."
    template['solution'][1][1] = f"We need to find the greatest number that can divide both {item1_count} and {item2_count} evenly."
    template['solution'][2][1] = f"The factors of {item1_count} are: {', '.join(map(str, factors1))}."
    template['solution'][3][1] = f"The factors of {item2_count} are: {', '.join(map(str, factors2))}."
    template['solution'][4][1] = f"The greatest common factor is {gcf}. That means {theme[1]} can make {gcf} training stations."
    template['solution'][5][1] = f"Each station would have {item1_count // gcf} {theme[2]} and {item2_count // gcf} {theme[3]}. So, the greatest number of stations is {gcf}."

    variations.append(template)

# Generate LCM variations (24 based on template 2)
for i in range(24):
    template = copy.deepcopy(templates[1])
    theme = random.choice(lcm_themes)

    # Generate group sizes
    group1 = random.randint(2, 8)
    group2 = random.randint(3, 12)
    if group2 == group1:
        group2 += 2

    result_lcm = lcm(group1, group2)

    # Update question
    template['question_number'] = f"3_{i + 28}"
    template['question_text'] = f"Over the next two days, {theme[0]} is conducting {theme[1]}. On the first day, they plan to train {theme[2]} in groups of {group1}. On the second day, they will train {theme[3]} in groups of {group2}. If the school will have the same total number of participants on each day, what is the smallest number of participants that could attend each day?\n"

    # Update correct answer
    template['correct_answers'] = [str(result_lcm)]

    # Generate multiples
    multiples1 = [group1 * j for j in range(1, min(8, result_lcm // group1 + 2))]
    multiples2 = [group2 * j for j in range(1, min(8, result_lcm // group2 + 2))]

    # Update solution
    template['solution'][0][1] = f"The {theme[0]} plans to train participants in groups of {group1} on the first day and in groups of {group2} on the second day."
    template['solution'][1][1] = f"We are told the number of participants each day must be the same. So, we need to find the smallest number that both {group1} and {group2} can divide into evenly."
    template['solution'][2][1] = f"The multiples of {group1} are: {', '.join(map(str, multiples1))}..."
    template['solution'][3][1] = f"The multiples of {group2} are: {', '.join(map(str, multiples2))}..."
    template['solution'][4][1] = f"The least common multiple (LCM) of {group1} and {group2} is {result_lcm}. That means {result_lcm} is the smallest number of participants that works for both grouping methods."
    template['solution'][5][1] = f"So, the smallest number of participants that could attend each day is {result_lcm}."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_18_E3 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_18_E3")
print("Saved to 'Gr7_18_E3 variations.json'")