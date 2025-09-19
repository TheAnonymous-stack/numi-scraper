import json
import random
import copy

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_18_E2
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_18_E2':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_18_E2")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate least common multiple"""
    return abs(a * b) // gcd(a, b)

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])

    # Generate two numbers with interesting LCM
    if i < 20:
        # Small numbers where one divides the other
        choices = [
            (2, 4), (3, 6), (4, 8), (3, 9), (5, 15), (6, 12), (7, 14),
            (4, 12), (5, 20), (6, 18), (8, 16), (9, 18), (7, 21), (8, 24)
        ]
        num1, num2 = random.choice(choices)
        if random.random() > 0.5:
            num1, num2 = num2, num1
    elif i < 35:
        # Numbers with small common factors
        num1 = random.randint(4, 15)
        num2 = random.randint(6, 20)
    else:
        # Larger numbers
        num1 = random.randint(12, 30)
        num2 = random.randint(8, 25)

    # Ensure we don't have the same pair as the template
    if num1 == 5 and num2 == 10:
        num1, num2 = 3, 12

    # Calculate LCM
    result_lcm = lcm(num1, num2)

    # Update question
    template['question_number'] = f"2_{i + 2}"
    template['question_text'] = f"What is the least common multiple of {num1} and {num2}?\n\n"

    # Update correct answer
    template['correct_answers'] = [str(result_lcm)]

    # Generate multiples for solution
    multiples1 = [num1 * j for j in range(1, min(6, result_lcm // num1 + 2))]
    multiples2 = [num2 * j for j in range(1, min(6, result_lcm // num2 + 2))]

    multiples1_str = ", ".join(map(str, multiples1))
    if multiples1[-1] < result_lcm:
        multiples1_str += ", ..."

    multiples2_str = ", ".join(map(str, multiples2))
    if multiples2[-1] < result_lcm:
        multiples2_str += ", ..."

    # Update solution
    template['solution'][0][1] = f"To find the least common multiple (LCM) of {num1} and {num2}, list the multiples of each number."
    template['solution'][1][1] = f"Multiples of {num1}: {multiples1_str}"
    template['solution'][2][1] = f"Multiples of {num2}: {multiples2_str}"
    template['solution'][3][1] = f"The first multiple that both numbers share is {result_lcm}."
    template['solution'][4][1] = f"So, the least common multiple of {num1} and {num2} is {result_lcm}."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_18_E2 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_18_E2")
print("Saved to 'Gr7_18_E2 variations.json'")