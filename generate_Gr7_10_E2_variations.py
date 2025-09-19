import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_10_E2 (add-integers-using-number-lines)"""

    # Load template
    with open('Gr7_10_E2_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Random integers to add
        num1 = random.randint(-10, -1)
        num2 = random.randint(-8, 8)
        if num2 == 0:
            num2 = random.choice([-5, -3, 3, 5])

        result = num1 + num2

        # Ensure result is within reasonable range for number line
        if result < -15 or result > 5:
            continue

        # Create variation
        variation = copy.deepcopy(template)

        # Format the expression
        if num2 >= 0:
            expression = f"${num1} + {num2}$"
            expression_plain = f"{num1} + {num2}"
        else:
            expression = f"${num1} + ({num2})$"
            expression_plain = f"{num1} + ({num2})"

        # Update question text
        variation["question_text"] = f"Which number line models {expression}?\n\nChoose the correct number line, then write the result of the expression.\n\nAdd.\n{expression_plain} = \\_\\_\\_\\_\n"

        # Update image choice tags
        variation["image_choice_tags"] = [
            f"Gr7_10_2_{variation_num}_A",
            f"Gr7_10_2_{variation_num}_B"
        ]

        # Determine direction and steps
        if num2 > 0:
            direction_correct = "right"
            direction_incorrect = "left"
            steps = num2
        else:
            direction_correct = "left"
            direction_incorrect = "right"
            steps = abs(num2)

        # Create descriptions for the two number lines
        variation["image_choice_tags_backend_description"] = [
            f"Number line from {min(-15, result - 2)} to {max(5, num1 + 2)} with a blue arrow starting at {num1} and curving {direction_correct} {steps} units to land at {result}, representing {expression_plain} = {result}",
            f"Number line from {min(-15, num1 - 2)} to {max(5, result + 2)} with a blue arrow starting at {result} and curving {direction_incorrect} {steps} units to land at {num1}, representing an incorrect interpretation"
        ]

        # Correct answer is always A (the first option shows correct addition)
        variation["correct_answers"] = ["A", str(result)]

        # Update solution
        if num2 < 0:
            variation["solution"] = [
                [
                    "1/4",
                    "When you add two negative numbers, the answer is also negative."
                ],
                [
                    "2/4",
                    f"Start at {num1} on the number line."
                ],
                [
                    "3/4",
                    f"You are adding {num2}, so move {abs(num2)} steps to the left."
                ],
                [
                    "4/4",
                    f"{expression_plain} = {result}, so the arrow should start on {num1} and land on {result}."
                ]
            ]
        elif num2 > 0:
            variation["solution"] = [
                [
                    "1/4",
                    f"When you add a negative number and a positive number, find the difference and use the sign of the larger absolute value."
                ],
                [
                    "2/4",
                    f"Start at {num1} on the number line."
                ],
                [
                    "3/4",
                    f"You are adding {num2}, so move {num2} steps to the right."
                ],
                [
                    "4/4",
                    f"{expression_plain} = {result}, so the arrow should start on {num1} and land on {result}."
                ]
            ]

        # Update question number
        variation["question_number"] = f"2_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_10_E2 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_10_E2")

if __name__ == "__main__":
    generate_variations()