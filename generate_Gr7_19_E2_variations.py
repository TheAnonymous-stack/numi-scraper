import json
import random
import copy

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_19_E2
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_19_E2':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_19_E2")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])

    # Choose base and exponent
    if i < 20:
        # Small bases with exponent 2
        base = random.randint(2, 12)
        if base == 8:  # Skip the original
            base = 7
        exponent = 2
    elif i < 35:
        # Various bases with exponent 2 or 3
        base = random.randint(3, 15)
        exponent = random.choice([2, 3])
    else:
        # Mix including some with exponent 4 and 1
        base = random.randint(2, 20)
        exponent = random.choice([1, 2, 3, 4])

    # Calculate the result
    result = base ** exponent

    # Update question
    template['question_number'] = f"2_{i + 2}"
    template['question_text'] = f"Evaluate.\n\n{base}$^{{{exponent}}} = \\_\\_\\_\\_$\n\n"
    template['image_tag'] = f"Gr7_19_2_{i + 2}"
    template['backend_description'] = f"Shows the power expression {base}^{exponent} equals blank for the student to fill in."

    # Update correct answer
    template['correct_answers'] = [str(result)]

    # Update solution image tag
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_19_2_{i + 2}_step_2"

                # Create multiplication string
                if exponent == 1:
                    mult_str = str(base)
                else:
                    mult_str = " x ".join([str(base)] * exponent)

                step[2] = f"Shows the calculation {base}^{exponent} = {mult_str} = {result}. The exponent notation is expanded to show multiplication, then the final result."

    # Update solution
    if exponent == 1:
        template['solution'][0][1] = f"The base is {base} and the exponent is 1. This means {base} appears once, so the answer is just {base}."
    else:
        template['solution'][0][1] = f"The base is {base} and the exponent is {exponent}. This means we multiply {base} by itself {exponent} times."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_19_E2 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_19_E2")
print("Saved to 'Gr7_19_E2 variations.json'")