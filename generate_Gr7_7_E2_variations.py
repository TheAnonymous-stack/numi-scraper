import json
import random
import copy

def generate_variations():
    # Load the fixed JSON file to get the template
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Find the template with tag Gr7_7_E2
    template = None
    for item in data:
        if item.get('tag') == 'Gr7_7_E2':
            template = item
            break

    if not template:
        print("Template for Gr7_7_E2 not found")
        return

    variations = []

    # Generate 50 variations
    for i in range(2, 52):
        variation = copy.deepcopy(template)

        # Generate random decimal values for the expression
        # Format: a + b ÷ c where we need to follow order of operations
        a = round(random.uniform(0.1, 9.9), random.choice([1, 2]))
        b = round(random.uniform(0.1, 9.9), random.choice([1, 2]))
        c = random.choice([2, 3, 4, 5, 6, 8, 10])  # Use divisors that give nice decimals

        # Calculate the result
        division_result = round(b / c, 3)
        final_result = round(a + division_result, 3)

        # Format for display
        a_display = f"{a:.2f}" if len(str(a).split('.')[-1]) > 1 else f"{a:.1f}" if '.' in str(a) else str(a)
        b_display = f"{b:.2f}" if len(str(b).split('.')[-1]) > 1 else f"{b:.1f}" if '.' in str(b) else str(b)

        # Update question text
        variation['question_text'] = f"Evaluate the expression.\n\n{a_display} dollars + {b_display} ÷ {c} = \\_\\_\\_\\_$\n\nWrite your answer as an integer or a decimal. Do not round.\n\n"

        # Handle alternative answers (with and without trailing zeros)
        correct_answers = []
        result_str = str(final_result)

        # Remove unnecessary trailing zeros
        if '.' in result_str:
            result_str = result_str.rstrip('0').rstrip('.')

        correct_answers.append([result_str])

        # Add version with one trailing zero if applicable
        if '.' in result_str:
            correct_answers.append([result_str + '0'])
            # Add version with two trailing zeros if needed
            if len(result_str.split('.')[-1]) == 1:
                correct_answers.append([result_str + '00'])

        variation['correct_answers'] = correct_answers if len(correct_answers) > 1 else correct_answers[0]
        variation['has_alternative_answers'] = len(correct_answers) > 1

        # Calculate steps for solution
        division_str = str(division_result).rstrip('0').rstrip('.')
        final_str = str(final_result).rstrip('0').rstrip('.')

        # Update solution
        variation['solution'] = [
            [
                "1/5",
                f"Start by identifying the operations in the expression: {a_display} + {b_display} ÷ {c}. According to the order of operations, divide before adding."
            ],
            [
                "2/5",
                f"Divide first: {b_display} ÷ {c} = {division_str}."
            ],
            [
                "3/5",
                f"Now add: {a_display} + {division_str} = {final_str}."
            ],
            [
                "4/5",
                f"So, {a_display} + {b_display} ÷ {c} = {final_str}."
            ],
            [
                "5/5",
                f"The final value of the expression is {final_str}."
            ]
        ]

        # Update question number
        variation['question_number'] = f"2_{i}"

        variations.append(variation)

    # Save variations to JSON file
    with open(r'C:\Users\kapil\numi-scraper\Gr7_7_E2 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_7_E2")

if __name__ == "__main__":
    generate_variations()