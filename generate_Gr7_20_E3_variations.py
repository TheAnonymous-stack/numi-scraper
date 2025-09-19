import json
import random
import copy
from math import gcd

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_20_E3
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_20_E3':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_20_E3")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

# Pop culture themes for fraction word problems
themes = [
    ("Konoha Ninja Academy", "practice jutsu", "use Shadow Clone technique"),
    ("Hogwarts", "study magic", "practice Patronus charms"),
    ("UA High School", "attend hero training", "have quirk practice"),
    ("Xavier's School", "take classes", "train in the Danger Room"),
    ("Jedi Temple", "attend training", "practice lightsaber forms"),
    ("Survey Corps Training", "complete exercises", "practice with ODM gear"),
    ("Demon Slayer Corps", "train", "practice Total Concentration Breathing"),
    ("Soul Society Academy", "study", "practice kido spells"),
    ("Fairy Tail Guild", "take jobs", "use dragon slayer magic"),
    ("Marine Headquarters", "train", "practice Haki"),
    ("Jujutsu High", "attend class", "practice curse techniques"),
    ("Hunter Association", "take the exam", "pass the final phase"),
    ("Black Bulls Squad", "go on missions", "use anti-magic"),
    ("Death Weapon Academy", "attend class", "achieve soul resonance"),
    ("Alchemist Military", "serve", "perform human transmutation"),
    ("Bebop Crew", "take bounties", "capture alive"),
    ("Black Knights", "join operations", "pilot Knightmares"),
    ("Future Gadget Lab", "conduct experiments", "achieve time travel"),
    ("CCG Investigators", "go on raids", "encounter SSS-rated ghouls"),
    ("Spirits and Such Office", "handle cases", "deal with evil spirits"),
    ("Pokemon Trainers", "battle", "use legendary Pokemon"),
    ("Avengers", "go on missions", "face cosmic threats"),
    ("X-Men", "join missions", "encounter Sentinels"),
    ("Justice League", "respond to alerts", "face Darkseid's forces"),
    ("Straw Hat Pirates", "sail the Grand Line", "find Devil Fruits")
]

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])
    theme = random.choice(themes)

    # Generate fractions
    if i < 20:
        # Simple unit fractions
        denom1 = random.randint(2, 6)
        denom2 = random.randint(2, 6)
        num1 = 1
        num2 = 1
    elif i < 35:
        # Small fractions
        denom1 = random.randint(3, 8)
        denom2 = random.randint(3, 8)
        num1 = random.randint(1, min(3, denom1 - 1))
        num2 = random.randint(1, min(3, denom2 - 1))
    else:
        # Larger fractions
        denom1 = random.randint(5, 12)
        denom2 = random.randint(5, 12)
        num1 = random.randint(1, min(5, denom1 - 1))
        num2 = random.randint(1, min(5, denom2 - 1))

    # Ensure not same as original
    if num1 == 1 and denom1 == 4 and num2 == 1 and denom2 == 3:
        denom1 = 5

    # Calculate result
    result_num = num1 * num2
    result_denom = denom1 * denom2

    # Simplify
    g = gcd(result_num, result_denom)
    simplified_num = result_num // g
    simplified_denom = result_denom // g

    # Update question
    template['question_number'] = f"3_{i + 2}"
    template['question_text'] = f"At {theme[0]}, $\\frac{{{num1}}}{{{denom1}}}$ of the students {theme[1]}. Of the students who {theme[1]}, $\\frac{{{num2}}}{{{denom2}}}$ {theme[2]}.\n\nWhat fraction of the students at {theme[0]} {theme[2]}?\n\nWrite your answer as a fraction or as a whole or mixed number.\n\n"

    # Update correct answer
    template['correct_answers'] = [f"{simplified_num}/{simplified_denom}"]

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for idx, step in enumerate(template['solution_image_tag']):
            if len(step) > 1:
                if idx == 0:
                    step[1] = f"Gr7_20_3_{i + 2}_step_2"
                    step[2] = f"Shows the multiplication of two fractions: {num1}/{denom1} x {num2}/{denom2}. The calculation is set up to multiply numerators and denominators separately."
                elif idx == 1:
                    step[1] = f"Gr7_20_3_{i + 2}_step_4"
                    step[2] = f"Shows the complete calculation: {num1}/{denom1} x {num2}/{denom2} = ({num1} x {num2})/({denom1} x {denom2}) = {result_num}/{result_denom}"

                    if g > 1:
                        step[2] += f" = {simplified_num}/{simplified_denom}. The fraction is simplified by dividing both by {g}."

    # Update solution
    template['solution'][0][1] = f"We are trying to find what fraction of all students {theme[2]}."
    template['solution'][1][1] = f"We know that $\\frac{{{num1}}}{{{denom1}}}$ of the students {theme[1]}, and $\\frac{{{num2}}}{{{denom2}}}$ of those students {theme[2]}. So we multiply the two fractions.\n"
    template['solution'][2][1] = f"First, multiply the numerators.\n{num1} x {num2} = {result_num}"
    template['solution'][3][1] = f"Now multiply the denominators.\n{denom1} x {denom2} = {result_denom}\n"

    if g > 1:
        template['solution'][4][1] = f"This gives us $\\frac{{{result_num}}}{{{result_denom}}}$, which simplifies to $\\frac{{{simplified_num}}}{{{simplified_denom}}}$.\n\nSo $\\frac{{{simplified_num}}}{{{simplified_denom}}}$ of the students at {theme[0]} {theme[2]}."
    else:
        template['solution'][4][1] = f"This means $\\frac{{{simplified_num}}}{{{simplified_denom}}}$ of the students at {theme[0]} {theme[2]}."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_20_E3 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_20_E3")
print("Saved to 'Gr7_20_E3 variations.json'")