import json
import random
import copy

def generate_variations():
    # Load the fixed JSON file to get the template
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Find the template with tag Gr7_5_E3
    template = None
    for item in data:
        if item.get('tag') == 'Gr7_5_E3':
            template = item
            break

    if not template:
        print("Template for Gr7_5_E3 not found")
        return

    variations = []

    # Generate 50 variations (51 total including the original template)
    for i in range(2, 52):  # Starting from 3_2 to 3_51
        variation = copy.deepcopy(template)

        # Generate random improper fraction
        denominator = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        whole_part = random.randint(1, 9)
        remainder = random.randint(1, denominator - 1)
        numerator = whole_part * denominator + remainder

        # Update question text
        variation['question_text'] = f"Write $\\frac{{{numerator}}}{{{denominator}}}$ as a mixed number.\n $\\frac{{{numerator}}}{{{denominator}}}$ = _ _/_"

        # Update correct answers
        variation['correct_answers'] = [
            str(whole_part),
            str(remainder),
            str(denominator)
        ]

        # Update solution
        variation['solution'] = [
            [
                "1/3",
                f"To convert $\\frac{{{numerator}}}{{{denominator}}}$ to a mixed number, you need a whole number and a fraction."
            ],
            [
                "2/3",
                f"Consider the remainder when dividing $\\frac{{{numerator}}}{{{denominator}}}$.\n\n$\\frac{{{numerator}}}{{{denominator}}} = {whole_part}$ with a remainder of {remainder}.\n\nThis means $\\frac{{{numerator}}}{{{denominator}}}$ is {whole_part} whole parts and {remainder} left over."
            ],
            [
                "3/3",
                f"Write the remainder as a fraction over the original denominator: $\\frac{{{remainder}}}{{{denominator}}}$. So, $\\frac{{{numerator}}}{{{denominator}}} = {whole_part} \\frac{{{remainder}}}{{{denominator}}}$."
            ]
        ]

        # Update question number
        variation['question_number'] = f"3_{i}"

        variations.append(variation)

    # Save variations to JSON file
    with open(r'C:\Users\kapil\numi-scraper\Gr7_5_E3 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_5_E3")

if __name__ == "__main__":
    generate_variations()