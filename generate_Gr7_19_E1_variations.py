import json
import random
import copy

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_19_E1
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_19_E1':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_19_E1")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])

    # Choose base and repetitions
    if i < 20:
        # Small bases with small exponents
        base = random.randint(2, 9)
        exponent = random.randint(2, 4)
    elif i < 35:
        # Include some with exponent 1 or larger bases
        base = random.randint(2, 15)
        exponent = random.randint(1, 5)
    else:
        # Mix of various combinations
        base = random.randint(3, 20)
        exponent = random.randint(2, 6)

    # Avoid the original (2 x 2)
    if base == 2 and exponent == 2:
        base = 3

    # Create multiplication expression
    mult_expr = " x ".join([str(base)] * exponent)

    # Update question
    template['question_number'] = f"1_{i + 2}"
    template['question_text'] = f"Write the expression using an exponent.\n\n{mult_expr} = \\_\\_\\_\\_^{{\\_\\_\\_\\_}}$"

    # Update correct answer
    template['correct_answers'] = [f"{base}^{exponent}"]

    # Update solution
    template['solution'][0][1] = f"We are multiplying {mult_expr}. That means we are using {base} (the base) as a factor {exponent} {'time' if exponent == 1 else 'times'}."
    template['solution'][1][1] = f"So, we can write this as an exponent.\n\n{mult_expr} = {base}$^{{{exponent}}}$."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_19_E1 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_19_E1")
print("Saved to 'Gr7_19_E1 variations.json'")