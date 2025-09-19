import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_9_E2 (multiply-using-the-distributive-property)"""

    # Load template
    with open('Gr7_9_E2_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    # Variables to use
    variables = ['t', 'x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q', 'r', 's', 'w']

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Create variation
        variation = copy.deepcopy(template)

        # Random coefficients
        outer = random.randint(2, 9)
        inner_coef = random.randint(2, 12)
        inner_const = random.randint(1, 9)
        var = random.choice(variables)

        # Calculate results
        result_coef = outer * inner_coef
        result_const = outer * inner_const

        # Update question text
        variation["question_text"] = f"Simplify the expression:\n\n${outer}({inner_coef}{var} + {inner_const}) = \\_\\_\\_\\_$\n\n"

        # Update correct answers with multiple valid forms
        variation["correct_answers"] = [
            [f"{result_coef}{var}+{result_const}"],
            [f"{result_const}+{result_coef}{var}"],
            [f"{var}{result_coef}+{result_const}"],
            [f"{result_const}+{var}{result_coef}"]
        ]

        # Update solution
        variation["solution"] = [
            [
                "1/3",
                f"To simplify the expression ${outer}({inner_coef}{var} + {inner_const})$, apply the distributive property."
            ],
            [
                "2/3",
                f"Multiply {outer} by each term inside the parentheses:\n{outer} × {inner_coef}{var} = {result_coef}{var}\n{outer} × {inner_const} = {result_const}"
            ],
            [
                "3/3",
                f"So, ${outer}({inner_coef}{var} + {inner_const}) = {result_coef}{var} + {result_const}$."
            ]
        ]

        # Update question number
        variation["question_number"] = f"2_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_9_E2 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_9_E2")

if __name__ == "__main__":
    generate_variations()