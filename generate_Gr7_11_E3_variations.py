import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_11_E3 (subtract-integers)"""

    # Load template
    with open('Gr7_11_E3_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Generate two random integers for subtraction
        num1 = random.randint(-20, 20)
        num2 = random.randint(-20, 20)

        # Avoid trivial cases
        if num1 == 0 or num2 == 0:
            continue

        result = num1 - num2

        # Create variation
        variation = copy.deepcopy(template)

        # Format the expression
        if num2 < 0:
            expression = f"${num1} - ({num2}) = \\_\\_\\_\\_$"
            expression_plain = f"{num1} - ({num2})"
        else:
            expression = f"${num1} - {num2} = \\_\\_\\_\\_$"
            expression_plain = f"{num1} - {num2}"

        # Update question text
        variation["question_text"] = f"Subtract:\n\n{expression}\n"

        # Update correct answer
        variation["correct_answers"] = [str(result)]

        # Generate solution based on the numbers
        opposite_num2 = -num2
        if num2 < 0:
            # Subtracting a negative (becomes addition)
            variation["solution"] = [
                [
                    "1/6",
                    f"We are subtracting: {expression_plain}."
                ],
                [
                    "2/6",
                    f"Subtracting a negative number is the same as adding its opposite, so rewrite the expression: {expression_plain} = {num1} + {opposite_num2}."
                ],
                [
                    "3/6",
                    f"Since {num1} {'and' if (num1 > 0 and opposite_num2 > 0) or (num1 < 0 and opposite_num2 < 0) else 'is'} {opposite_num2 if (num1 > 0 and opposite_num2 > 0) or (num1 < 0 and opposite_num2 < 0) else ''} {'are both positive' if num1 > 0 and opposite_num2 > 0 else 'are both negative' if num1 < 0 and opposite_num2 < 0 else 'have different signs'}, the answer will be {'' if result > 0 else 'negative' if result < 0 else 'zero'}."
                ],
                [
                    "4/6",
                    f"Now add: {num1} + {opposite_num2}"
                ],
                [
                    "5/6",
                    f"{'When you add two positive numbers, simply add them' if num1 > 0 and opposite_num2 > 0 else 'When you add two negative numbers, add their values and keep the negative sign' if num1 < 0 and opposite_num2 < 0 else f'Find the difference: {max(abs(num1), abs(opposite_num2))} - {min(abs(num1), abs(opposite_num2))} = {abs(result)}'}{', so the answer is ' + str(result) if (num1 > 0 and opposite_num2 > 0) or (num1 < 0 and opposite_num2 < 0) else ''}."
                ],
                [
                    "6/6",
                    f"Therefore, {expression_plain} = {result}."
                ]
            ]
        else:
            # Subtracting a positive
            variation["solution"] = [
                [
                    "1/6",
                    f"We are subtracting: {expression_plain}."
                ],
                [
                    "2/6",
                    f"Subtracting a number is the same as adding its opposite, so rewrite the expression: {expression_plain} = {num1} + ({opposite_num2})."
                ],
                [
                    "3/6",
                    f"Since {num1 if num1 < 0 else f'{num1} is positive'} and {opposite_num2} {'are both negative' if num1 < 0 else 'is negative'}, the answer will be {'negative' if result < 0 else 'positive' if result > 0 else 'zero'}."
                ],
                [
                    "4/6",
                    f"Now add the two {'negative' if num1 < 0 else ''} numbers: {num1} + ({opposite_num2})"
                ],
                [
                    "5/6",
                    f"{'When you add two negative numbers, you add their values and keep the negative sign: ' + str(abs(num1)) + ' + ' + str(abs(opposite_num2)) + ' = ' + str(abs(result)) + ', so the answer is ' + str(result) if num1 < 0 else f'Find the difference between {abs(num1)} and {abs(opposite_num2)}: {max(abs(num1), abs(opposite_num2))} - {min(abs(num1), abs(opposite_num2))} = {abs(result)}'}.{'The result is positive since ' + str(num1) + ' has the larger absolute value.' if result > 0 and num1 > 0 else ''}"
                ],
                [
                    "6/6",
                    f"Therefore, {expression_plain} = {result}."
                ]
            ]

        # Update question number
        variation["question_number"] = f"3_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_11_E3 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_11_E3")

if __name__ == "__main__":
    generate_variations()