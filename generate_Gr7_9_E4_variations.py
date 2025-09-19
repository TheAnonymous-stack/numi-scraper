import json
import random
import copy

def generate_variations():
    """Generate variations for Gr7_9_E4 (write-equivalent-expressions-using-properties)"""

    # Load template
    with open('Gr7_9_E4_templates.json', 'r', encoding='utf-8') as f:
        templates = json.load(f)

    template = templates[0]

    # Variables to use
    variables = ['s', 'x', 'y', 'z', 'a', 'b', 'c', 'm', 'n', 'p', 'q', 'r', 't', 'w']

    variations = []
    variation_num = 2

    # Generate 50 variations
    while len(variations) < 50:
        # Create variation
        variation = copy.deepcopy(template)

        # Random values
        var = random.choice(variables)
        const1 = random.randint(1, 9)
        coef = random.randint(2, 12)
        const2 = random.randint(1, 9)

        # Calculate sum of constants
        sum_const = const1 + const2

        # Update question text with proper formatting
        variation["question_text"] = f"Complete the expressions below. Write each answer as a number, a variable, or the product of a number and a variable.\n\nExpression: ${const1} + {coef}{var} + {const2}$\n\nStep 1: Rearrange using the commutative property of addition\n\n$\\_\\_\\_\\_ + {const1} + {const2}$\n\nStep 2: Add the constants\n\n${coef}{var} + \\_\\_\\_\\_$\n"

        # Update correct answers
        variation["correct_answers"] = [f"{coef}{var},{sum_const}"]

        # Update solution
        variation["solution"] = [
            [
                "1/6",
                f"We are given the expression: ${const1} + {coef}{var} + {const2}$."
            ],
            [
                "2/6",
                "Use the commutative property of addition to change the order of the terms. This property says that numbers can be added in any order."
            ],
            [
                "3/6",
                f"So, ${const1} + {coef}{var} + {const2} = {coef}{var} + {const1} + {const2}$."
            ],
            [
                "4/6",
                f"Now simplify the constants ${const1} + {const2}$. \n${const1} + {const2} = {sum_const}$"
            ],
            [
                "5/6",
                f"Replace ${const1} + {const2}$ with {sum_const} in the expression: ${coef}{var} + {sum_const}$."
            ],
            [
                "6/6",
                f"So, ${const1} + {coef}{var} + {const2} = {coef}{var} + {sum_const}$."
            ]
        ]

        # Update question number
        variation["question_number"] = f"4_{variation_num}"

        variations.append(variation)
        variation_num += 1

    # Save variations
    with open('Gr7_9_E4 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_9_E4")

if __name__ == "__main__":
    generate_variations()