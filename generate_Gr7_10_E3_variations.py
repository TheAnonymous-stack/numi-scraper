import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_10_E3 (add-integers)"""

    # Load template
    with open('Gr7_10_E3_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Generate two random integers
        num1 = random.randint(-20, 20)
        num2 = random.randint(-20, 20)

        # Avoid trivial cases
        if num1 == 0 or num2 == 0:
            continue

        result = num1 + num2

        # Create variation
        variation = copy.deepcopy(template)

        # Format the expression
        if num2 >= 0:
            expression = f"${num1} + {num2} = \\_\\_\\_\\_$"
        else:
            expression = f"${num1} + ({num2}) = \\_\\_\\_\\_$"

        # Update question text
        variation["question_text"] = f"Add:\n\n{expression}\n"

        # Update correct answer
        variation["correct_answers"] = [str(result)]

        # Generate appropriate solution based on the numbers
        if num1 < 0 and num2 < 0:
            # Both negative
            variation["solution"] = [
                [
                    "1/4",
                    f"We are adding {num1} + ({num2})."
                ],
                [
                    "2/4",
                    "Both numbers are negative, so the result will be negative."
                ],
                [
                    "3/4",
                    f"When adding two negative numbers, add their absolute values: {abs(num1)} + {abs(num2)} = {abs(result)}"
                ],
                [
                    "4/4",
                    f"Therefore, {num1} + ({num2}) = {result}."
                ]
            ]
        elif num1 > 0 and num2 > 0:
            # Both positive
            variation["solution"] = [
                [
                    "1/4",
                    f"We are adding {num1} + {num2}."
                ],
                [
                    "2/4",
                    "Both numbers are positive, so the result will be positive."
                ],
                [
                    "3/4",
                    f"Simply add the two positive numbers: {num1} + {num2} = {result}"
                ],
                [
                    "4/4",
                    f"Therefore, {num1} + {num2} = {result}."
                ]
            ]
        else:
            # One positive, one negative
            abs1, abs2 = abs(num1), abs(num2)
            if abs1 > abs2:
                sign = "positive" if num1 > 0 else "negative"
                bigger = num1
                smaller = num2
            else:
                sign = "positive" if num2 > 0 else "negative"
                bigger = num2
                smaller = num1

            variation["solution"] = [
                [
                    "1/4",
                    f"We are adding {num1} + {num2 if num2 > 0 else f'({num2})'}."
                ],
                [
                    "2/4",
                    f"One number is negative ({num1 if num1 < 0 else num2}) and one is positive ({num1 if num1 > 0 else num2}). Since {abs(bigger)} is bigger than {abs(smaller)}, our final answer should be {sign}."
                ],
                [
                    "3/4",
                    f"When adding {num1} + {num2 if num2 > 0 else f'({num2})'}, you are finding the difference between {max(abs1, abs2)} and {min(abs1, abs2)}.\n\nSince {abs(bigger)} is larger, subtract: {max(abs1, abs2)} – {min(abs1, abs2)} = {abs(result)}"
                ],
                [
                    "4/4",
                    f"Therefore, {num1} + {num2 if num2 > 0 else f'({num2})'} = {result}."
                ]
            ]

        # Update question number
        variation["question_number"] = f"3_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_10_E3 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_10_E3")

if __name__ == "__main__":
    generate_variations()