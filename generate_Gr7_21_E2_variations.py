import json
import random
import copy
from math import gcd

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_21_E2
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_21_E2':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_21_E2")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

# Pop culture themed recipes
recipes = [
    ("Hermione's", "Polyjuice potion", "lacewing flies"),
    ("Senzu Bean", "energy bars", "healing herbs"),
    ("Krabby Patty", "secret formula", "jellyfish jelly"),
    ("Ramen Ichiraku's", "special miso ramen", "secret sauce"),
    ("Willy Wonka's", "Everlasting Gobstopper", "flavor crystals"),
    ("Studio Ghibli's", "Totoro cookies", "magical flour"),
    ("Hogwarts'", "Butterbeer recipe", "butterscotch"),
    ("Tanjiro's", "charcoal bread", "special yeast"),
    ("Sanji's", "All Blue seafood stew", "mystery spice"),
    ("Gordon Ramsay's", "beef wellington", "truffle paste"),
    ("SpongeBob's", "Pretty Patty", "food coloring"),
    ("Shokugeki's", "transforming furikake", "umami powder"),
    ("Toriko's", "Century Soup", "rare ingredients"),
    ("Brock's", "Pokemon food", "berries"),
    ("Ignis'", "Ebony coffee", "special beans"),
    ("Link's", "Hearty Elixir", "fairy dust"),
    ("Mario's", "Super Mushroom soup", "power-up spores"),
    ("Kirby's", "Maximum Tomato salad", "dream fruit"),
    ("Cooking Mama's", "perfect cake", "vanilla extract"),
    ("Gordon's", "idiot sandwich", "disappointment sauce"),
    ("Salt Bae's", "golden steak", "special salt"),
    ("Uncle Iroh's", "jasmine tea", "tea leaves"),
    ("Soma's", "transforming rice", "special vinegar"),
    ("Remy's", "ratatouille", "fresh herbs"),
    ("Swedish Chef's", "bork bork special", "mystery meat")
]

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])
    recipe = random.choice(recipes)

    # Generate amount and fraction
    if i < 20:
        # Smaller whole numbers and simple fractions
        whole_amount = random.randint(2, 5)
        frac_num = random.randint(1, 4)
        frac_denom = random.randint(2, 5)
    elif i < 35:
        # Medium amounts
        whole_amount = random.randint(3, 8)
        frac_num = random.randint(1, 7)
        frac_denom = random.randint(3, 8)
    else:
        # Larger amounts
        whole_amount = random.randint(4, 12)
        frac_num = random.randint(2, 9)
        frac_denom = random.randint(4, 10)

    # Ensure proper fraction for batch fraction
    if frac_num >= frac_denom:
        frac_num = frac_denom - 1

    # Avoid the original
    if whole_amount == 3 and frac_num == 4 and frac_denom == 5:
        whole_amount = 4

    # Calculate result
    # Convert whole number to fraction
    whole_as_frac_num = whole_amount
    whole_as_frac_denom = 1

    # Multiply: (whole_amount/1) × (frac_num/frac_denom)
    result_num = whole_as_frac_num * frac_num
    result_denom = whole_as_frac_denom * frac_denom

    # Simplify
    g = gcd(result_num, result_denom)
    simplified_num = result_num // g
    simplified_denom = result_denom // g

    # Convert to mixed number if needed
    if simplified_num >= simplified_denom:
        result_whole = simplified_num // simplified_denom
        result_remainder = simplified_num % simplified_denom
    else:
        result_whole = 0
        result_remainder = simplified_num

    # Update question
    template['question_number'] = f"2_{i + 2}"
    template['question_text'] = f"{recipe[0]} {recipe[1]} recipe calls for {whole_amount} cups of {recipe[2]}.\n\nHow much {recipe[2]} would be needed to make $\\frac{{{frac_num}}}{{{frac_denom}}}$ of a batch of {recipe[1]}?\n\nWrite your answer as a fraction or as a whole or mixed number.\n"

    # Update correct answers
    if result_remainder == 0:
        template['correct_answers'] = [[str(result_whole)], [f"{simplified_num}/{simplified_denom}"]]
    else:
        if result_whole == 0:
            template['correct_answers'] = [[f"{result_remainder}/{simplified_denom}"], [f"{result_num}/{result_denom}"]]
        else:
            template['correct_answers'] = [
                [f"{result_whole} {result_remainder}/{simplified_denom}"],
                [f"{simplified_num}/{simplified_denom}"]
            ]

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for idx, step in enumerate(template['solution_image_tag']):
            if len(step) > 1:
                if idx == 0:
                    step[1] = f"Gr7_21_2_{i + 2}_step_1"
                    step[2] = f"Shows the multiplication setup: {whole_amount} x {frac_num}/{frac_denom}. The whole number {whole_amount} is to be multiplied by the fraction {frac_num}/{frac_denom}."
                elif idx == 1:
                    step[1] = f"Gr7_21_2_{i + 2}_step_2"
                    step[2] = f"Shows converting {whole_amount} to a fraction: {whole_amount} = {whole_amount}/1. This allows the multiplication to be performed as fraction x fraction."
                elif idx == 2:
                    step[1] = f"Gr7_21_2_{i + 2}_step_3"
                    step[2] = f"Shows the multiplication: {whole_amount}/1 x {frac_num}/{frac_denom} = ({whole_amount} x {frac_num})/(1 x {frac_denom}) = {result_num}/{result_denom}."
                elif idx == 3:
                    step[1] = f"Gr7_21_2_{i + 2}_step_5"
                    if result_whole > 0:
                        step[2] = f"Shows the conversion to a mixed number: {result_num}/{result_denom} = {result_whole} {result_remainder}/{simplified_denom}. Since {simplified_num} ÷ {simplified_denom} = {result_whole} remainder {result_remainder}."
                    else:
                        step[2] = f"Shows the final answer: {result_num}/{result_denom} = {result_remainder}/{simplified_denom} cups of {recipe[2]}."

    # Update solution
    template['solution'][0][1] = f"To find out how much {recipe[2]} is needed for $\\frac{{{frac_num}}}{{{frac_denom}}}$ of a batch, multiply:\n"
    template['solution'][1][1] = f"Write {whole_amount} as a fraction:\n"
    template['solution'][2][1] = "Multiply the numerators and multiply the denominators:\n"

    if result_whole > 0:
        template['solution'][3][1] = f"You would need $\\frac{{{result_num}}}{{{result_denom}}}$ cups of {recipe[2]}."
        template['solution'][4][1] = "This can also be expressed as mixed number.\n"
    else:
        template['solution'][3][1] = f"You would need $\\frac{{{result_num}}}{{{result_denom}}}$ cups of {recipe[2]}."

        if g > 1:
            template['solution'][4][1] = f"Simplifying: $\\frac{{{result_num}}}{{{result_denom}}} = \\frac{{{result_remainder}}}{{{simplified_denom}}}$ cups.\n"
        else:
            template['solution'][4][1] = f"So you need $\\frac{{{result_remainder}}}{{{simplified_denom}}}$ cups of {recipe[2]}.\n"

    variations.append(template)

# Save variations to JSON file
with open('Gr7_21_E2 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_21_E2")
print("Saved to 'Gr7_21_E2 variations.json'")