import json
import random
import copy

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_17_E2
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_17_E2':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_17_E2")

# Need to generate 49 variations (51 total - 2 templates = 49)
variations = []

# Pop culture themes for word problems
themes = [
    ("The Pokémon Center", "Poké Balls", "Great Balls"),
    ("Hogwarts Express", "chocolate frogs", "pumpkin pasties"),
    ("The Shire Bakery", "lembas bread", "honey cakes"),
    ("Stark Industries", "arc reactors", "repulsor arrays"),
    ("The TARDIS Café", "jelly babies", "fish fingers and custard"),
    ("Konoha Ramen Shop", "miso ramen bowls", "tonkotsu ramen bowls"),
    ("Springfield Nuclear Plant", "donuts", "Duff beers"),
    ("Central Perk", "cappuccinos", "lattes"),
    ("The Krusty Krab", "Krabby Patties", "Kelp Shakes"),
    ("Wayne Enterprises", "Batarangs", "smoke pellets"),
    ("Capsule Corp", "senzu beans", "capsules"),
    ("The Death Star Cantina", "blue milk", "green milk"),
    ("Avengers Tower", "shawarmas", "coffee"),
    ("Studio Ghibli Café", "totoro cookies", "catbus cakes"),
    ("The Three Broomsticks", "butterbeers", "firewhiskeys"),
    ("Demon Slayer Corps", "rice balls", "tempura bowls"),
    ("UA High School Cafeteria", "katsudon bowls", "cold soba"),
    ("Survey Corps Supply", "bread rations", "meat rations"),
    ("One Piece Galley", "meat portions", "sake barrels"),
    ("Soul Society Tea House", "green tea", "rice wine"),
    ("Jujutsu High", "mochi boxes", "dango skewers"),
    ("Tanjiro's Bakery", "charcoal bread", "sweet buns"),
    ("Midoriya's Diner", "hero sandwiches", "power smoothies"),
    ("Fairy Tail Guild Hall", "magic potions", "energy drinks"),
    ("Black Clover Tavern", "grimoire cookies", "mana cakes")
]

travel_themes = [
    ("Goku's", "instant transmission", "Nimbus cloud ride"),
    ("Hermione's", "Floo Network travel", "Apparition"),
    ("Spider-Man's", "web-swinging", "subway ride"),
    ("The Flash's", "speed force run", "normal jog"),
    ("Iron Man's", "suit flight", "car drive"),
    ("Doctor Strange's", "portal travel", "walk"),
    ("Naruto's", "shadow clone running", "regular running"),
    ("Luffy's", "Gear Second dash", "normal walk"),
    ("Saitama's", "serious series jump", "casual stroll"),
    ("Eren's", "ODM gear travel", "horseback ride"),
    ("Deku's", "One For All jump", "regular sprint"),
    ("Tanjiro's", "Total Concentration breathing run", "normal pace"),
    ("Gojo's", "teleportation", "casual walk"),
    ("Levi's", "ODM gear swing", "horse ride"),
    ("Ichigo's", "flash step", "normal run")
]

# Generate variations for addition word problems (based on template 1)
for i in range(25):
    template = copy.deepcopy(templates[0])
    theme = random.choice(themes)

    # Generate random mixed numbers
    denom = random.randint(3, 8)
    whole1 = random.randint(3, 10)
    num1 = random.randint(1, denom - 1)
    whole2 = random.randint(1, 8)
    num2 = random.randint(1, denom - 1)

    # Calculate result
    total_num = num1 + num2
    total_whole = whole1 + whole2

    if total_num >= denom:
        extra_whole = total_num // denom
        total_whole += extra_whole
        total_num = total_num % denom

    # Update question
    template['question_number'] = f"1_{i + 3}"
    template['question_text'] = f"Yesterday, {theme[0]} sold {whole1} $\\frac{{{num1}}}{{{denom}}}$ {theme[1]} and {whole2} $\\frac{{{num2}}}{{{denom}}}$ {theme[2]}. How many items did they sell in all?\n\nWrite your answer as a fraction or as a whole or mixed number.\n\n"

    # Update correct answers
    from math import gcd
    g = gcd(total_num, denom) if total_num > 0 else 1

    if total_num == 0:
        template['correct_answers'] = [[str(total_whole)], [f"{total_whole * denom}/{denom}"]]
    else:
        simplified_num = total_num // g
        simplified_denom = denom // g
        answers = []

        if simplified_denom == 1:
            answers.append([str(total_whole + simplified_num)])
        else:
            answers.append([f"{total_whole} {simplified_num}/{simplified_denom}"])
            answers.append([f"{(total_whole * denom + total_num)}/{denom}"])

            # Add non-simplified version if different
            if g > 1:
                answers.append([f"{(total_whole * simplified_denom + simplified_num)}/{simplified_denom}"])
                answers.append([f"{total_whole} {total_num}/{denom}"])

        template['correct_answers'] = answers

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_17_2_{i + 3}_step_{step[0].split('/')[0]}"

    # Update solution
    template['solution'][0][1] = f"Find total number of items by adding {whole1} $\\frac{{{num1}}}{{{denom}}}$ and {whole2} $\\frac{{{num2}}}{{{denom}}}$."
    template['solution'][1][1] = f"First, add the whole numbers: {whole1} + {whole2} = {whole1 + whole2}."
    template['solution'][2][1] = f"Next, add the fractions: $\\frac{{{num1}}}{{{denom}}} + \\frac{{{num2}}}{{{denom}}} = \\frac{{{num1 + num2}}}{{{denom}}}$. Putting this together, we have:\n"

    if total_num > 0 and g > 1:
        template['solution'][3][1] = f"Now simplify the fraction by dividing the numerator and denominator by {g}:\n"
        template['solution'][4][1] = f"So, a total of {total_whole} $\\frac{{{total_num // g}}}{{{denom // g}}}$ items were sold."
    else:
        template['solution'][3][1] = f"The fraction is already in simplest form.\n"
        template['solution'][4][1] = f"So, a total of {total_whole} $\\frac{{{total_num}}}{{{denom}}}$ items were sold."

    variations.append(template)

# Generate variations for subtraction word problems (based on template 2)
for i in range(24):
    template = copy.deepcopy(templates[1])
    theme = random.choice(travel_themes)

    # Generate random mixed numbers (ensure first > second)
    denom = random.randint(3, 8)
    whole1 = random.randint(8, 15)
    num1 = random.randint(1, denom - 1)
    whole2 = random.randint(3, min(whole1 - 2, 10))
    num2 = random.randint(1, denom - 1)

    # Calculate result
    if num1 >= num2:
        result_whole = whole1 - whole2
        result_num = num1 - num2
    else:
        result_whole = whole1 - whole2 - 1
        result_num = num1 + denom - num2

    # Update question
    template['question_number'] = f"2_{i + 3}"
    template['question_text'] = f"{theme[0]} {theme[1]} takes {whole1} $\\frac{{{num1}}}{{{denom}}}$ hours, whereas {theme[0]} {theme[2]} takes {whole2} $\\frac{{{num2}}}{{{denom}}}$ hours. How much longer is the {theme[1]} than the {theme[2]}?\n\nWrite your answer as a fraction or as a whole or mixed number.\n\n"

    # Update correct answers
    from math import gcd
    g = gcd(result_num, denom) if result_num > 0 else 1

    if result_num == 0:
        template['correct_answers'] = [[str(result_whole)]]
    else:
        simplified_num = result_num // g
        simplified_denom = denom // g

        if simplified_denom == 1:
            template['correct_answers'] = [[str(result_whole + simplified_num)]]
        else:
            template['correct_answers'] = [
                [f"{result_whole} {simplified_num}/{simplified_denom}"],
                [f"{(result_whole * denom + result_num)}/{denom}"]
            ]

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_17_2_{25 + i + 3}_step_{step[0].split('/')[0]}"

    # Update solution
    template['solution'][0][1] = f"To find how much longer {theme[0]} {theme[1]} is, subtract the {theme[2]} time from the {theme[1]} time."

    if num1 >= num2:
        template['solution'][1][1] = f"Subtract the whole numbers from whole numbers and fractions from fractions.\n\n{whole1} - {whole2} = {result_whole}\n\n$\\frac{{{num1}}}{{{denom}}} - \\frac{{{num2}}}{{{denom}}} = \\frac{{{result_num}}}{{{denom}}}$"
    else:
        template['solution'][1][1] = f"We can't subtract $\\frac{{{num2}}}{{{denom}}}$ from $\\frac{{{num1}}}{{{denom}}}$, so we need to borrow.\n\n{whole1} $\\frac{{{num1}}}{{{denom}}}$ = {whole1 - 1} $\\frac{{{num1 + denom}}}{{{denom}}}$\n\nNow: {whole1 - 1} - {whole2} = {result_whole}\n\n$\\frac{{{num1 + denom}}}{{{denom}}} - \\frac{{{num2}}}{{{denom}}} = \\frac{{{result_num}}}{{{denom}}}$"

    if result_num > 0 and g > 1:
        template['solution'][2][1] = f"Now simplify the fraction by dividing the numerator and denominator by {g}:\n"
        template['solution'][3][1] = f"{theme[0]} {theme[1]} is {result_whole} $\\frac{{{result_num // g}}}{{{denom // g}}}$ hours longer than the {theme[2]}:\n"
    else:
        template['solution'][2][1] = f"The fraction is already in simplest form:\n"
        template['solution'][3][1] = f"{theme[0]} {theme[1]} is {result_whole} $\\frac{{{result_num}}}{{{denom}}}$ hours longer than the {theme[2]}:\n"

    variations.append(template)

# Save variations to JSON file
with open('Gr7_17_E2 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_17_E2")
print("Saved to 'Gr7_17_E2 variations.json'")