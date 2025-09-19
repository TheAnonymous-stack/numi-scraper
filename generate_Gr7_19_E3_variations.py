import json
import random
import copy
import math

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_19_E3
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_19_E3':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_19_E3")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])

    # Choose base and result
    if i < 20:
        # Powers of 2
        base = 2
        exponent = random.randint(2, 6)
        if exponent == 3:  # Skip original
            exponent = 4
        result = base ** exponent
    elif i < 35:
        # Powers of 3
        base = 3
        exponent = random.randint(2, 4)
        result = base ** exponent
    elif i < 45:
        # Powers of 4 and 5
        base = random.choice([4, 5])
        exponent = random.randint(2, 3)
        result = base ** exponent
    else:
        # Some simple cases with larger bases
        base = random.randint(6, 10)
        exponent = 2
        result = base ** exponent

    # Update question
    template['question_number'] = f"3_{i + 2}"
    template['question_text'] = f"Solve for s.\n\n{base}$^{{s}} = {result}$\n\n$s = \\_\\_\\_\\_$"

    # Update correct answer
    template['correct_answers'] = [str(exponent)]

    # Update solution image tag
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_19_3_{i + 2}_step_4"
                step[2] = f"Shows a table with three columns: 'Power of {base}', 'Repeated multiplication', and 'Value'. The table demonstrates the pattern of how each power of {base} is calculated, with arrows indicating multiplication by {base} to get from one value to the next."

    # Update solution
    template['solution'][0][1] = f"We are given the equation: {base}$^{{s}} = {result}$."
    template['solution'][1][1] = f"This means we need to figure out how many times we multiply {base} by itself to get {result}."

    # Generate trial calculations
    if exponent >= 2:
        trial1 = base ** (exponent - 1) if exponent > 2 else base ** 2
        trial1_exp = exponent - 1 if exponent > 2 else 2
        trial1_calc = " x ".join([str(base)] * trial1_exp)

        template['solution'][2][1] = f"First try {base}$^{{{trial1_exp}}} = {trial1_calc} = {trial1}$, this does not equal {result}."

        # Correct calculation
        correct_calc = " x ".join([str(base)] * exponent)
        if exponent == 2:
            template['solution'][3][1] = f"Now try {base}$^{{{exponent}}} = {correct_calc} = {result}$\n"
        else:
            intermediate = base ** (exponent - 1)
            template['solution'][3][1] = f"Now try {base}$^{{{exponent}}} = {correct_calc} = {intermediate} x {base} = {result}$\n"
    else:  # exponent = 1
        template['solution'][2][1] = f"Since {base}$^{{1}} = {base} = {result}$, we have our answer."
        template['solution'][3][1] = ""

    template['solution'][4][1] = f"Therefore, s = {exponent}."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_19_E3 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_19_E3")
print("Saved to 'Gr7_19_E3 variations.json'")