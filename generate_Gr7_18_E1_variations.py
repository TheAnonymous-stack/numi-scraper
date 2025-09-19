import json
import random
import copy

# Load the template questions
with open('test_fixed.json', 'r') as f:
    data = json.load(f)

# Extract template questions for tag Gr7_18_E1
templates = []
for item in data:
    if isinstance(item, dict) and item.get('tag') == 'Gr7_18_E1':
        templates.append(item)

print(f"Found {len(templates)} templates for Gr7_18_E1")

# Need to generate 50 variations (51 total - 1 template = 50)
variations = []

def prime_factorization(n):
    """Return the prime factorization of n as a list"""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

# Generate 50 variations
for i in range(50):
    template = copy.deepcopy(templates[0])

    # Generate two numbers with interesting GCD
    if i < 15:
        # Small numbers with obvious GCD
        num1 = random.randint(4, 20)
        factor = random.randint(2, 5)
        num2 = num1 * random.randint(2, 4) // factor
        if num2 == num1:
            num2 = num1 * 2
    elif i < 30:
        # Medium numbers
        num1 = random.randint(12, 48)
        num2 = random.randint(8, 36)
    else:
        # Larger numbers
        num1 = random.randint(24, 72)
        num2 = random.randint(16, 60)

    # Ensure we don't have the same pair as the template
    if num1 == 8 and num2 == 4:
        num1, num2 = 12, 8

    # Calculate GCD
    gcf = gcd(num1, num2)

    # Get prime factorizations
    factors1 = prime_factorization(num1)
    factors2 = prime_factorization(num2)

    # Update question
    template['question_number'] = f"1_{i + 2}"
    template['question_text'] = f"What is the greatest common factor of {num1} and {num2}?\n\n"

    # Update correct answer
    template['correct_answers'] = [str(gcf)]

    # Update solution image tags
    if 'solution_image_tag' in template and template['solution_image_tag']:
        for step in template['solution_image_tag']:
            if len(step) > 1:
                step[1] = f"Gr7_18_1_{i + 2}_step_{step[0].split('/')[0]}"

                if "step_1" in step[1]:
                    factors1_str = " x ".join(map(str, factors1))
                    factors2_str = " x ".join(map(str, factors2))
                    step[2] = f"Shows the prime factorization of both numbers. {num1} is broken down as {num1} = {factors1_str} (with each factor shown in red), and {num2} is broken down as {num2} = {factors2_str} (with each factor shown in red)."
                elif "step_2" in step[1]:
                    # Find common factors
                    f1_copy = factors1.copy()
                    f2_copy = factors2.copy()
                    common = []
                    for f in f1_copy:
                        if f in f2_copy:
                            common.append(f)
                            f2_copy.remove(f)

                    if common:
                        common_str = " x ".join(map(str, common))
                        step[2] = f"Highlights the common factors between the two numbers. Both {num1} and {num2} share {common_str} as common factors, with the shared factors shown in red to make the comparison clear."
                    else:
                        step[2] = f"Shows that {num1} and {num2} share only 1 as a common factor."

    # Update solution
    factors1_str = " x ".join(map(str, factors1))
    factors2_str = " x ".join(map(str, factors2))

    template['solution'][0][1] = "Write the prime factorization for each number."
    template['solution'][1][1] = "Next, find the common factors shared by both of the numbers."
    template['solution'][2][1] = "Finally, multiply the common factors to find the greatest common factor."

    # Find common prime factors
    f1_copy = factors1.copy()
    f2_copy = factors2.copy()
    common = []
    for f in f1_copy:
        if f in f2_copy:
            common.append(f)
            f2_copy.remove(f)

    if common:
        common_str = " x ".join(map(str, common))
        template['solution'][3][1] = f"{common_str} = {gcf}"
    else:
        template['solution'][3][1] = f"The only common factor is 1."

    template['solution'][4][1] = f"The greatest common factor of {num1} and {num2} is {gcf}."

    variations.append(template)

# Save variations to JSON file
with open('Gr7_18_E1 variations.json', 'w') as f:
    json.dump(variations, f, indent=2)

print(f"Generated {len(variations)} variations for Gr7_18_E1")
print("Saved to 'Gr7_18_E1 variations.json'")