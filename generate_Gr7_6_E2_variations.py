import json
import random
import copy

def generate_variations():
    # Load the fixed JSON file to get the template
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Find the template with tag Gr7_6_E2
    template = None
    for item in data:
        if item.get('tag') == 'Gr7_6_E2':
            template = item
            break

    if not template:
        print("Template for Gr7_6_E2 not found")
        return

    variations = []

    # Common fractions that convert nicely to percentages
    fraction_percentage_pairs = [
        (1, 2, 50),
        (1, 4, 25),
        (3, 4, 75),
        (1, 5, 20),
        (2, 5, 40),
        (3, 5, 60),
        (4, 5, 80),
        (1, 10, 10),
        (3, 10, 30),
        (7, 10, 70),
        (9, 10, 90),
        (1, 20, 5),
        (3, 20, 15),
        (9, 20, 45),
        (11, 20, 55),
        (13, 20, 65),
        (17, 20, 85),
        (19, 20, 95),
        (1, 25, 4),
        (2, 25, 8),
        (3, 25, 12),
        (4, 25, 16),
        (6, 25, 24),
        (7, 25, 28),
        (8, 25, 32),
        (9, 25, 36),
        (11, 25, 44),
        (12, 25, 48),
        (13, 25, 52),
        (14, 25, 56),
        (16, 25, 64),
        (17, 25, 68),
        (18, 25, 72),
        (19, 25, 76),
        (21, 25, 84),
        (22, 25, 88),
        (23, 25, 92),
        (24, 25, 96),
        (1, 50, 2),
        (3, 50, 6),
        (7, 50, 14),
        (9, 50, 18),
        (11, 50, 22),
        (13, 50, 26),
        (17, 50, 34),
        (19, 50, 38),
        (21, 50, 42),
        (23, 50, 46),
        (27, 50, 54),
        (29, 50, 58),
        (31, 50, 62),
        (33, 50, 66)
    ]

    # Shuffle and select 50 unique variations
    random.shuffle(fraction_percentage_pairs)
    selected_pairs = fraction_percentage_pairs[:50]

    # Generate variations
    for i, (numerator, denominator, percentage) in enumerate(selected_pairs, start=2):
        variation = copy.deepcopy(template)

        # Update question text
        variation['question_text'] = f"How do you write $\\frac{{{numerator}}}{{{denominator}}}$ as a percentage?\n\nWrite your answer using a percent sign (%).\n"

        # Update correct answer
        variation['correct_answers'] = [f"{percentage}%"]

        # Calculate the multiplier to get to 100
        multiplier = 100 // denominator
        new_numerator = numerator * multiplier

        # Update solution
        variation['solution'] = [
            [
                "1/2",
                f"Write an equivalent fraction with 100 as the denominator.\n\nSince {denominator} x {multiplier} = 100, multiply the numerator ({numerator}) and denominator ({denominator}) by {multiplier}.\n"
            ],
            [
                "2/2",
                f"{numerator} x {multiplier} = {new_numerator} and {denominator} x {multiplier} = 100.\n$\\frac{{{numerator}}}{{{denominator}}} = \\frac{{{new_numerator}}}{{100}} = {percentage}%$\n So, $\\frac{{{numerator}}}{{{denominator}}}$ as a percentage is {percentage}%."
            ]
        ]

        # Update solution image tags
        variation['solution_image_tag'] = [
            [
                "1/2",
                f"Gr7_6_2_1_{i}_step_1",
                f"Shows the conversion of {numerator}/{denominator} to a fraction with denominator 100. The calculation displays: {numerator}/{denominator} x {multiplier}/{multiplier} = {new_numerator}/100, demonstrating how multiplying by {multiplier}/{multiplier} creates an equivalent fraction."
            ],
            [
                "2/2",
                f"Gr7_6_2_1_{i}_step_2",
                f"Shows the final conversion from {new_numerator}/100 to {percentage}%, illustrating that a fraction with denominator 100 directly converts to a percentage."
            ]
        ]

        # Update question number
        variation['question_number'] = f"2_{i}"

        variations.append(variation)

    # Save variations to JSON file
    with open(r'C:\Users\kapil\numi-scraper\Gr7_6_E2 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_6_E2")

if __name__ == "__main__":
    generate_variations()