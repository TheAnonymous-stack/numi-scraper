import json
import random
import copy
from math import gcd

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_20_E2
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_20_E2':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_20_E2")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])

    # Generate two fractions
    if i < 20:
        # Simple unit fractions
        num1 = 1
        num2 = 1
        denom1 = random.randint(2, 10)
        denom2 = random.randint(2, 10)
        # Avoid the original
        if denom1 == 5 and denom2 == 4:
            denom1 = 3
    elif i < 35:
        # Small numerators
        num1 = random.randint(1, 4)
        num2 = random.randint(1, 4)
        denom1 = random.randint(3, 12)
        denom2 = random.randint(3, 12)
    else:
        # Larger fractions
        num1 = random.randint(1, 8)
        num2 = random.randint(1, 8)
        denom1 = random.randint(5, 15)
        denom2 = random.randint(5, 15)

    # Calculate result
    result_num = num1 * num2
    result_denom = denom1 * denom2

    # Simplify
    g = gcd(result_num, result_denom)
    simplified_num = result_num // g
    simplified_denom = result_denom // g

    # Update question
    template['question_number'] = f"2_{i + 2}"
    template['image_tag'] = f"Gr7_20_2_{i + 2}"
    template['backend_description'] = f"Shows the multiplication problem {num1}/{denom1} x {num2}/{denom2} with an empty box for the answer."

    # Update correct answer
    template['correct_answers'] = [f"{simplified_num}/{simplified_denom}"]

    # Update solution image tag
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_20_2_{i + 2}_step_3"
                step[2] = f"Shows the complete multiplication: ({num1} x {num2})/({denom1} x {denom2}) = {result_num}/{result_denom}"

                if g > 1:
                    step[2] += f" = {simplified_num}/{simplified_denom}. The fraction is simplified by dividing both numerator and denominator by {g}."
                else:
                    step[2] += f". The fraction is already in simplest form."

    # Update solution
    template['solution'][0][1] = f"We are multiplying two fractions.\n$\\frac{{{num1}}}{{{denom1}}} x \\frac{{{num2}}}{{{denom2}}}$"
    template['solution'][1][1] = f"First, multiply the numerators.\n{num1} x {num2} = {result_num}"
    template['solution'][2][1] = f"Now multiply the denominators:\n{denom1} x {denom2} = {result_denom}\n"

    if g > 1:
        template['solution'][3][1] = f"So, $\\frac{{{num1}}}{{{denom1}}} x \\frac{{{num2}}}{{{denom2}}} = \\frac{{{result_num}}}{{{result_denom}}} = \\frac{{{simplified_num}}}{{{simplified_denom}}}$."
    else:
        template['solution'][3][1] = f"So, $\\frac{{{num1}}}{{{denom1}}} x \\frac{{{num2}}}{{{denom2}}} = \\frac{{{result_num}}}{{{result_denom}}}$."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_20_E2 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_20_E2")
print("Saved to 'Gr7_20_E2 variations.json'")