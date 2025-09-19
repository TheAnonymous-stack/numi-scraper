import json
import random
import copy

def generate_variations():
    # Load the fixed JSON file to get the template
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Find the template with tag Gr7_6_E1
    template = None
    for item in data:
        if item.get('tag') == 'Gr7_6_E1':
            template = item
            break

    if not template:
        print("Template for Gr7_6_E1 not found")
        return

    variations = []

    # Common fractions that convert nicely to decimals
    fraction_decimal_pairs = [
        (1, 2, 0.5),
        (1, 5, 0.2),
        (2, 5, 0.4),
        (3, 5, 0.6),
        (4, 5, 0.8),
        (1, 8, 0.125),
        (3, 8, 0.375),
        (5, 8, 0.625),
        (7, 8, 0.875),
        (1, 10, 0.1),
        (3, 10, 0.3),
        (7, 10, 0.7),
        (9, 10, 0.9),
        (1, 20, 0.05),
        (3, 20, 0.15),
        (7, 20, 0.35),
        (9, 20, 0.45),
        (11, 20, 0.55),
        (13, 20, 0.65),
        (17, 20, 0.85),
        (19, 20, 0.95),
        (1, 25, 0.04),
        (2, 25, 0.08),
        (3, 25, 0.12),
        (4, 25, 0.16),
        (6, 25, 0.24),
        (7, 25, 0.28),
        (8, 25, 0.32),
        (9, 25, 0.36),
        (11, 25, 0.44),
        (12, 25, 0.48),
        (13, 25, 0.52),
        (14, 25, 0.56),
        (16, 25, 0.64),
        (17, 25, 0.68),
        (18, 25, 0.72),
        (19, 25, 0.76),
        (21, 25, 0.84),
        (22, 25, 0.88),
        (23, 25, 0.92),
        (24, 25, 0.96),
        (1, 50, 0.02),
        (3, 50, 0.06),
        (7, 50, 0.14),
        (9, 50, 0.18),
        (11, 50, 0.22),
        (13, 50, 0.26),
        (17, 50, 0.34),
        (19, 50, 0.38),
        (21, 50, 0.42),
        (23, 50, 0.46)
    ]

    # Shuffle and select 50 unique variations
    random.shuffle(fraction_decimal_pairs)
    selected_pairs = fraction_decimal_pairs[:50]

    # Generate variations
    for i, (numerator, denominator, decimal) in enumerate(selected_pairs, start=2):
        variation = copy.deepcopy(template)

        # Update question text
        variation['question_text'] = f"Write $\\frac{{{numerator}}}{{{denominator}}}$ as a decimal number.\n"

        # Update correct answer
        variation['correct_answers'] = [str(decimal)]

        # Calculate the multiplier to get to 100
        if 100 % denominator == 0:
            multiplier = 100 // denominator
            new_numerator = numerator * multiplier

            # Update solution
            variation['solution'] = [
                [
                    "1/2",
                    f"Write an equivalent fraction with 100 as the denominator. Since {multiplier} x {denominator} = 100, multiply the numerator ({numerator}) and denominator ({denominator}) by {multiplier}."
                ],
                [
                    "2/2",
                    f"So, $\\frac{{{numerator}}}{{{denominator}}}$ in decimal form is {decimal}"
                ]
            ]

            # Update solution image tag
            variation['solution_image_tag'] = [
                [
                    "1/2",
                    f"Gr7_6_1_1_{i}_step_1",
                    f"Shows the conversion of {numerator}/{denominator} to {new_numerator}/100 by multiplying both numerator and denominator by {multiplier}. The equation {numerator}/{denominator} = {new_numerator}/100 = {decimal} demonstrates the complete conversion process from fraction to decimal."
                ]
            ]
        else:
            # For fractions that don't easily convert to /100
            variation['solution'] = [
                [
                    "1/2",
                    f"To convert $\\frac{{{numerator}}}{{{denominator}}}$ to a decimal, divide the numerator by the denominator."
                ],
                [
                    "2/2",
                    f"So, $\\frac{{{numerator}}}{{{denominator}}}$ in decimal form is {decimal}"
                ]
            ]

            variation['solution_image_tag'] = [
                [
                    "1/2",
                    f"Gr7_6_1_1_{i}_step_1",
                    f"Shows the conversion of {numerator}/{denominator} to decimal form. The division {numerator} ÷ {denominator} = {decimal} demonstrates the conversion process from fraction to decimal."
                ]
            ]

        # Update question number
        variation['question_number'] = f"1_{i}"

        variations.append(variation)

    # Save variations to JSON file
    with open(r'C:\Users\kapil\numi-scraper\Gr7_6_E1 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_6_E1")

if __name__ == "__main__":
    generate_variations()