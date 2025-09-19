import json
import random
import copy

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_17_E1
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_17_E1':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_17_E1")

# Need to generate 49 variations (51 total - 2 templates = 49)
variations = []
variation_count = 3  # Start numbering from 3 (templates are 1_1, 1_2)

# Generate variations based on template 1 (addition)
for i in range(25):
    template = copy.deepcopy(templates[0])

    # Generate random mixed numbers for addition
    whole1 = random.randint(1, 15)
    num1 = random.randint(1, 10)
    denom = random.randint(5, 15)
    num1 = min(num1, denom - 1)  # Ensure proper fraction

    whole2 = random.randint(1, 15)
    num2 = random.randint(1, denom - 1)

    # Calculate the result
    total_num = num1 + num2
    total_whole = whole1 + whole2

    # Handle improper fraction
    if total_num >= denom:
        extra_whole = total_num // denom
        total_whole += extra_whole
        total_num = total_num % denom

    # Update question fields
    template['question_number'] = f"1_{variation_count}"
    template['image_tag'] = f"Gr7_17_1_{variation_count}"
    template['backend_description'] = f"Shows the addition of two mixed numbers: {whole1} {num1}/{denom} + {whole2} {num2}/{denom} with an empty box for the answer."

    # Update correct answers
    if total_num == 0:
        template['correct_answers'] = [[str(total_whole)], [f"{total_whole * denom}/{denom}"]]
    else:
        # Find GCD for simplified form
        from math import gcd
        g = gcd(total_num, denom)
        simplified_num = total_num // g
        simplified_denom = denom // g

        if simplified_denom == 1:
            template['correct_answers'] = [[str(total_whole + simplified_num)]]
        else:
            template['correct_answers'] = [
                [f"{total_whole} {simplified_num}/{simplified_denom}"],
                [f"{total_whole * denom + total_num}/{denom}"]
            ]

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_17_1_{variation_count}_step_{step[0].split('/')[0]}"
                step[2] = step[2].replace("2 8/11 + 8 8/11", f"{whole1} {num1}/{denom} + {whole2} {num2}/{denom}")
                step[2] = step[2].replace("10 + 16/11", f"{whole1 + whole2} + {num1 + num2}/{denom}")

    # Update solution text
    template['solution'][0][1] = f"We are adding two mixed numbers: ${whole1} \\frac{{{num1}}}{{{denom}}} + {whole2} \\frac{{{num2}}}{{{denom}}}$."
    template['solution'][1][1] = f"First, add the whole numbers: {whole1} + {whole2} = {whole1 + whole2}."
    template['solution'][2][1] = f"Next, add the fractions: $\\frac{{{num1}}}{{{denom}}} + \\frac{{{num2}}}{{{denom}}} = \\frac{{{num1 + num2}}}{{{denom}}}$."

    if num1 + num2 >= denom:
        extra = (num1 + num2) // denom
        remainder = (num1 + num2) % denom
        template['solution'][4][1] = f"Since $\\frac{{{num1 + num2}}}{{{denom}}}$ is an improper fraction, convert it to a mixed number:\n\n $\\frac{{{num1 + num2}}}{{{denom}}} = {extra} \\frac{{{remainder}}}{{{denom}}}$."
        template['solution'][5][1] = f"Now add the whole numbers: {whole1 + whole2} + {extra} = {total_whole}.\n\n So the final answer is {total_whole} $\\frac{{{total_num}}}{{{denom}}}$."
    else:
        template['solution'][4][1] = f"The fraction $\\frac{{{num1 + num2}}}{{{denom}}}$ is already proper."
        template['solution'][5][1] = f"So the final answer is {total_whole} $\\frac{{{total_num}}}{{{denom}}}$."

    variations.append(template)
    variation_count += 1

# Generate variations based on template 2 (subtraction)
for i in range(24):
    template = copy.deepcopy(templates[1])

    # Generate random mixed numbers for subtraction (ensure first > second)
    denom = random.randint(5, 15)
    whole1 = random.randint(10, 20)
    num1 = random.randint(1, denom - 1)

    whole2 = random.randint(1, min(whole1 - 1, 10))
    num2 = random.randint(1, denom - 1)

    # Calculate the result with borrowing if needed
    if num1 < num2:
        # Need to borrow
        whole1_borrow = whole1 - 1
        num1_borrow = num1 + denom
        result_whole = whole1_borrow - whole2
        result_num = num1_borrow - num2
    else:
        result_whole = whole1 - whole2
        result_num = num1 - num2

    # Update question fields
    template['question_number'] = f"2_{variation_count - 25}"
    template['image_tag'] = f"Gr7_17_1_{variation_count}"
    template['backend_description'] = f"Shows the subtraction of two mixed numbers: {whole1} {num1}/{denom} - {whole2} {num2}/{denom} with an empty box for the answer."

    # Update correct answers
    if result_num == 0:
        template['correct_answers'] = [[str(result_whole)], [f"{result_whole * denom}/{denom}"]]
    else:
        # Find GCD for simplified form
        from math import gcd
        g = gcd(result_num, denom)
        simplified_num = result_num // g
        simplified_denom = denom // g

        if simplified_denom == 1:
            template['correct_answers'] = [[str(result_whole + simplified_num)]]
        else:
            template['correct_answers'] = [
                [f"{result_whole} {simplified_num}/{simplified_denom}"],
                [f"{result_whole * denom + result_num}/{denom}"]
            ]

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_17_1_{variation_count}_step_{step[0].split('/')[0]}"
                step[2] = step[2].replace("15 1/11 - 6 8/11", f"{whole1} {num1}/{denom} - {whole2} {num2}/{denom}")
                if num1 < num2:
                    step[2] = step[2].replace("14 12/11", f"{whole1 - 1} {num1 + denom}/{denom}")

    # Update solution text
    if num1 < num2:
        template['solution'][1][1] = f"We can't subtract $\\frac{{{num2}}}{{{denom}}}$ from $\\frac{{{num1}}}{{{denom}}}$, so we need to borrow 1 from the whole number part of {whole1} $\\frac{{{num1}}}{{{denom}}}$:"
        template['solution'][2][1] = f"Rewrite {whole1} $\\frac{{{num1}}}{{{denom}}}$ as {whole1 - 1} $\\frac{{{num1 + denom}}}{{{denom}}}$. Now we can subtract {whole2} $\\frac{{{num2}}}{{{denom}}}$."
        template['solution'][3][1] = f"Subtract the whole numbers: {whole1 - 1} − {whole2} = {result_whole}.\n\nSubtract the fractions: $\\frac{{{num1 + denom}}}{{{denom}}} − \\frac{{{num2}}}{{{denom}}} = \\frac{{{result_num}}}{{{denom}}}$."
    else:
        template['solution'][1][1] = f"We are subtracting {whole2} $\\frac{{{num2}}}{{{denom}}}$ from {whole1} $\\frac{{{num1}}}{{{denom}}}$."
        template['solution'][2][1] = f"Since $\\frac{{{num1}}}{{{denom}}} ≥ \\frac{{{num2}}}{{{denom}}}$, we can subtract directly."
        template['solution'][3][1] = f"Subtract the whole numbers: {whole1} − {whole2} = {result_whole}.\n\nSubtract the fractions: $\\frac{{{num1}}}{{{denom}}} − \\frac{{{num2}}}{{{denom}}} = \\frac{{{result_num}}}{{{denom}}}$."

    template['solution'][5][1] = f"The final answer is {result_whole} $\\frac{{{result_num}}}{{{denom}}}$."

    variations.append(template)
    variation_count += 1

# Save variations to JSON file
with open('Gr7_17_E1 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_17_E1")
print("Saved to 'Gr7_17_E1 variations.json'")