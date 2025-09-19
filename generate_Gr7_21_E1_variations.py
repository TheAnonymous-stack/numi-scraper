import json
import random
import copy
from math import gcd

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_21_E1
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_21_E1':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_21_E1")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])

    # Generate two mixed numbers
    if i < 20:
        # Smaller mixed numbers
        whole1 = random.randint(1, 5)
        whole2 = random.randint(1, 4)
        denom1 = random.randint(2, 6)
        denom2 = random.randint(2, 6)
        num1 = random.randint(1, denom1 - 1)
        num2 = random.randint(1, denom2 - 1)
    elif i < 35:
        # Medium mixed numbers
        whole1 = random.randint(2, 8)
        whole2 = random.randint(2, 6)
        denom1 = random.randint(3, 8)
        denom2 = random.randint(3, 8)
        num1 = random.randint(1, denom1 - 1)
        num2 = random.randint(1, denom2 - 1)
    else:
        # Larger mixed numbers
        whole1 = random.randint(3, 10)
        whole2 = random.randint(2, 8)
        denom1 = random.randint(4, 10)
        denom2 = random.randint(4, 10)
        num1 = random.randint(1, denom1 - 1)
        num2 = random.randint(1, denom2 - 1)

    # Avoid the original
    if whole1 == 4 and num1 == 1 and denom1 == 3 and whole2 == 2 and num2 == 1 and denom2 == 4:
        whole1 = 5

    # Convert to improper fractions
    improper1_num = whole1 * denom1 + num1
    improper2_num = whole2 * denom2 + num2

    # Multiply
    result_num = improper1_num * improper2_num
    result_denom = denom1 * denom2

    # Simplify
    g = gcd(result_num, result_denom)
    simplified_num = result_num // g
    simplified_denom = result_denom // g

    # Convert back to mixed number
    result_whole = simplified_num // simplified_denom
    result_num_final = simplified_num % simplified_denom

    # Update question
    template['question_number'] = f"1_{i + 2}"
    template['image_tag'] = f"Gr7_21_1_{i + 2}"
    template['backend_description'] = f"Shows the multiplication of two mixed numbers: {whole1} {num1}/{denom1} x {whole2} {num2}/{denom2} with an empty box for the answer."

    # Update correct answers
    if result_num_final == 0:
        template['correct_answers'] = [[str(result_whole)], [f"{result_whole * simplified_denom}/{simplified_denom}"]]
    else:
        template['correct_answers'] = [
            [f"{result_whole} {result_num_final}/{simplified_denom}"],
            [f"{simplified_num}/{simplified_denom}"]
        ]

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for idx, step in enumerate(template['solution_image_tag']):
            if len(step) > 1:
                if idx == 0:
                    step[1] = f"Gr7_21_1_{i + 2}_step_3"
                    step[2] = f"Shows the conversion of {whole1} {num1}/{denom1} to an improper fraction: {whole1} {num1}/{denom1} = ({whole1} x {denom1} + {num1})/{denom1} = {improper1_num}/{denom1}."
                elif idx == 1:
                    step[1] = f"Gr7_21_1_{i + 2}_step_4"
                    step[2] = f"Shows the conversion of {whole2} {num2}/{denom2} to an improper fraction: {whole2} {num2}/{denom2} = ({whole2} x {denom2} + {num2})/{denom2} = {improper2_num}/{denom2}."
                elif idx == 2:
                    step[1] = f"Gr7_21_1_{i + 2}_step_5"
                    step[2] = f"Shows the multiplication of the improper fractions: {improper1_num}/{denom1} x {improper2_num}/{denom2} = ({improper1_num} x {improper2_num})/({denom1} x {denom2}) = {result_num}/{result_denom}."
                elif idx == 3:
                    step[1] = f"Gr7_21_1_{i + 2}_step_6"

                    if g > 1:
                        if result_num_final > 0:
                            step[2] = f"Shows the conversion back to a mixed number: {result_num}/{result_denom} = {result_whole} {result_num_final * g}/{simplified_denom * g} = {result_whole} {result_num_final}/{simplified_denom}. The fraction is simplified by dividing both by {g}."
                        else:
                            step[2] = f"Shows the conversion: {result_num}/{result_denom} = {result_whole}. The result is a whole number."
                    else:
                        if result_num_final > 0:
                            step[2] = f"Shows the conversion back to a mixed number: {result_num}/{result_denom} = {result_whole} {result_num_final}/{simplified_denom}."
                        else:
                            step[2] = f"Shows the conversion: {result_num}/{result_denom} = {result_whole}. The result is a whole number."

    # Update solution
    template['solution'][0][1] = f"We are multiplying {whole1} $\\frac{{{num1}}}{{{denom1}}} x {whole2} \\frac{{{num2}}}{{{denom2}}}$."
    template['solution'][1][1] = "First, change the mixed numbers to improper fractions."
    template['solution'][2][1] = f"Convert {whole1} {num1}/{denom1} to an improper fraction:\n"
    template['solution'][3][1] = f"Convert {whole2} {num2}/{denom2} to an improper fraction:\n"
    template['solution'][4][1] = "Multiply the improper fractions:\n"
    template['solution'][5][1] = "Convert the improper fraction answer back to a mixed number and simplify the fraction:\n"

    if result_num_final == 0:
        template['solution'][6][1] = f"The final answer is {result_whole}."
    else:
        template['solution'][6][1] = f"The final answer is {result_whole} $\\frac{{{result_num_final}}}{{{simplified_denom}}}$."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_21_E1 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_21_E1")
print("Saved to 'Gr7_21_E1 variations.json'")